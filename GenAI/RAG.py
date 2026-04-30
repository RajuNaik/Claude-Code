# Databricks notebook source
# MAGIC %md
# MAGIC ### Install

# COMMAND ----------

# MAGIC %skip
# MAGIC %pip install sentence-transformers faiss-cpu
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

data = [
    ("doc1", "Databricks is a unified data and AI platform."),
    ("doc2", "RAG systems use embeddings and vector search."),
    ("doc3", "PySpark enables distributed data processing.")
]

df = spark.createDataFrame(data, ["id", "text"])
df.write.mode("overwrite").saveAsTable("rag_raw")
spark.table("rag_raw").show()

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Chunk (simple + overlap)

# COMMAND ----------

def chunk_text(text, size=50, overlap=10):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

from pyspark.sql.functions import udf, explode, col
from pyspark.sql.types import ArrayType, StringType

chunk_udf = udf(chunk_text, ArrayType(StringType()))

df_chunks = spark.table("rag_raw") \
    .withColumn("chunks", chunk_udf(col("text"))) \
    .withColumn("chunk", explode(col("chunks"))) \
    .select("id", "chunk")

df_chunks.write.mode("overwrite").saveAsTable("rag_chunks")
df_chunks.show(truncate=False)

# COMMAND ----------

display(df_chunks)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Embeddings (Hugging Face — no API key)

# COMMAND ----------

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(text):
    return model.encode(text).tolist()

from pyspark.sql.types import ArrayType, FloatType
embed_udf = udf(embed, ArrayType(FloatType()))

df_embed = spark.table("rag_chunks") \
    .withColumn("embedding", embed_udf(col("chunk")))

df_embed.write.mode("overwrite").saveAsTable("rag_embeddings")
df_embed.show(truncate=False)

# COMMAND ----------

display(df_embed)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Vector DB (FAISS)

# COMMAND ----------

import faiss
import numpy as np

rows = spark.table("rag_embeddings").collect()

texts = [r["chunk"] for r in rows]
embs  = np.array([r["embedding"] for r in rows]).astype("float32")

dim = embs.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embs)

print("Vectors indexed:", index.ntotal)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Query (semantic search)

# COMMAND ----------

def embed_query(q):
    return model.encode(q).astype("float32")

query = "What is Databricks?"
qv = np.array([embed_query(query)])

D, I = index.search(qv, k=2)

print("Top matches:")
for i in I[0]:
    print("-", texts[i])
