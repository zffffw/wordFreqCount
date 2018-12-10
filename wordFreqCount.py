import codecs
import jieba
import jieba.posseg as pseg
import sys
import re
import numpy as np

class PartOfSpeechStat():
    def __init__(self, partOfSpeechList = []):
        self.partOfSpeechList = partOfSpeechList if partOfSpeechList else ['n', 'a', 'v', 'u', 'p']
        self.partOfSpeech = {}
    '''
        sieve the character if it's not chinese and some other specified characters
    '''
    def cleanUnChinese(self, line):
        return re.sub(r"[^\u4e00-\u9fa5！？｡＂＇（），：；､、!\"\'(),-.:;?\[\]]", '',  line)
    '''
        initial the dictionary
    '''
    def initPartOfSpeech(self):
        print("init dictionary  ---->", end='  ')
        for pos in self.partOfSpeechList:
            self.partOfSpeech[pos] = {}
        print("init ok")
    '''
        pos为指定词性，n为前n个出现次数最高的词
    '''
    def getTopN(self, pos, n):
        tempList = list(zip(self.partOfSpeech[pos], self.partOfSpeech[pos].values()))
        result = sorted(tempList, key = lambda x : -x[1])[:n]
        print(result)
        return result
    '''
        全角转半角
    '''
    def strQ2B(self, ustring):
        """全角转半角"""
        rstring = ""
        for uchar in ustring:
            inside_code=ord(uchar)
            if inside_code == 12288:                              #全角空格直接转换            
                inside_code = 32 
            elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        return rstring
    def addWord(self, word, flag):
        if flag in self.partOfSpeech and word in self.partOfSpeech[flag]:
            self.partOfSpeech[flag][word] += 1
        elif flag in self.partOfSpeech:
            self.partOfSpeech[flag][word] = 1
    def addSentence(self, textLine):
        words = pseg.cut(textLine)
        for word, flag in words:
            self.addWord(word, flag)
    def addArticle(self, articleSentenceList):
        print("adding article into the dictionary  ---->", end='  ')
        for line in articleSentenceList:
            line = line.strip('\n')
            line = self.strQ2B(line)
            line = self.cleanUnChinese(line)
            self.addSentence(line)
        print("add ok")
    def save(self, name):
        print("saving the dictionary  ---->", end='  ')
        numpyArray = np.array([self.partOfSpeechList, self.partOfSpeech])
        np.save(name, numpyArray)
        print("save success: {}.npy".format(name))  
    def load(self, name):
        print("loading the dictionary  ---->", end='  ')
        numpyAarray = np.load(name+'.npy')
        self.partOfSpeechList = numpyAarray[0]
        self.partOfSpeech = numpyAarray[1]
        print("load success")
    def createWordFreqCount(self, name, articleSentenceList):
        self.initPartOfSpeech()
        self.addArticle(articleSentenceList)
        self.save(name)     


if __name__=='__main__':
    article = codecs.open('/Users/zhang/Documents/琼瑶小说爬虫/琼瑶.txt', 'r', encoding='utf-8')
    fileLines = article.readlines()
    test = PartOfSpeechStat()
    test.createWordFreqCount('琼瑶词频', fileLines)
    # test.load('鲁迅词频')
    # test.getTopN('a', 100)
    # print(test.partOfSpeech)
    
