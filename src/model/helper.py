
from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list, to_tree, centroid, cut_tree
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA,KernelPCA
from sklearn.manifold import TSNE
import pandas as pd

def compute_kmeans(X, title = "",no_clusters=3):
    """Compute K means of 3 groups by default"""
    kmeans = KMeans(n_clusters=no_clusters)
    res = kmeans.fit(X)
    #print(f"res: \n {res}")
    plt.figure(figsize=(40,40),dpi= 600, facecolor='white')
    classes = kmeans.predict(X)
    #print(f"classes: {classes}")
    plt.scatter(X[:, 0], X[:, 1], c=classes)
    plt.title(title)
    plt.show()
    plt.savefig(f'Diagrams/{title}.png')
    # return classes



def plot_tsne(matrix,titles_list,title="", metric = "cosine", perplexity = 60):
    """Reduces matrix to 2 dimensions using TSNE and plots it"""
    reduced_matrix =TSNE(n_components=2,init='TruncatedSVD',method='exact',perplexity=perplexity, metric = metric).fit_transform(matrix)
    axes =reduced_matrix.T

    plt.figure(figsize=(20,20),dpi= 600, facecolor='white')
    axis1 =axes[0].tolist()
    axis2 =axes[1].tolist()
    plt.scatter(axis1,axis2)
    for i,label in enumerate(titles_list):
        plt.annotate(label, (axis1[i], axis2[i]))
    plt.title(title)
    plt.savefig(f'Diagrams/{title}.png')
    return reduced_matrix

def plot_kpca(matrix,titles_list, kernel="linear",title=""):
    """Reduces matrix to 2 dimensions using PCA and plots it
    kernel choices: {‘linear’, ‘poly’, ‘rbf’, ‘sigmoid’, ‘cosine’, ‘precomputed’}
    """
    np.matrix(matrix)
    pca = KernelPCA(n_components=2,kernel=kernel)
    reduced_matrix=pca.fit_transform(matrix)
    print(f"shape reduced matrix: {np.shape(reduced_matrix)}")
    
    axes =reduced_matrix.T

    plt.figure(figsize=(20,20),dpi= 600, facecolor='white')
    axis1 =axes[0].tolist()
    axis2 =axes[1].tolist()
    plt.scatter(axis1,axis2)
    for i,label in enumerate(titles_list):
        plt.annotate(label, (axis1[i], axis2[i]))
    plt.title(title)
    plt.savefig(f'Diagrams/{title}.png')
    return reduced_matrix

def plot_dendrogram(matrix,titles_list = None,  hierarchy_method = "complete",dist_metric = "cos", title= ""):
    """Plots dendro gram given matrix with parameters for the linkage
    labels: name labels on the dendrogram tree"""
    out = linkage(matrix, method = hierarchy_method, metric = dist_metric)
    plt.figure(figsize=(96, 36) ,dpi= 400, facecolor='white')
    plt.title(title)
    dn = dendrogram(out, labels = titles_list)
    plt.show()
    plt.savefig(f'Diagrams/{title}.png')
    
def plot_pca(matrix,titles_list = None,title=""):
    """Reduces matrix to 2 dimensions using PCA and plots it along with the screeplot
    output: 
    reduced_matrix: 2 x m matrix"""
    matrix = np.matrix(matrix)
    pca = PCA(n_components=2)
    reduced_matrix=pca.fit_transform(matrix)
    print(f"shape reduced matrix: {np.shape(reduced_matrix)}")
    print(f"pca.explained_variance_ratio_: {pca.explained_variance_ratio_}")
    transpose =reduced_matrix.T
    axis1 =transpose[0].tolist()
    axis2 =transpose[1].tolist()
    fig, axes = plt.subplots(2,1, figsize=(10, 10), dpi= 1200, facecolor='white')
    
    axes[0].scatter(axis1,axis2)
    for i,label in enumerate(titles_list):
        axes[0].annotate(label, (axis1[i], axis2[i]))
    axes[0].set_title(title)
    components = np.arange(pca.n_components_) + 1
    
    axes[1].plot(components, pca.explained_variance_ratio_, 'o-')
    axes[1].set_title(f"Scree plot of {title}")
    fig.savefig(f'Diagrams/{title}.png')
    return reduced_matrix

def heat_map(leaves_list,titles_list,matrix):
    """Prints heat map where rows are ordered by the clustering algorithm,
    columns are still chains list ordered"""
    rows = [titles_list[i] for i in leaves_list]
    ordered_mat = [matrix[i] for i in leaves_list]
    #print(f"rows: {rows}, chains_list {chains_list}")
    heat_frame = pd.DataFrame(ordered_mat,rows,titles_list)
    print(f"starting heat function 2")
    #f, ax = plt.subplots(figsize=(11, 9))
    #cmap = sns.diverging_palette(230, 20, as_cmap=True)
    plt.figure(figsize=(1000,1000))
    plt.xticks(range(len(titles_list)),titles_list,rotation=90)
    plt.yticks(range(len(rows)),rows)
    plt.imshow(heat_frame, cmap='hot',interpolation="nearest")