#coding:utf-8
from __future__ import unicode_literals
# 科学计算，计算到比较后的小数位
from __future__ import division
import re
import sys

from utils.tfidf import tfidf
from utils.ArticleTool import GetWrodContent, IsFen
from utils.lda import GetTheme

from django.shortcuts import render
# Create your views here.
from django.views.generic import View
from django import forms

reload(sys)
sys.setdefaultencoding('utf8')

class ArticleForm(forms.Form):
    # 至少输入一个关键字
    keyword = forms.CharField(required=True, min_length=1)


class ArticleView(View):
    def get(self, request):
        return render(request, 'index.html')
    def post(self, request):
        keyword = ArticleForm(request.POST)
        if keyword.is_valid():
            # 遍历数据表，将没有分词的文件进行分词
            # IsFen()
            # initdata()
            word = request.POST.get('keyword','')
            # 空格分割
            keylist = word.split()
            reslist = tfidf(keylist)
            contentdict = dict()
            themelist = list()
            if len(reslist):
                contentdict = GetWrodContent(reslist,keylist)
                # theme : [(0, u'0.081*" " + 0.037*"." + 0.023*"pyenv"')]
                theme = GetTheme(reslist)
                themelist = re.compile('"(.*?)"').findall(theme[0][1])
            return render(request, 'index.html', {
                'contentdict':contentdict,
                'themelist':themelist,
            })
        return render(request, 'index.html')