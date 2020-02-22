# encoding=utf-8

import jieba.analyse
import xlwt  # 写入Excel表的库
from operator import itemgetter


class JieBaUtil():
    '''
    结巴分词工具类
    '''

    def 一句话分词(self,words, space=' ', cut_allType=2):
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


    def 读写文章分词统计(self,text, getList=True, sort=3):
        '''
        需要分词并且统计的文本，可以是String，也可以是存放String的列表
        :param text: 需要分词的文本
        :param getList: 返回词频字典还是已排序的词频列表，默认为列表
        :param sort: 排序类型 0：按键、正序；1：按键、倒叙；2：按值、正序；3：按值、倒叙
        :return:
        '''
        # 分词结果列表
        word_lst = []
        if isinstance(text, (list, tuple)):
            for line in text:
                self.分词(line)
        else:
            self.分词(text)
        word_dict = {}  # 分词后的统计字典
        for item in word_lst:
            if item not in word_dict:  # 统计数量
                word_dict[item] = 1  # 如果不在字典中，那么添加上
            else:
                word_dict[item] += 1  # 在字典中，则数量+1
        if not getList:
            return word_dict
        # 包含元组（key-value）的列表：[('a', 8), ('b', 4), ('c', 12)]
        list = []
        if sort == 3:
            # 键、正序
            list = sorted(word_dict.items(), key=itemgetter(1), reverse=True)
        elif sort == 2:
            # 值、正序
            list = sorted(word_dict.items(), key=itemgetter(1), reverse=False)
        elif sort == 1:
            # 键、正序
            list = sorted(word_dict.items(), key=itemgetter(0), reverse=True)
        elif sort == 0:  # 对键进行排序:正序
            # 键、正序
            list = sorted(word_dict.items(), key=itemgetter(0), reverse=False)
        return list


    def 分词(self,line, word_lst):
        '''
        对一行文本进行分词，分词结果追加到列表中
        :param line:
        :param word_lst:
        :return:
        '''
        item = line.strip('\n\r').split('\t')  # 制表格切分
        # print item
        tags = jieba.analyse.extract_tags(item[0])  # jieba分词
        for t in tags:
            word_lst.append(t)


    def 读写文件分词统计(self,inFilePath, inEncoding, outFilePath, outEncoding):
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
    jie. 读写文件分词统计('F:/Profile/User/Desktop/wordCount.txt','gbk','F:/Profile/User/Desktop/wordCount.xls','ascii')
