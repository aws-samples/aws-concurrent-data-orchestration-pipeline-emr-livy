val ratings_df = spark.read.format("csv").option("header", "true").option("inferschema", "true").load("s3://<s3-bucket>/ratings.csv")

ratings_df.write.mode("overwrite").parquet("s3://<s3-bucket>/movielens-parquet/ratings/")
