from math import log
import operator
# import matplotlib.pyplot as plt
import pandas as pd
def createDataSet():
    dataSet = [[1,1,1,'yes'],
               [1,0,1,'yes'],
               [1,0,0,'no'],
               [0,1,0,'yes'],
               [0,0,1,'no'],
               [0,1,1,'yes']]
    labels = ['asset','kindness','appearance']
    return dataSet, labels
def createDataSet1():
    dataSet = pd.read_csv('data.csv')
    dataSet = dataSet.values.tolist()
    labels = ['buying','maint','doors','persons','lug_boot','safety']
    return dataSet, labels
dataSet, dataLabels = createDataSet1()

#计算香农熵
def calcShannonEnt(dataSet):
    #样本总个数
    totalNum = len(dataSet)
    #类别集合
    labelSet = {}
    #计算每个类别的样本个数
    for dataVec in dataSet:
        label = dataVec[-1]
        if label not in labelSet.keys():
            labelSet[label] = 0
        labelSet[label] += 1
    shannonEnt = 0
    #计算熵值
    for key in labelSet:
        pi = float(labelSet[key])/totalNum
        shannonEnt -= pi*log(pi,2)
    return shannonEnt

print("样本熵值：%f" % calcShannonEnt(dataSet))

def splitDataSet(dataSet, featNum, featvalue):
    retDataSet = []
    for dataVec in dataSet:
        if dataVec[featNum] == featvalue:
            splitData = dataVec[:featNum]
            splitData.extend(dataVec[featNum+1:])
            retDataSet.append(splitData)
    return retDataSet

#选择最好的特征划分数据集
def chooseBestFeatToSplit(dataSet):
    featNum = len(dataSet[0]) - 1
    maxInfoGain = 0
    bestFeat = -1
    #计算样本熵值，对应公式中：H(X)
    baseShanno = calcShannonEnt(dataSet)
    #以每一个特征进行分类，找出使信息增益最大的特征
    for i in range(featNum):
        featList = [dataVec[i] for dataVec in dataSet]
        featList = set(featList)
        newShanno = 0
        #计算以第i个特征进行分类后的熵值，对应公式中：H(X|Y)
        for featValue in featList:
            subDataSet = splitDataSet(dataSet, i, featValue)
            prob = len(subDataSet)/float(len(dataSet))
            newShanno += prob*calcShannonEnt(subDataSet)
        #ID3算法：计算信息增益,对应公式中：g(X,Y)=H(X)-H(X|Y)
        infoGain = baseShanno - newShanno
        #C4.5算法：计算信息增益比
        #infoGain = (baseShanno - newShanno)/baseShanno
        #找出最大的熵值以及其对应的特征
        if infoGain > maxInfoGain:
            maxInfoGain = infoGain
            bestFeat = i
    return bestFeat

#如果决策树递归生成完毕，且叶子节点中样本不是属于同一类，则以少数服从多数原则确定该叶子节点类别
def majorityCnt(labelList):
    labelSet = {}
    #统计每个类别的样本个数
    for label in labelList:
        if label not in labelSet.keys():
            labelSet[label] = 0
        labelSet[label] += 1
    #iteritems：返回列表迭代器
    #operator.itemgeter(1):获取对象第一个域的值
    #True：降序
    sortedLabelSet = sorted(labelSet.items(), key=operator.itemgetter(1), reverse=True)
    return sortedLabelSet[0][0]

def createDecideTree(dataSet, featName):
    #数据集的分类类别
    classList = [dataVec[-1] for dataVec in dataSet]
    #所有样本属于同一类时，停止划分，返回该类别
    if len(classList) == classList.count(classList[0]):
        return classList[0]
    #所有特征已经遍历完，停止划分，返回样本数最多的类别
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    #选择最好的特征进行划分
    bestFeat = chooseBestFeatToSplit(dataSet)
    beatFestName = featName[bestFeat]
    del featName[bestFeat]
    #以字典形式表示树
    DTree = {beatFestName:{}}
    #根据选择的特征，遍历该特征的所有属性值，在每个划分子集上递归调用createDecideTree
    featValue = [dataVec[bestFeat] for dataVec in dataSet]
    featValue = set(featValue)
    for value in featValue:
        subFeatName = featName[:]
        DTree[beatFestName][value] = createDecideTree(splitDataSet(dataSet,bestFeat,value), subFeatName)
    return DTree

tree = createDecideTree(dataSet,dataLabels)
print(tree)

