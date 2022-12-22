import pandas as pd
import numpy as np
import urllib
import networkx as nx
import re

def load_data() :#Articles data
    """Load the data of Wikispedia 
    Return:
        a tuple with the files parsed 
            articles : the content of each pages, 
            categories : the categories associated to each page, 
            links : the hyperlinks that links two pages in wikipedia, 
            paths_finished : all the games of Wikispedia that were finished with length bigger than one, 
            paths_unfinished : all the games of Wikispedia that were finished with length bigger than one,
            paths_all : the concatenation of paths_finished and paths_unfinished, 
            shortest_path_distance : the shortest path distance between all pages
    """
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
    """ Construct the players and the wikipedia graph.
    Args:
        paths_all : all the paths of the Wikispeedia games
        links : the wikipedia hyperlinks between pages 
    Return:
        a tuple with two graphs 
            G_paths : the graph generated from the paths the players used, 
            G_links : the graph generated from the hyperlinks present in Wikipedia
    """
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
  

def geo_mean(iterable):
    """ compute the geometric mean
    Args:
        iterable : the iterable we want to get the geometric mean from 
    Return:
        the geometric mean
    """
    return np.exp(np.log(iterable).mean())


def bootstrap_CI(data, nbr_draws, mean, with_means = False):
    """ compute the 95% confidence interval for the given mean 
    Args:
        data : the data we want the mean from, 
        nbr_draws : the numer of draws done for the boostraping, 
        mean : the type of mean we want to use. 'geometric' or 'arithmetic', 
        with_means = False : returns the means associated to the CI
    Return:
        the geometric mean
    """
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
    
    
##############################################
#### helpers for cluster with categories #####
##############################################

def get_in_out_degree(G, page) :
    """ Return the in and out degree of page in a given graph
    Args:
        G : the netwrokx graph
        page : a wikipedia page
    Return:
        an array with indegree and outdegree of the page in the graph
    """
    in_deg = G.in_degree(page, 'weight')
    in_deg = in_deg if in_deg else 0
    out_deg = G.out_degree(page, 'weight')
    out_deg = out_deg if out_deg else 0
    return [in_deg, out_deg]

def add_in_out_deg(cat, G):
    """ add the in and out degree to the df cat
    Args:
        cat : a df of categories, 
        G : a networkx graph
    Return:
        the categories with the in and out degree added


    """
    cat['in_deg'] = cat.article.apply(
        lambda art: get_in_out_degree(G, art)[0])
    cat['out_deg'] = cat.article.apply(
        lambda art: get_in_out_degree(G, art)[1])
    cat['mean_in_out_deg'] = (cat['in_deg']+cat['out_deg'])/2
    return cat

def split_cat(cat):
    """ Take the categories in an array format rather than a string separated by '.'
    Args:
        cat : a df of categories, 
    Return:
        the df with the categories splitted 
        
    """
    cat['splitted_cat'] = cat.category.apply(lambda x : x.split('.')[1:])
    return cat

def get_sum_in_out_by_cat(cat):
    """ Returns the sum of degree for each categories
    Args:
        cat : a df of categories, 
    Return:
        the df with the grouped categories and their in and out deg    
    """
    cat = cat.explode('splitted_cat')
    cat = cat.groupby('splitted_cat').apply(lambda x : pd.Series({
        'sum_in_deg' : x.in_deg.sum(),
        'sum_out_deg' : x.out_deg.sum(),
        'sum_mean_in_out_deg' : x.mean_in_out_deg.sum() 
    }))
    return cat

def get_cat_summary(cat, G):
    """ get a summary of each categories and how many times they appear in a graph 
    Args:
        cat : the df with the categories
        G : a networx graph
    Return:
        a summary of the categories
    """
    cat = add_in_out_deg(cat, G)
    cat = split_cat(cat)
    cat = get_sum_in_out_by_cat(cat)
    return cat

