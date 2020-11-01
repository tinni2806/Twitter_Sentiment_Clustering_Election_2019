import os, collections
import numpy as np
from sklearn import cluster

path_to_data = "/Twitter_Sentiment_Clustering_Election_2019/data/"
path_to_results = "/Twitter_Sentiment_Clustering_Election_2019/results/"

if __name__ == '__main__':
    seed = 1536488
    np.random.seed(seed)

    for filename in sorted(os.listdir(path_to_data+"processed/")):
        print("Clustering: "+ filename)
        data = np.genfromtxt(path_to_data+"processed/"+filename, delimiter=',')
        sample_size = 10000
        sample = data[np.random.randint(len(data),size=sample_size),:]
        birch = cluster.Birch(branching_factor=5, n_clusters=None, threshold=0.25, compute_labels=True).fit(sample)
        labels = birch.labels_
        sample = np.c_[sample, labels]
        os.makedirs(os.path.dirname(path_to_results+"clustered_"+filename), exist_ok=True)
        np.savetxt(path_to_results+"clustered_"+filename, sample, fmt='%.5f', delimiter=",")
        counts = collections.Counter(labels)
        centroids = birch.subcluster_centers_
        print("Clusters: label, X, Y, Size\n")
        for i in counts.most_common(len(counts)):
            print(i[0], " , ", centroids[i[0]][1], " , ", centroids[i[0]][0], " , ", counts[i[0]] )
        print("\nClustered File: clustered_"+filename,"\n")
