# _*_ coding:utf-8 _*_
from __future__ import division
from article.models import ArticleModel
import json
import math

# tfidf,使用Django中的ORM来对数据库进行操作
def tfidf(keylist):
    reskeylist = list()
    for key in keylist:
        articles = ArticleModel.objects.filter(file_fence__icontains=key)
        print articles
        reskeylist.append(articles)

    keyDict = dict()
    for articles in reskeylist:
        for article in articles:
            id = int(article.id)
            keyDict[id] = 0

    print keyDict
    # 文章总数
    allFileNum = ArticleModel.objects.count()
    if allFileNum <= 0:
        allFileNum = 1

    i = 0
    for articles in reskeylist:
        # 有相关文章才计算
        if len(articles)>0:
            # 相关文章的数量
            similarFileNum = len(articles)
            idf = math.log(allFileNum/similarFileNum)
            print idf
            tf = 0
            tflist = list()
            for article in articles:
                am = ArticleModel.objects.get(id=article.id)
                fenjson = json.loads(am.file_fence)
                #关键词在分词列表中的次数
                fenNum = fenjson.count(keylist[i])
                # 文章总长度
                WordNum = len(fenjson)
                if WordNum <=0:
                    WordNum = 1
                tf = fenNum/WordNum
                keyDict[int(article.id)] += tf*idf
    # {365: 0.01997152565305817, 366: 0.012601575957802818, 367: 0.0, 371: 0.011724096780857167, 372: 0.003015601012787639, 374: 0.007828322186332488}
    print keyDict
    # 排序，reverse=True 降序,并将dict转成了list
    # [(365, 0.01997152565305817), (366, 0.012601575957802818), (371, 0.011724096780857167), (374, 0.007828322186332488), (372, 0.003015601012787639), (367, 0.0)]
    reslist = sorted(keyDict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    return reslist[0:5]
