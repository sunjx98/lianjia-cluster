import pandas as pd
import numpy as np
import os
import lianjia
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from scipy.cluster import hierarchy
from itertools import cycle

def check_file(filename):
    if os.path.exists(filename):
        print('------数据文件已存在------')
        house_data = pd.read_csv(filename, encoding = 'gbk', sep = ',')
        return house_data
    else:
        print('------文件不存在，运行爬虫程序对信息进行爬取------')
        lianjia.main()
        house_data = pd.read_csv(filename, encoding = 'gbk', sep= ',')
        return house_data
def data_info(data_set):
    print('-----数据集基本信息-----')
    data_set.info()
    print('-----预览数据-----\n',data_set.head())
def data_adj(area_data, str):
    if str in area_data :
        return float(area_data[0 : area_data.find(str)])
    else :
        return None
def main():
    filename = '/Users/sunnnjx/Desktop/house_data.csv'
    house_data = check_file(filename)
    data_info(house_data)
    house_data['area_adj'] = house_data['house_area'].apply(data_adj, str='平米')
    house_data['interest_adj'] = house_data['house_interest'].apply(data_adj, str='人关注')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    fig, ax1 = plt.subplots(1, 1)
    type_interest_group = house_data['interest_adj'].groupby(house_data['house_type']).agg([('户型', 'count'), ('关注人数', 'sum')])
    ti_sort = type_interest_group[type_interest_group['户型'] > 50].sort_values(by='户型')
    ti_sort.plot(kind='barh', alpha=0.7, grid=True, ax=ax1)
    plt.title('二手房户型和关注人数分布')
    plt.ylabel('户型')
    plt.show()
    fig, ax2 = plt.subplots(1,1)
    area_level = [0, 50, 100, 150, 200, 250, 300, 500]
    label_level = ['小于50', '50-100', '100-150', '150-200', '200-250', '250-300', '300-350']
    area_cut = pd.cut(house_data['area_adj'], area_level, labels=label_level)
    area_cut.value_counts().plot(kind='bar', rot=30, alpha=0.4, grid=True, fontsize='small', ax=ax2)
    plt.title('二手房面积分布')
    plt.xlabel('面积')
    plt.legend(['数量'])
    plt.show()

    plt.figure(1)
    plt.clf()
    plt.scatter(house_data['area_adj'], house_data['interest_adj'], c='b', linewidths=0.01)
    plt.xlabel('面积/平米')
    plt.ylabel('关注人数/人')
    plt.show()
    #Kmeans聚类
    kmeans_n_clusters=3
    cluster_data = house_data[['interest_adj', 'area_adj']].dropna()
    cluster_data0=np.array(cluster_data)
    kmeans_clusterer=KMeans(n_clusters=kmeans_n_clusters, init='random',n_init=1)
    kmeans_clusterer.fit(cluster_data0)
    kmeans_cluster_label=kmeans_clusterer.labels_
    kmeans_cluster_center=kmeans_clusterer.cluster_centers_
    plt.figure(2)
    plt.clf()
    colours=['g','r','b','y','c']
    class_label=['Class 1','Class 2','Class 3','center']
    for i in range(kmeans_n_clusters):
        kmeans_members=kmeans_cluster_label==i
        plt.scatter(cluster_data0[kmeans_members,0], cluster_data0[kmeans_members,1], s=30, c=colours[i], marker='.')
    plt.title('KMeans clustering result')
    plt.xlabel('面积/平米')
    plt.ylabel('关注/人')
    for i in range(kmeans_n_clusters):
        plt.scatter(kmeans_cluster_center[i][0], kmeans_cluster_center[i][1], marker='p', c='k', linewidths=0.4)
    plt.legend(class_label,loc=0)
    plt.show()
    plt.clf()
    inertia_Je = []
    k = []
    for n_clusters in range(1, 10):
        cls = KMeans(n_clusters).fit(cluster_data0)
        inertia_Je.append(cls.inertia_)
        k.append(n_clusters)
    plt.scatter(k, inertia_Je)
    plt.plot(k, inertia_Je)
    plt.xlabel("k")
    plt.ylabel("Je")
    plt.show()
    #分层聚类
    linkages = ['ward', 'average', 'complete', 'single', 'average,' 'weighted', 'centroid']
    hierarchical_n_clusters = 3
    Z = hierarchy.linkage(cluster_data0, method='ward', metric='euclidean')
    hierarchy.dendrogram(Z)
    plt.savefig('plot_dendrogram.png')
    label=hierarchy.cut_tree(Z,height=200)
    label=label.reshape(label.size,)
    class_label = ['Class 1', 'Class 2', 'Class 3', 'center']
    plt.figure(3)
    plt.clf()
    colours=cycle('bgrcmyk')
    for k, col in zip(range(hierarchical_n_clusters), colours):
        hierarchical_members= label==k
        plt.plot(cluster_data0[hierarchical_members,0],cluster_data0[hierarchical_members,1], col + '.')
    plt.legend(class_label,loc=0)
    plt.title('Hierarchical clustering result')
    plt.xlabel('面积/平米')
    plt.ylabel('关注人数/人')
    plt.show()
if __name__ == '__main__':
    main()