# Milestone 2 - The tale of the unfinished paths

## Abstract

Wikispeedia is an online game based on Wikipedia. A player has to reach an article from a not related article, only by using hyperlinks in the articles encountered [[1]](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf). By analyzing the graphs and data collected from people playing these games, a lot of interesting questions concerning semantic distance between concepts or the searching behavior of humans can be answered. To do this a lot of data is needed. But how can you get people to play and finish the game maybe even multiple times? What motivates people to finish the task and do not give up? With this work these questions are answered by proposing a set-up for the game that is likely to incentivize people to stay engaged, and hence more data for analysis purposes can be generated.

## Research questions

The goal of this project is to first investigate how to get people engaged in a game by seeing why they stop playing. According to the results we should find what makes the game easy or difficult so that we can tailor the games to the level and needs of the players that want to quit.
1. Is there a pattern in the players' history that makes them stop playing the game?
   - e.g. number of games played before
   - e.g. progress during a single run
2. What is the interaction between timeout and restart in the unfinished paths?
3. How do we break the pattern of disengagement?


## Methods

- Preprocessing of the data.
   - Invalid or less valuable data: We find some ‘cheating’ attempts with duration less than 1 second and path length less than 2. We propose to filter out those data. In addition, we suggest excluding the paths with length shorter than 4 (about 8 percent) when analyzing the strategy stages of players. This way we are left with "serious" attempt only.
  
  - Organizing the data: We formed two graphs from the data we loaded. One graph is the paths’ graph (or referred to as Player’s Graph). It is a weighted directional graph derived from the paths the players took. The edge weight is the number of occurences the path has been taken. The other graph is the ideal graph (or referred to as Machine’s Graph). It is generated from the links of different articles. Initial analysis suggests the graphs are very different.


- Firstly we try to find patterns from player’s History to find why they quit the game. The History can be categorized into two kinds: In-Run History and Game History. In-Run History refers to the path one player has taken in a game whereas Game History is the record of the different games. We examine reasons for quitting during a run which will, if it happens frequently, result in complete abandonment of the game. We want to explore potential reasons driving this behavior such as:
   - People find themselves getting farther from their goal. For that we need to determine a metric of distance in the Player’s Graph.
   - People get tired of clicking through pages or spend too much time and lose patience.
   - People get stuck at different ‘game stages’ (‘Going to a Hub’ stage or ‘Converging’ stage - or purely have no strategy at all).
   - People are stuck in certain concepts or the target concept is really hard to reach
   - Other potential reasons we might discover in later analysis

   We deal with the situations separately:
   - We have to find a certain metric from the Player’s Graph or use ‘semantic distance’ as proposed in the paper to identify how far people were to their goals when they quit their game.
   - We use logistic regression to analyze the relationship between path length/duration/other features to be found with whether people quit the game.
   - We combine in-degree, out-degree and number of accesses (weight in the paths’ graph) to find potential hub articles, and then deduce from each path at which stage the player quitted or where there was no obvious strategy at all.
   - We merge the nodes with the same concepts and see how the resulting graph is structured. We generate some stats (from the distribution of in-degree or out-degree, weights of edges and nodes) and then confirm or reject our hypothesis via hypothesis testing.


   Game History refers to the history of each player’s runs, whether finished or not. We tried to get players' history in term or how their games ended up (finished, restart, timeout). Then we use a logistic regression to examine how much the number of previous finishes, restarts and timeouts have an influence of the next run’s quitting or not. And we can also use clustering algorithms to find patterns of player’s Game History.

- In addition, we want to have an objective metric of how hard a run is. We have the Ideal Graph and the Player’s Graph. For some games we also have the subjective rating from the player. We can consider the subjective rating as a result of objective difficulty, player’s In-Run History, player’s Game History (experience) and player's domain knowledge (that determines the distance metric). The objective difficulty is solely the result of the positions of source and target in both graphs, assuming the graph is ‘complete’. We can make use of machine learning techniques to find the correlations and infer from them the objective difficulty.


### Timeline
1. Finish preprocessing 30.11
1. Find new interesting features about the runs for the regressions. 30.11
1. Find what are the hubs pages 30.11
1. Search and find a first metric to establish how far are two pages and a second one to establish how hard a run is. 30.11
1. Construct the graph with the nodes merged by concepts and see if people get stuck in the same concept 4.12
1. Make an history for each players of their duration time path length, the concepts they go through and find a pattern using Multi-class Logistic regression 9.12
1. Additional stuff we might want to do 13.12
1. Finish coding and start writing report 16.12
1. Submission 23.12

### Organization within the team

- Mels will focus on 1, 5, 7, 8, 9
- Tamara on 2, 6, 7, 8, 9
- Mengjie on 3, 5, 7, 8, 9
- Mathieu on 4, 6, 7, 8, 9

### (Optional) Questions for TAs

- Preprocess data, how to handle outliers? 
How to handle values for finished paths for example that are at path_length 0 and time 0? How do we set a threshold.
