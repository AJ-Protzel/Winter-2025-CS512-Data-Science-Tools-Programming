import pyspark
from pyspark.sql import SparkSession
import pprint
import json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, FloatType
from pyspark.sql import Window
from pyspark.sql.functions import col, sum, desc

sc = pyspark.SparkContext()

bucket = sc._jsc.hadoopConfiguration().get('fs.gs.system.bucket')
project = sc._jsc.hadoopConfiguration().get('fs.gs.project.id')
input_directory = 'gs://{}/hadoop/tmp/bigquerry/pyspark_input'.format(bucket)
output_directory = 'gs://{}/pyspark_demo_output'.format(bucket)

spark = SparkSession \
  .builder \
  .master('yarn') \
  .appName('transactions') \
  .config("spark.task.maxFailures", 8) \
  .getOrCreate()

conf = {
    'mapred.bq.project.id': 'transaction-pipeline',
    'mapred.bq.gcs.bucket': bucket,
    'mapred.bq.temp.gcs.path': input_directory,
    'mapred.bq.input.project.id': 'transaction-pipeline',
    'mapred.bq.input.dataset.id': 'transaction_data',
    'mapred.bq.input.table.id': 'transactions_modified',
}

# Pull table from BigQuery
table_data = sc.newAPIHadoopRDD(
    'com.google.cloud.hadoop.io.bigquery.JsonTextBigQueryInputFormat',
    'org.apache.hadoop.io.LongWritable',
    'com.google.gson.JsonObject',
    conf=conf)

# Convert table to a JSON-like object
vals = table_data.values()
vals = vals.map(lambda line: json.loads(line))

# Define schema
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("Year", IntegerType(), True),
    StructField("Month", StringType(), True),
    StructField("Day", IntegerType(), True),
    StructField("Date", DateType(), True),
    StructField("Description", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Amount", FloatType(), True),
    StructField("Type", StringType(), True),
    StructField("Bank", StringType(), True),
    StructField("Card", StringType(), True)
])

# Create a DataFrame object
df1 = spark.createDataFrame(vals, schema=schema)

# Repartition the DataFrame
df1 = df1.repartition(6)



# ## create window by partitioning by Icao and ordering by PosTime, then use lead to get next lat long
# window = Window.partitionBy("Icao").orderBy("PosTime").rowsBetween(1,1)
# df1=df1.withColumn("Lat2", lead('Lat').over(window))
# df1=df1.withColumn("Long2", lead('Long').over(window))
# df1 = df1.na.drop()

# # apply the haversine function to each set of coordinates
# haver_udf = udf(haversine, FloatType())
# df1 = df1.withColumn('dist', haver_udf('long', 'lat', 'long2', 'lat2'))
# #pprint.pprint(df1.take(5))

# ## sum the distances for each Icao to get distance each plane traveled
# df1.createOrReplaceTempView('planes')
# top = spark.sql("Select Icao, SUM(dist) as dist FROM planes GROUP BY Icao ORDER BY dist desc LIMIT 10 ")
# top = top.rdd.map(tuple)
# pprint.pprint(top.collect())

# ##sum the distances for all planes. 
# miles = spark.sql("Select SUM(dist) FROM planes")
# pprint.pprint(miles.collect())

pprint.pprint("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
pprint.pprint("Working")



# Delete the temporary files
input_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
input_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(input_path, True)