from django.contrib import admin

from .models import Node, Line, Device, Market, member, hosts, command, T_Host, T_Command
from .models import Employee, Task, Process, Upload
# Register your models here.

class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_name','node_address','node_signer')
    exclude = ['node_signer']
    def save_model(self, request, obj, form, change):
        obj.node_signer = str(request.user)
        obj.save()

class LineAdmin(admin.ModelAdmin):
    exclude = ('line_signer',)
    def save_model(self, request, obj, form, change):
        obj.line_signer = str(request.user)
        obj.save()

class DeviceAdmin(admin.ModelAdmin):
    exclude = ('device_signer',)
    def save_model(self, request, obj, form, change):
        obj.device_signer = str(request.user)
        obj.save()

class MarketAdmin(admin.ModelAdmin):
    list_display = ('market_name','market_address','market_contact')
    exclude = ['node_signer']
    def save_model(self, request, obj, form, change):
        obj.node_signer = str(request.user)
        obj.save()

admin.site.register(Node, NodeAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(Market, MarketAdmin)
admin.site.register(member)
admin.site.register(hosts)
admin.site.register(command)
admin.site.register(T_Host)
admin.site.register(T_Command)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(Process)
admin.site.register(Upload)