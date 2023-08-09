from django.http import HttpResponse
import requests
from django.shortcuts import render
from call_center.forms import DateForm
from ztcore.settings import MTS_API_KEY

CHOICES_FULL_NAME_OPERATOR = {
    '89130856155': 'Пастухова Ю.',
    '89833820992': 'Прохорова Е.',
    '89833900748': 'Резервный',
    '89835458998': 'Граверы',
    None: None,
}


def index(request):
    return HttpResponse('Server is worked!')


def get_data_from_api(url, payload):
    """
    Получить статистику входящих звонков за определенный период.
    По умолчанию период это сегодняшний день.
    """
    headers = {
        'Authorization': MTS_API_KEY
    }
    data = requests.get(url, headers=headers, params=payload)
    # print('DATA = ', data)
    return data.json() if data.status_code == 200 else None


def get_clients_data(data, incoming_calls):
    clients = []
    total_numbers = []
    total_info = {}

    if data:
        for item in data['items']:
            client = {
                'number_of_client': item['an'],
                'number_of_employee': item['cn'],
                'operator_full_name': CHOICES_FULL_NAME_OPERATOR[item['cn']],
                'start_time': item['startTime'][11:],
                'call_date': item['startTime'][:10],
                'duration': item['duration'] - item['talkDuration'],
                'talk_duration': item['talkDuration'],
            }
            total_numbers.append(item['an'])
            clients.append(client)

        total_info = {
            'total_numbers': len(total_numbers),
            'unique_numbers': len(set(total_numbers)),
        }

        clients.sort(key=lambda dictionary: dictionary['start_time'])

        if incoming_calls == 'unanswered_calls':
            clients = [client for client in clients if client['number_of_employee'] is None]
        elif incoming_calls == 'answered_calls':
            clients = [client for client in clients if client['number_of_employee'] is not None]

    return {'clients': clients, 'total_info': total_info}


def get_statistics_of_incoming_calls(request):
    clients_data = {
        'clients': None,
        'total_info': None
    }
    url = 'https://aa.mts.ru/api/v5/Cdr/GetByTimePaging'
    payload = {
        'Phone': 8002509921,
        'Limit': 2000,
    }

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            date_start = form.cleaned_data['date_start']
            date_finish = form.cleaned_data['date_finish']
            incoming_calls = form.cleaned_data['incoming_calls']

            payload['Begin'] = date_start + 'T00:00:00'
            payload['End'] = date_finish + 'T23:59:59'

            data = get_data_from_api(url, payload)
            clients_data = get_clients_data(data, incoming_calls)

    else:
        form = DateForm()
    return render(request,
                  'call_center/incoming_calls.html',
                  context={'form': form,
                           'clients': clients_data['clients'],
                           'total_info': clients_data['total_info'],
                           })
