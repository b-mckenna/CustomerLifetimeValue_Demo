from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *
import pandas as pd

def read_my_table(tablename):
  spark = SparkSession \
      .builder \
      .appName("read-table") \
      .getOrCreate()
      
  df = spark.sql("SELECT * FROM " + tablename)
  return df