def get_all_features_of_categories(categories, G_paths_finished, G_paths_unfinished, nb_finished_node_visited, nb_unfinished_node_visited):
    """  get all the stats necessary for the analysis
    Args:
        categories : the categories, 
        G_paths_finished : the players graph with only the finished paths, 
        G_paths_unfinished: the players graph with only the unfinished paths, 
        nb_finished_node_visited : the number sum of in degree in finished graph, 
        nb_unfinished_node_visited: the number sum of in degree in unfinished graph
    Return:
        the categrories with all the stats necessary for the analysis
    """
    categories_finished = categories.copy()
    categories_unfinished = categories.copy()

    categories_finished= get_cat_summary(categories_finished, G_paths_finished)
    categories_unfinished= get_cat_summary(categories_unfinished, G_paths_unfinished)

    # Divide the sums by the number of node and multiply by 1000 so that it is easier to read
    categories_finished = categories_finished/nb_finished_node_visited*1000
    categories_unfinished = categories_unfinished/nb_unfinished_node_visited*1000

    categories_finished = categories_finished.rename(columns = {'sum_in_deg'  : 'frac_in_deg_finished',
                                                    'sum_out_deg' : 'frac_out_deg_finished',
                                                    'sum_mean_in_out_deg' : 'frac_mean_in_out_deg_finished'})
    categories_unfinished = categories_unfinished.rename(columns ={'sum_in_deg'  : 'frac_in_deg_unfinished',
                                                    'sum_out_deg' : 'frac_out_deg_unfinished',
                                                    'sum_mean_in_out_deg' : 'frac_mean_in_out_deg_unfinished'})

    #We join all the categories
    categories_all = categories_finished.join(categories_unfinished)

    # compute differences bwtween frequency of used in finished and unfinished paths using mean degree 
    categories_all['diff_in'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_in_deg_unfinished) , axis = 1)
    categories_all['diff_out'] = categories_all.apply(lambda x: 
                (x.frac_out_deg_finished - x.frac_out_deg_unfinished), axis = 1)
    categories_all['diff_mean_in_out'] = categories_all.apply(lambda x: 
                (x.frac_mean_in_out_deg_finished - x.frac_mean_in_out_deg_unfinished), axis = 1)
    categories_all['weighted_diff_in'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_in_deg_unfinished) /(x.frac_in_deg_finished + x.frac_in_deg_unfinished), axis = 1)
    categories_all['weighted_diff_out'] = categories_all.apply(lambda x: 
                (x.frac_out_deg_finished - x.frac_out_deg_unfinished) /(x.frac_out_deg_finished + x.frac_out_deg_unfinished), axis = 1)
    categories_all['weighted_diff_mean_in_out'] = categories_all.apply(lambda x: 
                (x.frac_mean_in_out_deg_finished - x.frac_mean_in_out_deg_unfinished)/(x.frac_mean_in_out_deg_finished + x.frac_mean_in_out_deg_unfinished), axis = 1)
    categories_all['frac_finished_for_degree'] = categories_all.apply(lambda x: 
                (x.frac_mean_in_out_deg_finished)/(x.frac_mean_in_out_deg_finished + x.frac_mean_in_out_deg_unfinished), axis = 1)
    
    # compute differences bwtween in and out degree for finished and unfinished paths 
    categories_all['diff_finished'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_out_deg_finished) , axis = 1)
    categories_all['diff_unfinished'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_out_deg_unfinished), axis = 1)
    categories_all['weighted_diff_finished'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_out_deg_finished)/(x.frac_in_deg_finished + x.frac_out_deg_finished) , axis = 1)
    categories_all['weighted_diff_unfinished'] = categories_all.apply(lambda x: 
                (x.frac_in_deg_finished - x.frac_out_deg_unfinished)/(x.frac_in_deg_finished + x.frac_out_deg_finished), axis = 1)
    
    return categories_all

