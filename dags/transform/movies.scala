val movies_df = spark.read.format("csv").option("header", "true").option("inferschema", "true").load("s3://<s3-bucket>/movies.csv")

movies_df.write.mode("overwrite").parquet("s3://<s3-bucket>/movielens-parquet/movies/")
