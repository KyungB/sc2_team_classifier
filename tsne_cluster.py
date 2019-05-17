from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import process as pc
import feature_convert as fc
from os import listdir
from os.path import isfile, join

def plot_tsne_cluster(k_data, title=""):
    model = TSNE(n_components=2,learning_rate=10)
    transformed = model.fit_transform(k_data[0])
    x_axis = transformed[:,0]
    y_axis = transformed[:,1]
    
    plt.figure(figsize=(20,10))
    plt.title("t-distributed Stochastic Neighbor Embedding Clustering ("+title+")")
    plt.scatter(x_axis,y_axis, s=1)
    plt.legend()
    plt.show()

onlyfiles_pe2 = [f for f in listdir('/media/ky/easystore/cil_reader_data/pe2/') 
                if isfile(join('/media/ky/easystore/cil_reader_data/pe2/', f))]

onlyfiles_sc2 = [f for f in listdir('/media/ky/easystore/cil_reader_data/scrimmage2/') 
                if isfile(join('/media/ky/easystore/cil_reader_data/scrimmage2/', f))]


#onlyfiles_pe2 = [f for f in listdir('E:/cil_reader_data/pe2/') 
#                if isfile(join('E:/cil_reader_data/pe2/', f))]

#k_gps = pc.cvt_opener_data(pc.opener_pe2_gps([i for i in onlyfiles_pe2 if 'Team' not in i]))
#k_dp = pc.cvt_opener_data(pc.opener_pe2_dp([i for i in onlyfiles_pe2 if 'Team' not in i]))
#k_voxel = pc.cvt_opener_data(pc.opener_pe2_voxel([i for i in onlyfiles_pe2 if 'Team' not in i]))

k_gps = pc.cvt_opener_data(pc.opener_sc2_gps([i for i in onlyfiles_sc2 if 'Team' not in i]))
k_dp = pc.cvt_opener_data(pc.opener_pe2_dp([i for i in onlyfiles_sc2 if 'Team' not in i]))
k_voxel = pc.cvt_opener_data(pc.opener_pe2_voxel([i for i in onlyfiles_sc2 if 'Team' not in i]))