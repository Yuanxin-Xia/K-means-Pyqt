from numpy import mat, nonzero ,mean
from numpy import float as f
import K_means


def run_and_draw(latituede,longtitude,k):
    datList=[]
        #解析文本数据中的每一行中的数据特征值
    for P in range(len(latituede)):
        datList.append([latituede[P],longtitude[P]])
        datMat=mat(datList)


    myCentroids,clusterAssing= K_means.biKmeans(datMat, k)

    LA = mean(latituede)
    LO = mean(longtitude)

    center = []
    other = []
    # 添加聚类中点
    for h, l in zip(myCentroids[:, 0].flatten().A[0], myCentroids[:, 1].flatten().A[0]):  # 解包操作
        center.append([f(h), f(l)])

    for m in range(k):

        # 添加城市点
        ptsInCurrCluster = datMat[nonzero(clusterAssing[:, 0].A == m)[0], :]
        for i, j in zip(ptsInCurrCluster[:, 0].flatten().A[0], ptsInCurrCluster[:, 1].flatten().A[0]):  # 解包操作
            other.append([f(i), f(j), m])
    print('[INFO]: 景点聚类完成')
    return center,other,LO,LA