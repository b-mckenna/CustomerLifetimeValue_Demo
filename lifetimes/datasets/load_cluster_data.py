from pyspark.sql import SparkSession
from pyspark.sql.types import *
import pandas as pd
#pd.options.display.html.table_schema = True

def read_my_csv(filename):
  spark = SparkSession.builder \
      .appName("customer-data") \
      .getOrCreate()
  
  schemaData = StructType([StructField("date", StringType(), True),
                         StructField("id", StringType(),True)])

  data = spark.read.schema(schemaData).csv(filename,header='true')
  
  return data