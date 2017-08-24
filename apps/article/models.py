#coding:utf-8
from __future__ import unicode_literals

import hashlib
import json
import os

import warnings

import jieba
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.deprecation import RemovedInDjango110Warning
from django.utils.encoding import force_text
from django.utils.inspect import func_supports_parameter
from django.core.files import File
import docx2txt
from SAS.settings import MEDIA_ROOT

# Create your models here.
class ArticleModel(models.Model):
    file_name = models.CharField(max_length=50, verbose_name=u'文章名称')
    file_path = models.CharField(max_length=150, verbose_name=u'文章路径')
    file_md5 = models.CharField(max_length=32, verbose_name=u'文章MD5')
    file_fence = models.TextField(verbose_name=u'文章分词')

    class Meta:
        verbose_name = u'文章信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.file_name

def getStopword():
    stopwordPath = os.getcwd()+'/static/stopwords.txt'
    with open(stopwordPath, 'r') as f:
        # 将\n转成空格，通过空格分割，成为list
        stopwordlist = f.read().replace('\n', ' ').split(' ')
    stopwordlist.append('\n')
    stopwordlist.append(' ')
    return stopwordlist

def initFile(filepath):
    stopwordlist = getStopword()
    filemd5 = ''
    with open(filepath, 'rb') as f:
        m = hashlib.md5()
        m.update(f.read())
        filemd5 = m.hexdigest()
    text = docx2txt.process(filepath)
    fence = jieba.cut_for_search(text)
    fencelist = list()
    for f in fence:
        if f in stopwordlist:
            continue
        fencelist.append(f)
    fenceJson = ''
    if fence:
        # 以json的形式存数据，不要转成ascii
        fenceJson = json.dumps(fencelist, ensure_ascii=False)
    article = ArticleModel()
    article.file_name = filepath.split('\\')[-1]
    article.file_path = filepath
    article.file_md5 = filemd5
    article.file_fence = fenceJson
    article.save()

class MyStorge(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        filepath = os.path.join(MEDIA_ROOT, name)
        if self.exists(name):
            os.remove(filepath)
        return name

    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name

        if not hasattr(content, 'chunks'):
            content = File(content)

        if func_supports_parameter(self.get_available_name, 'max_length'):
            name = self.get_available_name(name, max_length=max_length)
        else:
            warnings.warn(
                'Backwards compatibility for storage backends without '
                'support for the `max_length` argument in '
                'Storage.get_available_name() will be removed in Django 1.10.',
                RemovedInDjango110Warning, stacklevel=2
            )
            name = self.get_available_name(name)

        name = self._save(name, content)
        print name
        initFile(os.path.join(MEDIA_ROOT, name))
        # Store filenames with forward slashes, even on Windows
        return force_text(name.replace('\\', '/'))




class UploadModel(models.Model):
    file_name = models.CharField(max_length=50, verbose_name=u'文章名称')
    file_path = models.FileField(upload_to='article/%Y/%m', verbose_name=u'文章', storage=MyStorge())
    is_fen = models.BooleanField(default=False, verbose_name=u'是否分词')

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.file_name

