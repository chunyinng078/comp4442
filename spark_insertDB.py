import os
import sys

from pyspark.sql.functions import split
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count

spark = SparkSession.builder.appName("example-pyspark-read-and-write").getOrCreate()

args = sys.argv
inp = args[1]
out = args[2]

df = spark.read.option("delimiter", ",").csv(inp)
# rename columns header to the following names

df = df.toDF("driver_id", "CarPlateNumber", "Latitude", "Longitude", "Speed", "Direction", "SiteName", "Time",
             "isRapidlySpeedup",
             "IsRapidlySlowdown", "IsNeutralSlide", "IsNeutralSlideFinished", "NeturalSlideTime", "IsOverSpeed",
             "IsOverSpeedFinished", "OverSpeedTime", "IsFatigueDriving", "IsHthrottleStop", "IsOilLeak", "Temp")

df = df.drop("Latitude", "Longitude", "Speed", "Direction", "SiteName",
             "isRapidlySpeedup", "IsOverSpeed",
             "IsRapidlySlowdown", "IsNeutralSlide", "IsNeutralSlideFinished",
             "IsOverSpeedFinished", "IsHthrottleStop", "IsOilLeak", "Temp")

# make time become date and time
df = df.withColumn("date and time", split(df.Time, " "))
df = df.drop("Time")
df = df.withColumn("Date", df["date and time"].getItem(0))
df = df.withColumn("Time", df["date and time"].getItem(1))
df = df.drop("date and time")
df = df.withColumn("Hour", split(df.Time, ":").getItem(0))
df.show()

# group by driver_id, CarPlateNumber, Hour
# sum NeturalSlideTime, count OverSpeedTime, sum OverSpeedTime, count IsFatigueDriving

result_df = df.groupBy("driver_id", "CarPlateNumber","Date", "Hour").agg(
    sum(col("NeturalSlideTime")).alias("TotalNeturalSlideTime"),
    count(col("OverSpeedTime")).alias("CountOfOverSpeed"),
    sum(col("OverSpeedTime")).alias("TotalOfOverSpeedTime"),
    count(col("IsFatigueDriving")).alias("CountOfFatigueDriving")
)

result_df = result_df.orderBy("driver_id", "CarPlateNumber", "Hour")
result_df.show()


result_df.write.option("header", "true").csv(out)