#获取决策树叶节点个数
# def getNumLeafs(tree):
#     numLeafs = 0
#     #获取第一个节点的分类特征
#     firstFeat = list(tree.keys())[0]
#     #得到firstFeat特征下的决策树（以字典方式表示）
#     secondDict = tree[firstFeat]
#     #遍历firstFeat下的每个节点
#     for key in secondDict.keys():
#         #如果节点类型为字典，说明该节点下仍然是一棵树，此时递归调用getNumLeafs
#         if type(secondDict[key]).__name__== 'dict':
#             numLeafs += getNumLeafs(secondDict[key])
#         #否则该节点为叶节点
#         else:
#             numLeafs += 1
#     return numLeafs

# #获取决策树深度
# def getTreeDepth(tree):
#     maxDepth = 0
#     #获取第一个节点分类特征
#     firstFeat = list(tree.keys())[0]
#     #得到firstFeat特征下的决策树（以字典方式表示）
#     secondDict = tree[firstFeat]
#     #遍历firstFeat下的每个节点，返回子树中的最大深度
#     for key in secondDict.keys():
#         #如果节点类型为字典，说明该节点下仍然是一棵树，此时递归调用getTreeDepth，获取该子树深度
#         if type(secondDict[key]).__name__ == 'dict':
#             thisDepth = 1 + getTreeDepth(secondDict[key])
#         else:
#             thisDepth = 1
#         if thisDepth > maxDepth:
#             maxDepth = thisDepth
#     return maxDepth    

# print(getTreeDepth(tree))
# print(getNumLeafs(tree))

# def createPlot(tree):
#     #定义一块画布，背景为白色
#     fig = plt.figure(1, facecolor='white')
#     #清空画布
#     fig.clf()
#     #不显示x、y轴刻度
#     xyticks = dict(xticks=[],yticks=[])
#     #frameon：是否绘制坐标轴矩形
#     createPlot.pTree = plt.subplot(111, frameon=False, **xyticks)
#     #计算决策树叶子节点个数
#     plotTree.totalW = float(getNumLeafs(tree))
#     #计算决策树深度
#     plotTree.totalD = float(getTreeDepth(tree))
#     #最近绘制的叶子节点的x坐标
#     plotTree.xOff = -0.5/plotTree.totalW
#     #当前绘制的深度：y坐标
#     plotTree.yOff = 1.0
#     #（0.5,1.0）为根节点坐标
#     plotTree(tree,(0.5,1.0),'')
#     plt.show()

# #定义决策节点以及叶子节点属性：boxstyle表示文本框类型，sawtooth：锯齿形；fc表示边框线粗细
# decisionNode = dict(boxstyle="square", fc="0.5")
# leafNode = dict(boxstyle="round", fc="0.5")
# #定义箭头属性
# arrow_args = dict(arrowstyle="<|-")

# #nodeText:要显示的文本；centerPt：文本中心点，即箭头所在的点；parentPt：指向文本的点；nodeType:节点属性
# #ha='center'，va='center':水平、垂直方向中心对齐；bbox：方框属性
# #arrowprops：箭头属性
# #xycoords，textcoords选择坐标系；axes fraction-->0,0是轴域左下角，1,1是右上角
# def plotNode(nodeText, centerPt, parentPt, nodeType):
#     createPlot.pTree.annotate(nodeText, xy=parentPt, xycoords="axes fraction",
#                             xytext=centerPt, textcoords='axes fraction',
#                             va='center',ha='center',bbox=nodeType, arrowprops=arrow_args)

# def plotMidText(centerPt,parentPt,midText):
#     xMid = (parentPt[0] - centerPt[0])/2.0 + centerPt[0]
#     yMid = (parentPt[1] - centerPt[1])/2.0 + centerPt[1]
#     createPlot.pTree.text(xMid, yMid, midText)

# def plotTree(tree, parentPt, nodeTxt):
#     #计算叶子节点个数
#     numLeafs = getNumLeafs(tree)
#     #获取第一个节点特征
#     firstFeat = list(tree.keys())[0]
#     #计算当前节点的x坐标
#     centerPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
#     #绘制当前节点
#     plotMidText(centerPt,parentPt,nodeTxt)
#     plotNode(firstFeat,centerPt,parentPt,decisionNode)
#     secondDict = tree[firstFeat]
#     #计算绘制深度
#     plotTree.yOff -= 1.0/plotTree.totalD
#     for key in secondDict.keys():
#         #如果当前节点的子节点不是叶子节点，则递归
#         if type(secondDict[key]).__name__ == 'dict':
#             plotTree(secondDict[key],centerPt,str(key))
#         #如果当前节点的子节点是叶子节点，则绘制该叶节点
#         else:
#             #plotTree.xOff在绘制叶节点坐标的时候才会发生改变
#             plotTree.xOff += 1.0/plotTree.totalW
#             plotNode(secondDict[key], (plotTree.xOff,plotTree.yOff),centerPt,leafNode)
#             plotMidText((plotTree.xOff,plotTree.yOff),centerPt,str(key))
#     plotTree.yOff += 1.0/plotTree.totalD


# createPlot(tree)