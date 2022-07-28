# -*- coding: utf-8 -*-
# python3+  批量统计目录下文件中关键词出现的概率
# 处理当前文件所在目录下的所有终极目录下的文件， 文件类为.txt, 文件命名格式为 year+名字，例如：2021年中报告.txt
# 如需处理其他文件格式，修改下面代码即可

from operator import index
import os
import os.path
# decode open txt
import codecs
from pickle import FALSE
# 分割文档
import jieba
# 模糊匹配
import difflib
from numpy import append
import pandas as pd


# 参数设置
class Config:
     def __init__(self):
        self.path = '.'+os.sep  # 根目录
        self.root = "." +os.sep
        self.provinces = ['安徽','河北']    # 根目录下的子目录
        self.words= ['人居环境','农村人居环境','国民经济','经济和社会','退休']            # 需要统计的词
        self.date_range=[2003,2020]        # 数据年限跨度，闭区间
        self.cutoff=0.8                    # 模糊匹配比例，越大精度越高
config = Config()


# 词频统计
def word_freq( fPath ):   
    # root = "./"
    # name = "demo.txt"
    # filepath = os.path.join(root,name)
    print(fPath)
    f=codecs.open(fPath,'r',encoding='UTF-8') # open txt
    filecontent=f.read()   # read txt
    seg=jieba.lcut(filecontent)   # 分割
    nums = 0
    for word in config.words:
        # print(word)
        # 模糊匹配
        select_word1=difflib.get_close_matches(word, seg, len(seg),cutoff=config.cutoff) 
        # 剔除负向相似匹配，即被选取字段长度一定要大于等于目标字段长度
        select_word2=list(select_word1[j] for j in range(len(select_word1)) if len(select_word1[j])>=len(word))
        num_word = len(select_word2)
        # 查看区别
        # print(select_word1)
        # print(select_word2)
        # print(num_word)
        nums += num_word
        #print(len(select_word1))
        #print(len(select_word2))
        # num_words+=num_word
    
    return nums

def dir_loop():

    countSli = []

    #遍历 指定目录下的文件夹和文件 第二个参数，为不遍历当前目录，从当前目录的子目录开始遍历
    # root 当前文件夹路径
    # dirs 内容是该文件夹中所有文件夹的名字
    # files 内容是该文件夹中所有的文件
    for root,dirs,files in os.walk(config.root,topdown=False): 
        files.sort()  # 对列表进行排序
        print(root)
        print(dirs)
        print(files)
        
        if len(dirs) == 0: # 无目录，最终级别
            wordDic = {}
            wordDic['dirName'] = os.path.basename(root)
            for file in files:
                if file[len(file)-3:] != 'txt': # 只处理txt的文档. 
                    continue
                fileYear = int(file[:4]) # 获取文档的年份
                if fileYear >config.date_range[1] or fileYear < config.date_range[0]: # 过滤不符合年份的数据
                    continue
                filePath = os.path.join(root+os.sep,file)
                num = word_freq(filePath)
                wordDic[fileYear] = num
            countSli.append(wordDic)
                
        # for name in files:
        #     print(name)

    columsIndex = ["dirName"] + list(range(config.date_range[0],config.date_range[1]+1))
    
    df=pd.DataFrame(data=countSli,columns=columsIndex)
    # 存储df
    writer=pd.ExcelWriter('.'+os.sep+'words_freq222.xlsx')
    df.to_excel(writer,index=False)
    writer.save()
    writer.close()

dir_loop()







