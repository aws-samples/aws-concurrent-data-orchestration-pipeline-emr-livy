val genome_tags_df = spark.read.format("csv").option("header", "true").option("inferschema", "true").load("s3://<s3-bucket>/genome-tags.csv")

genome_tags_df.write.mode("overwrite").parquet("s3://<s3-bucket>/movielens-parquet/genome-tags/")
