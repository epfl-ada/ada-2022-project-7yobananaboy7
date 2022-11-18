# Milestone 2 - The tale of the unfinished paths

### Abstract
Wikispeedia is an online game based on Wikipedia. A player has to reach an article from a not related article, only by using hyperlinks in the articles encountered [[1]](http://infolab.stanford.edu/~west1/pubs/West-Pineau-Precup_IJCAI-09.pdf). By analyzing the graphs and data collected from people playing these games a lot of interesting questions concerning the searching behaviour of humans can be answered or also propositions of how articles should be designed can be done. To do this a lot of data is needed. But how can you get people to play and finish the game maybe even multiple times? What motivates people to finish the task and do not give up? With this work these questions are answered by propsing a set up for the game that is likely to motivate people to play multiple times so that more data for analyzation purposes can be generated. 

### Research questions
Understand when they give up : Is it because it is too easy/hard, is it because the concept of the target is really hard to reach, …
What makes people restart, give up ?

Understand what is an easy game, is it in terms of distance in the link paths or in terms of the distance in the graph with the player paths.

### Methods

When describing the relevant aspects of the data, and any other datasets you may intend to use, you should in particular show (non-exhaustive list):

That you can handle the data in its size.
That you understand what’s in the data (formats, distributions, missing values, correlations, etc.).
That you considered ways to enrich, filter, transform the data according to your needs.
That you have a reasonable plan and ideas for methods you’re going to use, giving their essential mathematical details in the notebook.
That your plan for analysis and communication is reasonable and sound, potentially discussing alternatives to your choices that you considered but dropped.


What analysis do we want to do ? 
Difference between restart and finished are only in time not in term of pathLength
Difference between restart and timeout 
We need to go deeper in the graph 
Look at the shortest path in the players graph with the weights 
Find more features to use in the logistic regression 
Type of concepts people used 


Do players that timeout or restart always end up in the same set of concepts ? These concepts would be considered hard to reach 
Is the ratings related to some metric distance in the players graph (sum 1/w)

Methods 
Find a metric distance on the paths’ graph that makes the correspondence between this distance and the ratings 
Find some metrics that we can use for the (multi-class) logistic regression 
Construct a graph that ‘merge’ nodes that has the same concepts, see the internal links and how they connect to other concepts 
Try to find if concepts are apart and hard to reach 


### Timeline
- Submission 23.12.2022

### Organization within the team

### (Optional) Questions for TAs
Add here any questions you have for us related to the proposed project.



