# The tale of the unfinished paths

## Data story

Please visit our website [[here]](https://melsjagt.github.io/ada-template-website/)

## Abstract

Wikispeedia is an online game based on Wikipedia. A player has to reach an article from a not related article, only by using hyperlinks in the articles encountered [[1]](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf). By analyzing the graphs and data collected from people playing these games, a lot of interesting questions concerning semantic distance between concepts or the searching behavior of humans can be answered. To do this a lot of data is needed, which can be supported by an active community that frequently plays the Wikispeedia game. But how can you get people to play and finish the game maybe even multiple times? What motivates people to finish the task and do not give up? With this work these questions are answered by proposing a set-up for the game that is likely to incentivize people to stay engaged, and hence more data for analysis purposes can be generated.


## Research questions

   -  Can we set up a simple logistic model that can predict if a player is more likeli to stop the game or finish it based on the history of the games played by the         player and based on the start and target article?
   -  How can the results of the logistic regression be included in a set-up for a gme that is likely to incentivize people to stay engaged?


## Methods

   -  Preprocessing of the data
      -  Filtering out all the games played with a pathlength >= 1
   -  Between-Game history: To analyze the history of a certain player, the hasedusersId gets grouped and analyzed further.
      -  Preanalyzation answering the following questions:
         - How many people got unfinished/finished paths? 
         - How is the pathlength associated with the fraction of finished games?
         - Has the number of finished games an influence on the behaviour of the last game?
      -  Find interesting features based on the analysis for the logistic regression:
   -  In-game history: Analysis per game to try to understand what makes a player finish or not.
      -  Preprocessing: Building two graphs from the data provided. One graph is the path's graph (or reffered to as Player's Graph). It is a weighted directional              graph derived from the paths the players took. The edge weight is the number of occurences the path has been taken. The other graph is the ideal graph (or              referred to as  Machine’s Graph). It is generated from the links of different articles. Initial analysis suggests the graphs are very different.
      -  Generate feature fot the logistic regression: For categories, the in and out degrees and the possibility to be stuck in those categories were examined. Then,          a score for each was generated, indicating if this is a good category to begin or end with.
      -  Trying to answer the question how likeli the player will quit the game?
   -  Based on the features a logitstic regression is built
   -  The logitstic regression together with the analyzing parts in the in-game and between game history help find a conclusion and to propose a set-up to a game that       is likely to incentivize people to stay engaged. 

## Structure of the directory

The directory is organized according to the chapters in the webpage. Each file can be run individually. It contains the following notebooks:
   -  home: contains all the analysis used for the home part on the webpage
   -  between_game: contains all the analysis and feature generation done for the "Between game" chapter. 
   -  in_game: contains all the analysis and feature generation done for the "In game" chapter
   -  classification: contains the logistic regression and the intepretation of the logitstic regression. The feature files are saved in the folder "data" and the           classification can therefore be run individually.
   -  conclusion: contains all the information gathered for a conclusion.

In addition to that the following can be found:
   -  Milestone_2: It contains the analysis done for the milestone 2.
   -  helpers: containing functions that are used in different files or to simplify the main files. 
   -  data: folder that contains all the data from wikispeedia the project is based on as well as feature files for the in-game as well as the between game                   analyzation.


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

### Contribution of the team members



