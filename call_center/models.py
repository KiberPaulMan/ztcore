from django.db import models


class IncomingCall(models.Model):
    seqId = models.PositiveBigIntegerField()
    un = models.CharField(max_length=15, verbose_name='hotline number')
    an = models.CharField(max_length=15, verbose_name='number of client')
    cn = models.CharField(max_length=15, verbose_name='number of operator', blank=True, null=True)
    startTime = models.CharField(max_length=20, verbose_name='date and time of the call')
    duration = models.PositiveSmallIntegerField(verbose_name='total call duration')
    talkDuration = models.PositiveSmallIntegerField(verbose_name='call duration')
    recDuration = models.PositiveSmallIntegerField(verbose_name='call recording')
    log = models.CharField(max_length=5000, verbose_name='log')
    result = models.PositiveIntegerField()
    subResult = models.IntegerField()
    outbounds = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering: ['startTime', ]

    def __str__(self):
        return f'seq_id {self.seqId}'


class Comment(models.Model):
    STATUS_CHOICES = (
        ('status_1', 'Не обработан'),
        ('status_2', 'Обработан'),
        ('status_3', 'Не дозвонились'),
        ('status_4', 'Перезвонить'),
        ('status_5', 'Спам'),
    )
    incoming_call = models.OneToOneField(IncomingCall, on_delete=models.CASCADE, related_name='comments')
    title = models.TextField(blank=True, null=True, verbose_name='comment')
    status = models.CharField(choices=STATUS_CHOICES, default='status_1', verbose_name='status')

    def __str__(self):
        return f'{self.incoming_call}'
