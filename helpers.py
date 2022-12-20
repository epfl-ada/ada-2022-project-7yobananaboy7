import pandas as pd
import numpy as np
import urllib
import networkx as nx
import re

def load_data() :#Articles data
    articles = pd.read_csv("data/articles.tsv", skiprows=11, names=["article"])
    articles['article'] = articles['article'].apply(urllib.parse.unquote) #Parsing URL encoding

    #Category data
    categories = pd.read_csv("data/categories.tsv", sep="\t", skiprows=12, names=["article", "category"])
    categories["article"] = categories["article"].apply(urllib.parse.unquote) #Parsing URL encoding

    #Links data
    links = pd.read_csv("data/links.tsv", sep="\t", skiprows=11, names=["article", "link"])
    links["article"] = links["article"].apply(urllib.parse.unquote) #Parsing URL encoding
    links["link"] = links["link"].apply(urllib.parse.unquote) #Parsing URL encoding

    #Finished paths
    paths_finished = pd.read_csv("data/paths_finished.tsv", sep="\t", skiprows=15, names=["hashedIpAddress",
                                                                                          "timestamp",
                                                                                          "durationInSec",
                                                                                          "path",
                                                                                          "rating"])
    paths_finished["path"] = paths_finished["path"].apply(urllib.parse.unquote) #Parsing URL encoding

    #Unfinished paths
    paths_unfinished = pd.read_csv("data/paths_unfinished.tsv", sep="\t", skiprows=16, names=["hashedIpAddress",
                                                                                              "timestamp",
                                                                                              "durationInSec",
                                                                                              "path",
                                                                                              "target",
                                                                                              "type"])
    paths_unfinished["path"] = paths_unfinished["path"].apply(urllib.parse.unquote) #Parsing URL encoding
    paths_unfinished["target"] = paths_unfinished["target"].apply(urllib.parse.unquote) #Parsing URL encoding

    # Add the length of the paths
    paths_unfinished['pathLength'] = paths_unfinished['path'].apply(lambda x : len(str(x).split(';')))
    paths_finished['pathLength'] = paths_finished['path'].apply(lambda x : len(str(x).split(';')))

    #shortest path matrix
    with open('data/shortest-path-distance-matrix.txt', 'r') as file:

        #Initialize shortest_path_distance list
        shortest_path_distance = []

        for line in file:

            #Check if the first character of the line is either a digit or underscore
            if re.search("([0-9]|_)", line[0]): 

                #Append list to shortest_path_distance
                shortest_path_distance.append([np.nan if x=='_' else int(x) for x in line.strip()])

    #Convert to numpy ndarray
    shortest_path_distance = np.array(shortest_path_distance)    
    
    paths_finished['target'] = paths_finished['path'].apply(lambda x : str(x).split(';')[-1])

    #Add and remove (ir)relevant colums.
    paths_finished = paths_finished.copy()
    paths_unfinished = paths_unfinished.copy()
    paths_finished['type'] = 'finished'
    paths_finished = paths_finished.drop('rating',axis =1)
    
    paths_finished = paths_finished[paths_finished.pathLength >1]
    paths_unfinished = paths_unfinished[paths_unfinished.pathLength >1]

    #concatenate data
    paths_all = pd.concat([paths_finished, paths_unfinished]).reset_index().drop('index',axis = 1)
    
    return articles, categories, links, paths_finished, paths_unfinished, paths_all, shortest_path_distance

def get_graphs(paths_all, links):
    paths_all.insert(0, 'path_id',  paths_all.index)
    paths = paths_all[['path_id', 'path']].copy()
    paths = paths.explode('path').reset_index().rename(columns={'path': 'page', 'index' : 'page_index_in_path'})
    paths['page_index_in_path'] = paths.groupby('page_index_in_path').cumcount()
    paths.head()

    #Need to handle >
    start_edges = paths_all[['path_id', 'path']].copy()
    start_edges.loc[:,'path'] = start_edges['path'].apply(lambda x : str(x).split(';')[:-1])
    start_edges = start_edges.explode('path').reset_index().rename(columns={'path': 'start_edge', 'index' : 'page_index_in_path'})

    end_edges =  paths_all[['path_id', 'path']].copy()
    end_edges.loc[:,'path'] = end_edges['path'].apply(lambda x : str(x).split(';')[1:])
    end_edges = end_edges.explode('path').reset_index().rename(columns={'path': 'end_edge', 'index' : 'page_index_in_path'})

    edges = pd.concat([start_edges.start_edge, end_edges.end_edge],axis = 1)

    #Handle the '<' b dropping when the end edge is '<' and taking the previous start_edge when the start_edge is '<'
    edges = edges.drop(edges[edges.end_edge == '<'].index)
    while len(edges[(edges.start_edge == '<') ]) > 0 :
        edges['start_edge'] = np.where(edges['start_edge'] == '<', edges['start_edge'].shift(1), edges['start_edge'])

    #Group the same edge and give the weight 
    edges = edges.groupby(['start_edge', 'end_edge']).agg(len).reset_index().rename(columns  = {0 : 'weight'})
    
    G_paths = nx.from_pandas_edgelist(edges, 'start_edge', 'end_edge', 'weight', create_using = nx.DiGraph)
    G_links = nx.from_pandas_edgelist(links, 'article', 'link', create_using = nx.DiGraph)
    return G_paths, G_links

#Function to compute the geometric mean
def geo_mean(iterable):
    return np.exp(np.log(iterable).mean())

#Function for bootstrapping
def bootstrap_CI(data, nbr_draws, mean, with_means = False):
    means = np.zeros(nbr_draws)
    data = np.array(data)
    
    for n in range(nbr_draws):
        indices = np.random.randint(0, len(data), len(data))
        data_tmp = data[indices] 

        if mean == 'arithmetic':
            means[n] = np.nanmean(data_tmp)

        if mean == 'geometric':
            means[n] = geo_mean(data_tmp)

    if with_means :
        return [np.nanpercentile(means, 2.5),np.nanpercentile(means, 97.5)], means
    else : 
        return [np.nanpercentile(means, 2.5),np.nanpercentile(means, 97.5)]