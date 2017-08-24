# _*_ coding:utf-8 _*_
from __future__ import division
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim import corpora
import gensim
from article.models import ArticleModel
import json


#LDA算法
def GetTheme(reslist):
    fencelist = list()
    for res in reslist:
        id = res[0]
        article = ArticleModel.objects.get(id = id)
        filefence = json.loads(article.file_fence)
        fencelist.append(filefence)
    dictionary = corpora.Dictionary(fencelist)
    corpus = [dictionary.doc2bow(word) for word in fencelist]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=20)
    # print(ldamodel.print_topics(num_topics=2, num_words=3))
    return ldamodel.print_topics(num                      _topics=1, num_words=3)