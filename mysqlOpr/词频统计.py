# encoding=utf-8
from __future__ import print_function, unicode_literals
import jieba.analyse
import xlwt  # 写入Excel表的库
from operator import itemgetter

import jieba.posseg as pseg


class JieBaUtil():
    '''
    结巴分词工具类
    '''

    def 一句话分词(self, words, space=' ', cut_allType=2):
        '''
        选择模式进行匹配
        :param words: 需要分词的语句
        :param space: 分词后的分隔符
        :param cut_allType:1:全模式；2：精确模式（默认是精确模式）;3:搜索引擎模式
        :return: 分好词的字符串
        '''
        mystr = ''
        if cut_allType == 1:
            seg_list = jieba.cut(words, cut_all=True)
            mystr = space.join(seg_list)  # 全模式
        elif cut_allType == 2:
            seg_list = jieba.cut(words)  # 默认是精确模式
            mystr = space.join(seg_list)
        elif cut_allType == 3:
            seg_list = jieba.cut_for_search(words)  # 搜索引擎模式
            mystr = space.join(seg_list)
        return mystr

    def 使用停用词库进行分词(self, file_name):

        # sys.path.append("../")将本文件父目录添加到搜索列表。这样就可以只填写文件名称了。
        jieba.load_userdict(file_name)

        jieba.add_word('石墨烯')
        jieba.add_word('凱特琳')
        jieba.del_word('自定义词')

        test_sent = (
            "李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
            "例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
            "「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
        )
        words = jieba.cut(test_sent)
        print('/'.join(words))

        print("=" * 40)

        result = pseg.cut(test_sent)

        for w in result:
            print(w.word, "/", w.flag, ", ", end=' ')

        print("\n" + "=" * 40)

        terms = jieba.cut('easy_install is great')
        print('/'.join(terms))
        terms = jieba.cut('python 的正则表达式是好用的')
        print('/'.join(terms))

        print("=" * 40)
        # test frequency tune
        testlist = [
            ('今天天气不错', ('今天', '天气')),
            ('如果放到post中将出错。', ('中', '将')),
            ('我们中出了一个叛徒', ('中', '出')),
        ]

        for sent, seg in testlist:
            print('/'.join(jieba.cut(sent, HMM=False)))
            word = ''.join(seg)
            print('%s Before: %s, After: %s' % (word, jieba.get_FREQ(word), jieba.suggest_freq(seg, True)))
            print('/'.join(jieba.cut(sent, HMM=False)))
        print("-" * 40)

    def 读写文章分词统计全(self, textList,stopWordsFilePath=None, getList=True, sortType=3):
        '''
        需要分词并且统计的文本，可以是String，也可以是存放String的列表
        :param text: 需要分词的文本
        :param getList: 返回词频字典还是已排序的词频列表，默认为列表
        :param sort: 排序类型 0：按键、正序；1：按键、倒叙；2：按值、正序；3：按值、倒叙
        :return:默认返回排序后的列表
        '''
        # 分词结果列表
        word_lst = []
        if isinstance(textList,(list,tuple)):
            for line in textList:
                word_lst=self.分词(line)
        else:
            word_lst=self.分词(textList)
        word_dict = {}  # 分词后的统计字典
        stopWords=self.getStopWords(stopWordsFilePath)
        for item in word_lst:
            if item not in word_dict:
                if item not in word_dict:  # 统计数量
                    word_dict[item] = 1  # 如果不在字典中，那么添加上
                else:
                    word_dict[item] += 1  # 在字典中，则数量+1
        if not getList:#默认不返回字典。如果为getList为False，则返回字典
            return word_dict
        # 排序
        word_list=[]
        word_list = self.sortDict(word_dict,sortType)
        return word_list

    def getStopWords(self,stopWordsFilePath):
        if stopWordsFilePath is None:
            return []
        stopwords = [line.strip() for line in open(stopWordsFilePath, 'r').readlines()]
        return stopwords


    def sortDict(self,word_dict,sortType):
        '''
        对字典进行排序。可以按键、值进行排序
        :param word_dict:需要排序的字典
        :param sortType:排序类型 0：按键、正序；1：按键、倒叙；2：按值、正序；3：按值、倒叙
        :return: 列表：排序后包含元组（key-value）的列表：[('a', 8), ('b', 4), ('c', 12)]
        '''
        word_list = []
        if sortType == 3:
            # 键、正序
            word_list = sorted(word_dict.items(), key=itemgetter(1), reverse=True)
        elif sortType == 2:
            # 值、正序
            word_list = sorted(word_dict.items(), key=itemgetter(1), reverse=False)
        elif sortType == 1:
            # 键、正序
            word_list = sorted(word_dict.items(), key=itemgetter(0), reverse=True)
        elif sortType == 0:  # 对键进行排序:正序
            # 键、正序
            word_list = sorted(word_dict.items(), key=itemgetter(0), reverse=False)
        return word_list


    def 分词(self, line):
        '''
        对一行文本进行分词，分词结果追加到列表中
        :param line:
        :return: 分词后的list
        '''
        word_lst=[]
        item = line.strip('\n\r').split('\t')  # 制表格切分
        # print item
        tags = jieba.analyse.extract_tags(item[0])  # jieba分词
        for t in tags:
            word_lst.append(t)
        return word_lst

    def 读写文件分词统计(self, inFilePath, inEncoding, outFilePath, outEncoding):
        '''
        读写文件分词统计
        :param inFilePath:数据来源，应该是txt格式
        :param inEncoding:数据来源文件编码
        :param outFilePath:写入的文件，格式为txt或excel
        :param outEncoding:写入文件的编码格式
        :return:
        '''
        word_lst = []
        key_list = []
        with open(file=inFilePath, mode='r+', encoding=inEncoding) as rfile:
            for line in rfile:
                item = line.strip('\n\r').split('\t')  # 制表格切分
                # print item
                tags = jieba.analyse.extract_tags(item[0])  # jieba分词
                for t in tags:
                    word_lst.append(t)
            word_dict = {}
            for item in word_lst:
                if item not in word_dict:  # 统计数量
                    word_dict[item] = 1
                else:
                    word_dict[item] += 1

            orderList = list(word_dict.values())
            orderList.sort(reverse=True)  # 倒序排序
            # print orderList
            for i in range(len(orderList)):
                for key in word_dict:
                    if word_dict[key] == orderList[i]:
                        # rfile.write(key + ' ' + str(word_dict[key]) + '\n')  # 写入txt文档
                        key_list.append(key)
                        word_dict[key] = 0
        # 写文件
        wbk = xlwt.Workbook(encoding=outEncoding)
        sheet = wbk.add_sheet("Sheet1")  # Excel单元格名字
        for i in range(len(key_list)):
            sheet.write(i, 1, label=orderList[i])
            sheet.write(i, 0, label=key_list[i])
        wbk.save(outFilePath)  # 保存为 wordCount.xls文件


if __name__ == "__main__":
    jie = JieBaUtil()
    # jie.读写文件分词统计('F:/Profile/User/Desktop/wordCount.txt', 'gbk', 'F:/Profile/User/Desktop/wordCount.xls', 'ascii')
    # jie.使用停用词库进行分词('resource/jieba/stopword/医院信息化要求项目停用词表.txt')
    test_sent = [
        "李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
        "例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
        "「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
    ]
    a= jie.读写文章分词统计全(test_sent)
    print(a)