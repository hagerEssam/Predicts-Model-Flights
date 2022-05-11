# -*- coding: utf-8 -*-
"""EvaluateModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J40SXkClipxtTbV3ngF6AatW5oazRl91
"""

!pip install pyspark

from pyspark.sql import SparkSession

spark=SparkSession.builder.getOrCreate()

Flights=spark.read.csv("Flights.csv",header=True)
Planes=spark.read.csv("planes.csv",header=True)

# Rename year column
planes = Planes.withColumnRenamed("year","plane_year")

# Join the DataFrames
model_data = Flights.join(planes, on="tailnum", how="leftouter")

model_data.show() 
#Before you get started modeling :Cast the columns to integers (Spark only handles numeric data)

# Cast the columns to integers
model_data = model_data.withColumn("arr_delay", model_data.arr_delay.cast("integer"))
model_data = model_data.withColumn("air_time", model_data.air_time.cast("integer"))
model_data = model_data.withColumn("month", model_data.month.cast("integer"))
model_data = model_data.withColumn("plane_year", model_data.plane_year.cast("integer"))

# Create the column plane_age
model_data = model_data.withColumn("plane_age", model_data.year - model_data.plane_year)

# Create is_late
model_data = model_data.withColumn("is_late", model_data.arr_delay > 0)

# Convert to an integer
model_data = model_data.withColumn("label", model_data.is_late.cast("integer"))

# Remove missing values
model_data = model_data.filter("arr_delay is not NULL and dep_delay is not NULL and air_time is not NULL and plane_year is not NULL")

from pyspark.ml.feature import StringIndexer, OneHotEncoder
# Create a StringIndexer (String Indexer:convert the string values into label indices (numeric values))
carr_indexer = StringIndexer(inputCol="carrier",outputCol="carrier_index")
dest_indexer = StringIndexer(inputCol="dest",outputCol="dest_index")
# Create a OneHotEncoder (technique which is used to convert or transform a categorical feature having string labels into  numerical)
carr_encoder = OneHotEncoder(inputCol="carrier_index",outputCol="carrier_fact")
dest_encoder= OneHotEncoder(inputCol="dest_index",outputCol="dest_fact")

from pyspark.ml.feature import VectorAssembler
# Make a VectorAssembler(transformer that combines a given list of columns into a single vector column.)
vec_assembler = VectorAssembler(inputCols=["month", "air_time", "carrier_fact", "dest_fact", "plane_age"], outputCol="features")

from pyspark.ml import Pipeline

# Make the pipeline
flights_pipe = Pipeline(stages=[dest_indexer, dest_encoder, carr_indexer, carr_encoder, vec_assembler])

# Fit and transform the data
piped_data = flights_pipe.fit(model_data).transform(model_data)

# Split the data into training and test sets
training, test = piped_data.randomSplit([.6, .4])

training.show(5)

test.show(5)