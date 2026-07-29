from pyspark.sql import functions as F
from pyspark.sql.window import Window

def deduplicar(df, coluna_id, coluna_data):

    if coluna_data not in df.columns:
        df = df.withColumn(coluna_data, F.current_timestamp())

    w = Window.partitionBy(coluna_id).orderBy(F.col(coluna_data).desc())

    df = (
        df.withColumn("rn", F.row_number().over(w))
          .filter("rn = 1")
          .drop("rn")
    )

    df = df.withColumn("data_atualizacao", F.current_timestamp())
    return df
