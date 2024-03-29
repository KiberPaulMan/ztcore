import requests
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from call_center.forms import DateForm, CommentForm
from .models import IncomingCall, Comment

CHOICES_FULL_NAME_OPERATOR = {
    '89130856155': 'Пастухова Ю.',
    '89833820992': 'Прохорова Е.',
    '89833900748': 'Резервный',
    '89835458998': 'Граверы',
    None: None,
}


def get_data_from_api(url, payload):
    headers = {
        'Authorization': settings.MTS_API_KEY
    }
    data = requests.get(url, headers=headers, params=payload)
    return data.json() if data.status_code == 200 else None


def get_comment(request):
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = Comment.objects.get(incoming_call__pk=int(request.POST.get('incoming_call')))
        comment.status = form.cleaned_data['status']
        comment.title = form.cleaned_data['title']
        comment.save()


def get_clients_data(incoming_calls, date_start, date_finish):
    clients = []
    total_numbers = []
    total_info = {}

    client_data = IncomingCall.objects.filter(
        seqId__in=get_seq_id_incoming_calls_from_db(date_start, date_finish))

    if client_data:
        for obj in client_data:
            if obj.log != 'denyservice':

                comment = Comment.objects.get(incoming_call=obj)

                if obj.cn:
                    comment.status = Comment.STATUS_CHOICES[1]
                    comment.save()

                client = {
                    'number_of_client': obj.an,
                    'number_of_employee': obj.cn,
                    'operator_full_name': CHOICES_FULL_NAME_OPERATOR[obj.cn],
                    'start_time': obj.startTime[11:],
                    'call_date': obj.startTime[:10],
                    'duration': obj.duration - obj.talkDuration,
                    'talk_duration': obj.talkDuration,
                    'comment_form': CommentForm(instance=comment),
                    'client_id': obj.pk,
                }
                total_numbers.append(obj.an)
                clients.append(client)

        total_info = {
            'total_numbers': len(total_numbers),
            'unique_numbers': len(set(total_numbers)),
        }

        if incoming_calls == 'unanswered_calls':
            clients = [client for client in clients if client['number_of_employee'] is None]
        elif incoming_calls == 'answered_calls':
            clients = [client for client in clients if client['number_of_employee'] is not None]

    return {'clients': clients, 'total_info': total_info}


@login_required(login_url='login')
def get_statistics_of_incoming_calls(request):
    clients_data = {
        'clients': None,
        'total_info': None
    }
    url = 'https://aa.mts.ru/api/v5/Cdr/GetByTime'
    payload = {
        'Phone': 8002509921,
        'Limit': 2000,
    }

    if request.method == 'POST':

        if 'incoming_call' in request.POST:
            get_comment(request)

        form = DateForm(request.POST)

        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_finish = form.cleaned_data['date_finish']
            incoming_calls = form.cleaned_data['incoming_calls']

            payload['Begin'] = date_start + 'T00:00:00'
            payload['End'] = date_finish + 'T23:59:59'

            data = get_data_from_api(url, payload)
            save_data_from_api_to_db(data, date_start, date_finish)
            clients_data = get_clients_data(incoming_calls, date_start, date_finish)

    else:
        form = DateForm()

    return render(request,
                  'call_center/incoming_calls.html',
                  context={'form': form,
                           'clients': clients_data['clients'],
                           'total_info': clients_data['total_info'],
                           })


def save_data_from_api_to_db(data, date_start, date_finish):
    seq_id = get_seq_id_incoming_calls_from_db(date_start, date_finish)
    if data:
        for item in data:
            if item['seqId'] not in seq_id:
                incoming_call = IncomingCall.objects.create(**item)
                Comment.objects.create(incoming_call=incoming_call)


def get_seq_id_incoming_calls_from_db(date_start, date_finish):
    seq_id = []
    for current_date in get_list_dates(date_start, date_finish):
        for obj in IncomingCall.objects.filter(startTime__startswith=current_date):
            seq_id.append(obj.seqId)
    return seq_id


def get_list_dates(date_start, date_finish):
    start = datetime.strptime(date_start, '%Y-%m-%d')
    end = datetime.strptime(date_finish, '%Y-%m-%d')

    return [(start + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0, (end - start).days + 1)]


