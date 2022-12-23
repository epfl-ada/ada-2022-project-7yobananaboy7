# The tale of the unfinished paths

## Data story

Please visit our website [here](https://melsjagt.github.io/ada-template-website/).

## Abstract

Wikispeedia is an online game based on Wikipedia. A player has to reach an article from a not related article, only by using hyperlinks in the articles encountered [[1]](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf). By analyzing the graphs and data collected from people playing these games, a lot of interesting questions concerning semantic distance between concepts or the searching behavior of humans can be answered. To do this a lot of data is needed, which can be supported by an active community that frequently plays the Wikispeedia game. In fact, sometimes more data on poor algorithms can beat state-of-the-art algorithm with less data.  But how can you get people to play and finish the game maybe even multiple times? What motivates people to finish the task and do not give up? With this work these questions are answered by proposing a set-up for the game that is likely to incentivize people to stay engaged, and hence more data for analysis purposes can be generated.


## Research questions
   - Can we set up a simple logistic model that can predict if a player is more likely to stop the game or finish it based on the history of the games played by the player and based on the start and target article?
   - How can the results of the logistic regression be included in a set-up for a game that is likely to incentivize people to stay engaged and play more games?
   - How to make the game easier for the players and give hints to them when necessary to keep them motivated?

## Methods

### General

- Preprocessing of the data
   - Filtering out all the games played with a pathlength >= 1
- Between-Game history: To analyze the history of a certain player, the hashedUsersId gets grouped and analyzed further.
   - Preanalyzation answering the following questions:
      - How many people got unfinished/finished paths? An unfinished path is in the following always considering timeout and restart.
      - How is the pathlength associated with the fraction of finished games?
      - Has the number of finished games an influence on the behaviour of the last game?
   -  Find interesting features based on the analysis for the logistic regression.
- In-game history: Analysis per game to try to understand what makes a player finish or not.
   -  Preprocessing: Building two graphs from the data provided. One graph is the path's graph (or reffered to as Player's Graph). It is a weighted directional graph derived from the paths the players took. The edge weight is the number of occurences the path has been taken. The other graph is the ideal graph (or referred to as  Machine’s Graph). It is generated from the links of different articles. Initial analysis suggests the graphs are very different.
   - Generate features fot the logistic regression: For categories, the in and out degrees and the possibility to be stuck in those categories were examined. Then, a score for each was generated, indicating if this is a good category to begin or end with.
   - Trying to answer the question how likely the player will quit the game by analyzing the path during a run. We generated a Progress Score trying to discriminate whether people will finish the run in an ongoing run. We also analyzed players' motivation to play with in-game history and found interesting results.
- Based on the features a logitstic regression is built
- The logitstic regression together with the analyzing parts in the in-game and between game history help to find a conclusion and to propose a set-up for a game that is likely to incentivize people to stay engaged. 

### External lybraries

The following external lybraries are used for the analysis:

- matplotlib.pyplot
- itertools.groupby
- seaborn
- pandas
- os
- numpy
- sklearn
- statsmodels.formula.api
- scipy.stats
- networkx
- re
- urllib
- bokeh

## Structure of the directory

The directory is organized according to the chapters in the webpage. Each file can be run individually. It contains the following notebooks:

- `1. Home.ipynb`: First we look at the history of each player, get indight on the data and the motivation on why there is a big potential that players play more and therefore that we can get more data 
- `2. Between_game.ipynb`: In this notebook we look at the history of the players, how many resulted in a finished game and how long was the tale of unfinished paths before the last game. We also look at the success streak and the time between the first and last game.
- `3. In_game.ipynb`: We then look at each game separatly and understand what make a specific game hard or easy. We analyse the impact of the starting and target page and in which categories players can get stuck during their game. We also discussed about the path and distance to the target in each run and how it influences the result and the motivation of the player.
- `4. Classification.ipynb`: The logistic regression is done with the features gathered from the two previous parts and the intepretation of the logitstic regression is done. The feature files are saved in the folder "data" and the classification can therefore be run individually.
- `5. Conclusion.ipynb`: All the information gathered for a conclusion.

In addition to that the following can be found:

- `Milestone_2.ipynb`: It contains the analysis done for the milestone 2.
- `helpers.py`: Containing functions that are used to simplify the `in_game.ipynb` notebook. The functions in this file are for loading and parsing raw data into something we can process in the later analysis.
- `data`: folder that contains all the data from wikispeedia the project is based on as well as feature files for the in-game and the between game analysis.

### Contribution of the team members

- EDA : all
- Between game analysis : Mels and Tamara
- In-Game analysis : Mathieu and Mengjie
- Classification : Mels and Tamara
- Readme : Tamara and Mathieu
- Website : Mels
