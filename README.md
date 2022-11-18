# Milestone 2 - The tale of the unfinished paths

### Abstract
Wikispeedia is an online game based on Wikipedia. A player has to reach an article from a not related article, only by using hyperlinks in the articles encountered [[1]](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf). By analyzing the graphs and data collected from people playing these games a lot of interesting questions concerning the searching behaviour of humans can be answered or also propositions of how articles should be designed can be done. To do this a lot of data is needed. But how can you get people to play and finish the game maybe even multiple times? What motivates people to finish the task and do not give up? With this work these questions are answered by propsing a set up for the game that is likely to motivate people to play multiple times so that more data for analyzation purposes can be generated. 

### Research questions
Understand when they give up : Is it because it is too easy/hard, is it because the concept of the target is really hard to reach, …
What makes people restart, give up ?

Understand what is an easy game, is it in terms of distance in the link paths or in terms of the distance in the graph with the player paths.

### Methods
1. Preprocessing of the data.

   * Invalid or Less valuable data: We find some ‘cheating’ attempts with duration less than 1 second and path length less than 2. We filtered out those data. In addition, we excluded the paths with length shorter than 4 (about 8 percent) when analyzing the strategy stages of players.

   * Organizing the data: We formed two graphs from the data we loaded. One graph is the paths’ graph (or referred to as Player’s Graph). This graph is derived from the paths of the players of different attempts. It’s a weighted directional graph. The weight for each edge is the number of attempts having that path. The other graph is the ideal graph (or referred to as Machine’s Graph). It’s generated from the links of different articles. Initial analysis suggests the graphs are very different. Other data is stored in dataframes, such that we can perform regression analysis or more complex methods.

2. Firstly, we try to find patterns from player’s History which can be categorized into two kinds: In-Run History and Game History. In-Run History refers to the path one player has taken. We examine the probable reasons for quitting during a run such as:

   * People find themselves getting farther from their goal.
   * People get tired of clicking through pages or spend too much time and lose patience.
   * People get stuck at different ‘game stages’ (‘Going to a Hub’ stage or ‘Converging’ stage or purely have no strategy at all).
   * People are stuck in certain concepts
   * Other potential reasons we might discover in later analysis

    In this sense, we deal with the situations separately:

   * We use a certain matric we find from the Player’s Graph (Graph generated from paths of players, in our case the matric could be the weighted path length to the target in the graph) or ‘semantic distance’ as proposed in the paper to identify how far people were to their goals when they quit their game.
   * We use logistic regression to analyze the relationship between path length/duration with whether people quit the game.
   * We combine in-degree, out-degree and number of accesses (weight in the paths’ graph) to find potential hub articles, and then deduce from each path at which stage the player quitted or there was no obvious strategy at all.
   * We merge the nodes with the same concepts and see how the resulting graph is structured. We generate some stats (from the distribution of in-degree or out-degree, weights of edges and nodes) and then confirm or reject our hypothesis via hypothesis testing.

    Game History refers to the history of each player’s runs, whether finished or not. We tried to get players' history in term or how their games ended up (finished, restart, timeout). Then we simply use a logistic regression to examine how much the number of previous finishes, restarts and timeouts have an influence of the next run’s quitting or not. And we can also use clustering algorithms to find patterns of player’s Game History.

3. In addition, we want to have an objective metric of how hard a run is. We have the Ideal Graph and the Player’s Graph. For some games we also have the subjective rating from the player. We can consider the subjective rating as a result of objective difficulty, player’s In-Run History, player’s Game History (experience). The objective difficulty is solely the result of the positions of source and target in both graphs, assuming the graph is ‘complete’. We can make use of machine learning techniques to find the correlations and infer from them the objective difficulty.  


### Timeline
- Submission 23.12.2022

### Organization within the team

### (Optional) Questions for TAs
Add here any questions you have for us related to the proposed project.



