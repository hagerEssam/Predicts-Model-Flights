# Predicts-Model-Flights
Build a model that predicts whether or not a flight will be delayed based on the flights data we've been working with. 
This model will also include information about the plane that flew the route
1)Rename the year column of planes to plane_year to avoid duplicate column names
2)Join the two tables: flights and planes
3)Create a new DataFrame called model_data by joining the flights table with planes using the tailnum column as the key
4)Cast the columns to integers
5)create a boolean column which indicates whether the flight was late or not (is_late)
6)Remove missing values
7)Create a StringIndexer (String Indexer:convert the string values into label indices (numeric values))
8)Create a OneHotEncoder (technique which is used to convert or transform a categorical feature having string labels into  numerical)
9)Make a VectorAssembler(transformer that combines a given list of columns into a single vector column.)
10)Make the pipeline (allows us to maintain the data flow of all the relevant transformations that are required to reach the end result)
11)Fit and transform the data
12)Split the data into training and test sets
13)show my results
----------------
programming languages : Python ( Pyspark ) 
