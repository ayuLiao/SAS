# _*_ coding:utf-8 _*_

from article.models import ArticleModel,UploadModel
from SAS.settings import MEDIA_ROOT
import docx2txt
import jieba
import hashlib
import re
import os
import json

def getStopword():
    stopwordPath = os.getcwd()+'/static/stopwords.txt'
    with open(stopwordPath, 'r') as f:
        # 将\n转成空格，通过空格分割，成为list
        stopwordlist = f.read().replace('\n', ' ').split(' ')
    stopwordlist.append('\n')
    stopwordlist.append(' ')
    return stopwordlist

def initdata(filedir = os.getcwd()+'/Data'):
    stopwordlist = getStopword()
    for path in os.listdir(filedir):
        fileExten = path.split('.')[-1]
        if fileExten == 'docx':
            filepath = filedir+'/'+path
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
            article.file_name = path
            article.file_path = filepath
            article.file_md5 = filemd5
            article.file_fence = fenceJson
            article.save()

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


def IsFen():
    uploadFile = UploadModel.objects.filter(is_fen=False)

    for uf in uploadFile:
        uf.is_fen = True
        path = os.path.join(MEDIA_ROOT, uf.file_path.name.encoding('utf8'))
        uf.save()
        initdata(path)



# 获得相关文章的分词内容
def GetWrodContent(reslist,keylist):
    wordcontent = dict()
    # 遍历最相关文章列表，通过id获得内容
    for res in reslist:
        id = res[0]
        article = ArticleModel.objects.get(id = id)
        filepath = article.file_path
        # 把文件结尾去除
        filename = article.file_name.split('.')[0]
        text = docx2txt.process(filepath)
        # 分句
        wordlist = re.split('\n', text)
        showlist = list()
        # 获得不同的分句，判断关键词是否在句子中
        for words in wordlist:
            for key in keylist:
                # 关键字是否在句子中
                if key in words:
                    showlist.append(words)
                    break

        wordcontent[filename] = showlist[0:5]
    return wordcontent