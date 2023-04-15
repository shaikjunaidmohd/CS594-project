# CS594-project
The repo includes both python files namely 

# DataLoading.py:
The Dataloading python file has a code for preprocessing the data As a preprocessing step we will be merging all the data records into a single data frame
using NumPy and pandas library. The dataset has the GPS tracking information of different users at specific timestamps, we took around 11 Users and 
combined the spatial information with there time stamps. Once the final data frame is acquired and it is serialized to a pickle file.

# SamplingnAggregation.py
This python file has the implementation of R-tree from scratch, Two different node structures are maintained one for the leaf node and one for the internal
nodes, The leaf node represents the raw data hence it has only longitude and latitude where as the internal node has both child links as well as the MBR 
(Minimum Box Region) of the child nodes.
