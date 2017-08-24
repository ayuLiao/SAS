# _*_ coding:utf-8 _*_

import xadmin

from  .models import UploadModel

class UploadAdmin(object):

    list_display = ['file_name', 'file_path']
    search_fields = ['file_name', 'file_path']
    list_filter = ['file_name', 'file_path']

xadmin.site.register(UploadModel,UploadAdmin)