import pyspark
from pyspark.sql import SparkSession
import pprint
import json
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType, FloatType
from pyspark.sql import Window
from pyspark.sql.functions import col, sum as _sum, desc
from pyspark.sql.functions import to_date

sc = pyspark.SparkContext()

bucket = sc._jsc.hadoopConfiguration().get('fs.gs.system.bucket')
project = sc._jsc.hadoopConfiguration().get('fs.gs.project.id')
input_directory = 'gs://{}/hadoop/tmp/bigquerry/pyspark_input'.format(bucket)
output_directory = 'gs://{}/pyspark_demo_output'.format(bucket)

spark = SparkSession \
  .builder \
  .master('yarn') \
  .appName('transactions') \
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

## create a dataframe object
df1 = spark.createDataFrame(vals, schema= schema)
df1.repartition(6) 



# # Calculate the total expenses for each month
# window = Window.partitionBy("Year", "Month").orderBy(desc("Total_Expenses"))
# monthly_expenses = df1.groupBy("Year", "Month").agg(_sum("Amount").alias("Total_Expenses"))

# # Rank the months by total expenses
# ranked_expenses = monthly_expenses.withColumn("Rank", row_number().over(window))

# # Filter to get the top 5 months with the most expenses
# top_expenses = ranked_expenses.filter(col("Rank") <= 5)

# top_expenses.show()



# Calculate the total expenses for each month and rank them to show the top 5 months with the most expenses
df1.createOrReplaceTempView('transactions')
top_expenses = spark.sql("""
SELECT Year, Month, SUM(Amount) as Total_Expenses 
FROM transactions 
GROUP BY Year, Month 
ORDER BY Total_Expenses DESC 
LIMIT 5
""")

top_expenses.show()


# Delete the temporary files
input_path = sc._jvm.org.apache.hadoop.fs.Path(input_directory)
input_path.getFileSystem(sc._jsc.hadoopConfiguration()).delete(input_path, True)