def get_score(article, attribute, categories_merged_2, start_target_cats):
    """  Give the score of a specific attribute of a given paths for paths 
    Args:
        article : a Wikipeedia article, 
        attribute : an attribute with a score, 
        categories_merged_2 : a df with all the article and their corresponding categories, 
        start_target_cats : a df with the categories of the starting and target points
    Return:
        the categrories with all the stats necessary for the analysis
    """
    if article not in categories_merged_2.index :
        return 0.5
    arr = [start_target_cats.loc[cat][attribute] for cat in categories_merged_2.loc[article].categories ]
    return sum(arr)/len(arr)

def get_categories(article, df):
    """  Get the categories of the article
    Args:
        article : a Wikipeedia article, 
        df : the df with the article and their categories
    Return:
        the categrories of an article if it exists. [] otherwise
    """
    if article not in df.index :
        return [] 
    else : 
        return df.loc[article].categories

def get_start_target_cats_from_paths(paths, categories_merged):
    """  Get the starting and target pages categories of all the paths
    Args:
        paths : all the paths done by players
        categories_merged : all the article with their possibly multiple categories
    Return:
        a df with all the categories of the starting and target pages
    """
    paths['start'] = paths.path.apply(lambda x:x.split(';')[0])
    paths['start_cats'] = paths['start'].apply(lambda article : get_categories(article, categories_merged))
    paths['target_cats'] = paths['target'].apply(lambda article : get_categories(article, categories_merged))
    paths_start = paths.explode('start_cats').groupby('start_cats').start.agg(len)
    paths_target = paths.explode('target_cats').groupby('target_cats').target.agg(len)
    paths_out = pd.merge(paths_start, paths_target, right_index=True, left_index=True)
    return paths_out

def get_start_target_cats(paths_unfinished, paths_finished, categories_merged, nb_finished_node_visited, nb_unfinished_node_visited):
    """  Get all the categories of the starting and target pages of paths and their statistics 
    Args:
        Args:
        paths_finished : the players games with only the finished paths, 
        paths_unfinished: the players games with only the unfinished paths, 
        categories_merged : the categories, 
        nb_finished_node_visited : the number sum of in degree in finished graph, 
        nb_unfinished_node_visited: the number sum of in degree in unfinished graph
    Return:
        a df with all the categories of the starting and target pages of paths and their statistics 
    """
    start_target_cats_unfinished = get_start_target_cats_from_paths(paths_unfinished[['path', 'target']].copy(), categories_merged)
    start_target_cats_finished = get_start_target_cats_from_paths(paths_finished[['path', 'target']].copy(), categories_merged)
    start_target_cats_finished = start_target_cats_finished/nb_finished_node_visited*1000
    start_target_cats_unfinished = start_target_cats_unfinished/nb_unfinished_node_visited*1000

    start_target_cats_finished = start_target_cats_finished.add_suffix('_finished')
    start_target_cats_unfinished = start_target_cats_unfinished.add_suffix('_unfinished')
    start_target_cats = start_target_cats_finished.join(start_target_cats_unfinished)
    start_target_cats['weighted_diff_start'] = start_target_cats.apply(lambda x: 
            (x.start_finished - x.start_unfinished) /(x.start_finished + x.start_unfinished), axis = 1)
    start_target_cats['weighted_diff_target'] = start_target_cats.apply(lambda x: 
                (x.target_finished - x.target_unfinished) /(x.target_finished + x.target_unfinished), axis = 1)
    start_target_cats['frac_start'] = start_target_cats.apply(lambda x: 
                (x.start_finished) /(x.start_finished + x.start_unfinished), axis = 1)
    start_target_cats['frac_target'] = start_target_cats.apply(lambda x: 
                (x.target_finished) /(x.target_finished + x.target_unfinished), axis = 1)
    return start_target_cats

def get_first_last(n, df, cat):
    """  Get all n highest and worst score of a given Series
    Args:
        n : the number of categories we want to print, 
        df : a df, 
        cat : the column of the df we want to get the n first and last categories  
    Return:
        a tuple with the n first and last categories  
    """
    df_sorted_cat = df[cat].sort_values()
    return df_sorted_cat[-n :][::-1], df_sorted_cat[:n]