from numpy import sin
from numpy import arccos, cos, pi, seterr, shape, zeros, mat, inf, nonzero, mean
from numpy.random import rand

def distSLC(vecA,vecB):
    #sin()和cos()以弧度未输入，将float角度数值转为弧度，即*pi/180
    a=sin(vecA[0,1]*pi/180)*sin(vecB[0,1]*pi/180)
    b=cos(vecA[0,1]*pi/180)*cos(vecB[0,1]*pi/180)*\
        cos(pi*(vecB[0,0]-vecA[0,0])/180)
    seterr(divide='ignore', invalid='ignore')
    value = arccos(a + b) * 6371.0
    return value

# 随机初始化K个质心(质心满足数据边界之内)
def randCent(dataSet, k):
    # 得到数据样本的维度
    n = shape(dataSet)[1]  # 返回特征数目 2
    # 初始化为一个(k,n)的矩阵
    centroids = mat(zeros((k, n)))  # 创建一个 k x n 列的矩阵 存储质心
    # 遍历数据集的每一维度
    for j in range(n):
        # 得到该列数据的最小值
        minJ = min(dataSet[:, j])
        # 得到该列数据的范围(最大值-最小值)
        rangeJ = float(max(dataSet[:, j]) - minJ)
        # k个质心向量的第j维数据值随机为位于(最小值，最大值)内的某一值
        centroids[:, j] = minJ + rangeJ * rand(k, 1)
    # 返回初始化得到的k个质心向量
    return centroids
 
 
""" k-均值聚类算法"""
def kMeans(dataSet, k, distMeans=distSLC, createCent=randCent):
    """
    @dataSet:聚类数据集
    @k:用户指定的k个类
    @distMeas:距离计算方法，默认欧氏距离distSLC()
    @createCent:获得k个质心的方法，默认随机获取randCent()
    """
    m = shape(dataSet)[0]  # 返回样本数目 80
    clusterAssment = mat(zeros((m, 2)))  # 创建一个 m x 2 列的矩阵 初始化元素为0
    centroids = createCent(dataSet, k)  # 创建初始的k个质心向量
    clusterChanged = True  # 聚类结果是否发生变化的布尔类型
    while clusterChanged:
        # 聚类结果变化布尔类型置为false
        clusterChanged = False
        # 遍历数据集每一个样本向量
        for i in range(m):
            # 初始化最小距离最正无穷；最小距离对应索引为-1
            minDist = inf
            minIndex = -1
            # 循环k个类的质心
            for j in range(k):
                # 计算某个数据点到k个质心的欧氏距离 （得出最近的那个质心的索引和距离值 填充到 矩阵中 便于统计k的质心位置）
                distJI = distMeans(centroids[j, :], dataSet[i, :])
                # 如果距离小于当前最小距离
                if distJI < minDist:
                    # 当前距离定为当前最小距离；最小距离对应索引对应为j(第j个类)
                    minDist = distJI
                    minIndex = j
            # 当前聚类结果中第i个样本的聚类结果发生变化：布尔类型置为true，继续聚类算法
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            # 更新当前变化样本的聚类结果和平方误差
            clusterAssment[i, :] = minIndex, minDist ** 2
        # 打印k-均值聚类的质心
        #print(centroids)
        # 遍历每一个质心
        for cent in range(k):
            # 将数据集中所有属于当前质心类的样本通过条件过滤筛选出来
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
            if len(ptsInClust) != 0:
            # 计算这些数据的均值（axis=0：求列的均值），作为该类质心向量
                centroids[cent, :] = mean(ptsInClust, axis=0)
        # 返回k个聚类，聚类结果及误差
    return centroids, clusterAssment
 
 
def biKmeans(dataSet, k, distMeas=distSLC):
    m = shape(dataSet)[0] # 样本数目
    clusterAssment = mat(zeros((m, 2))) # m x 2 列的矩阵 用来存储每个样本镞系数和误差值
    centroid0 = mean(dataSet, axis=0).tolist()[0] # 获取各列的均值
    centList = [centroid0] # 存储镞质心
    for j in range(m):  # 遍历每个数据样本 返回每个样本到指定镞中心的距离值
        clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2#计算当前聚为一类时各个数据点距离质心的平方距离
    while (len(centList) < k):#循环，直至二分k-均值达到k类为止
        lowestSSE = inf # 将当前最小平方误差置为正无穷
        for i in range(len(centList)):#遍历当前每个聚类
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == i)[0], :]  # 通过数组过滤筛选出属于第i类的数据集合
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)# 对该类利用二分k-均值算法进行划分，返回划分后结果，及误差
            sseSplit = sum(splitClustAss[:, 1])  # 计算该类划分后两个类的误差平方和
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != i)[0], 1])# 计算数据集中不属于该类的数据的误差平方和
            if (sseSplit + sseNotSplit) < lowestSSE:#划分第i类后总误差小于当前最小总误差
                bestCentToSplit = i #第i类作为本次划分类
                bestNewCents = centroidMat#第i类划分后得到的两个质心向量
                bestClustAss = splitClustAss.copy()#复制第i类中数据点的聚类结果即误差值
                lowestSSE = sseSplit + sseNotSplit#将划分第i类后的总误差作为当前最小误差
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList) #数组过滤筛选出本次2-均值聚类划分后类编号为1数据点，将这些数据点类编号变为 当前类个数+1，作为新的一个聚类
        # 同理，将划分数据集中类编号为0的数据点的类编号仍置为被划分的类编号，使类编号
        # 连续不出现空缺
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        centList[bestCentToSplit] = bestNewCents[0, :].tolist()[0]  #更新质心列表中的变化后的质心向量
        centList.append(bestNewCents[1, :].tolist()[0])#添加新的类的质心向量
        #更新clusterAssment列表中参与2-均值聚类数据点变化后的分类编号，及数据该类的误差平方
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return mat(centList), clusterAssment#返回聚类结果