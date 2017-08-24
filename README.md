# SAS
最相关文章搜索引擎

整个Web应用使用了Django（1.9.0）构建

前端使用了Bootstrap简单实现

## SAS的功能：

用户输入关键字，后台可以根据用户输入的关键字从数据库中搜索出最相关的文章（前5章），并将文章中与关键字的内容返回

搜索最相关文章的算法使用了TF-IDF，简单暴力

同时在返回相关内容时，对这些内容进行了主题聚类，使用了gensim库的LDA模型，可能语料不是非常充足，所以主题聚类的效果不是特别好

后台使用了xadmin来搭建

重写了其中的文章上传方法，当文章上传时，会对文章中的内容进行中文分词，去除停用词，然后存入数据库中，用于TF-IDF算法的计算

## 环境与第三方库

Python2.7
Doc2vec
jieba
gensim
numpy
Django
xadmin相关的支持库

## 效果

前端效果：
![](http://onxxjmg4z.bkt.clouddn.com/sas_q.png)

后端效果
![](http://onxxjmg4z.bkt.clouddn.com/sas_h.png)
