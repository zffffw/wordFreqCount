# 词频统计小工具

该工具可以统计文章的词频，分词工具使用的是结巴

使用方法:
1. 创建类

```python
partOfSpeechList = ['n', 'v', 'a']
test = PartOfSpeechStat(partOfSpeechList)
```

其中词性表可以缺省，默认为['n', 'a', 'v', 'u', 'p']

2. 统计词频

test.createWordFreqCount(保存文件名, 打开文章后readlines之后的列表)

3. 输出指定词性词频最高的n个词

test.getTopN(词性, n)

4. 加载文件

test.load(文件名)

其他诸如文章对比功能还没完善。
