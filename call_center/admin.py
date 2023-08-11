from django.contrib import admin
from .models import IncomingCall, Comment


class IncomingCallAdmin(admin.ModelAdmin):
    list_display = ['seqId', 'an', 'cn', 'log', 'startTime']


# class IncomingCallInline(admin.TabularInline):
#     model = IncomingCall


class CommentAdmin(admin.ModelAdmin):
    list_display = ['incoming_call', 'status', 'title']
    list_filter = ['status']
    # inlines = (IncomingCallInline, )


admin.site.register(IncomingCall, IncomingCallAdmin)
admin.site.register(Comment, CommentAdmin)
