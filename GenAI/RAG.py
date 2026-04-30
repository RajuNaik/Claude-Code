# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "2"
# ///
# MAGIC %md
# MAGIC # 🚀 Enterprise AI Assistant using RAG
# MAGIC
# MAGIC ## 📌 Overview
# MAGIC
# MAGIC This project demonstrates an end-to-end **Retrieval-Augmented Generation (RAG)** system built using open-source tools on Databricks Community Edition.
# MAGIC
# MAGIC The system enables users to query enterprise data using natural language and receive context-aware, AI-generated responses.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🎯 Objective
# MAGIC
# MAGIC - Enable semantic search over enterprise data  
# MAGIC - Generate context-aware responses using LLMs  
# MAGIC - Build a scalable AI assistant architecture  
# MAGIC - Demonstrate real-world GenAI system design  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🧠 Key Concepts
# MAGIC
# MAGIC - **Chunking** → Splitting large text into smaller pieces  
# MAGIC - **Embeddings** → Converting text into vectors  
# MAGIC - **Vector Search** → Finding similar data using embeddings  
# MAGIC - **RAG** → Combining retrieval + LLM for answers  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 End-to-End Flow
# MAGIC
# MAGIC ```
# MAGIC User Query
# MAGIC    ↓
# MAGIC Query Embedding
# MAGIC    ↓
# MAGIC Vector Search (FAISS)
# MAGIC    ↓
# MAGIC Retrieve Relevant Chunks
# MAGIC    ↓
# MAGIC Build Context
# MAGIC    ↓
# MAGIC LLM Processing
# MAGIC    ↓
# MAGIC Final Answer
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🏗️ Architecture Diagram
# MAGIC
# MAGIC ```
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │   User Query         │
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ Query Embedding      │
# MAGIC                 │ (SentenceTransformer)│
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ Vector Database      │
# MAGIC                 │ (FAISS Index)        │
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ Retrieve Top-K       │
# MAGIC                 │ Relevant Chunks      │
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ Context Builder      │
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ LLM (distilgpt2)     │
# MAGIC                 └─────────┬────────────┘
# MAGIC                           ↓
# MAGIC                 ┌──────────────────────┐
# MAGIC                 │ Final Clean Answer   │
# MAGIC                 └──────────────────────┘
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚙️ Technology Stack
# MAGIC
# MAGIC | Layer | Technology |
# MAGIC |------|------------|
# MAGIC | Data Processing | PySpark |
# MAGIC | Storage | Delta Lake |
# MAGIC | Chunking | Python UDF |
# MAGIC | Embeddings | Sentence Transformers |
# MAGIC | Vector DB | FAISS |
# MAGIC | LLM | Hugging Face (distilgpt2) |
# MAGIC | Platform | Databricks Community Edition |
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔄 Detailed Data Flow
# MAGIC
# MAGIC ### Step 1: Data Ingestion
# MAGIC - Load enterprise data into Delta tables  
# MAGIC
# MAGIC ### Step 2: Chunking
# MAGIC - Split documents into manageable chunks  
# MAGIC - Preserve semantic meaning  
# MAGIC
# MAGIC ### Step 3: Embedding Generation
# MAGIC - Convert chunks into vector representations  
# MAGIC
# MAGIC ### Step 4: Vector Index Creation
# MAGIC - Store embeddings in FAISS index  
# MAGIC
# MAGIC ### Step 5: Query Processing
# MAGIC - Convert user query into embedding  
# MAGIC
# MAGIC ### Step 6: Retrieval
# MAGIC - Perform similarity search  
# MAGIC - Fetch top-k relevant chunks  
# MAGIC
# MAGIC ### Step 7: Context Building
# MAGIC - Combine retrieved chunks  
# MAGIC
# MAGIC ### Step 8: LLM Generation
# MAGIC - Generate response using context  
# MAGIC
# MAGIC ### Step 9: Output Cleaning
# MAGIC - Extract and refine final answer  

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧠 RAG (Retrieval-Augmented Generation)
# MAGIC
# MAGIC RAG enhances LLM responses by injecting relevant context from enterprise data.
# MAGIC
# MAGIC ### Without RAG
# MAGIC - LLM answers from general knowledge  
# MAGIC - May hallucinate  
# MAGIC
# MAGIC ### With RAG
# MAGIC - LLM answers based on retrieved data  
# MAGIC - Grounded and accurate responses  
# MAGIC
# MAGIC ### Flow
# MAGIC
# MAGIC ```
# MAGIC Question → Retrieve Data → Provide Context → Generate Answer
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ## 💼 Business Use Cases
# MAGIC
# MAGIC - Sales analytics assistant  
# MAGIC - Supply chain insights  
# MAGIC - Internal knowledge assistant  
# MAGIC - Customer support automation  
# MAGIC - Financial reporting assistant  
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚠️ Limitations
# MAGIC
# MAGIC - Local LLM (distilgpt2) has limited reasoning capability  
# MAGIC - FAISS is in-memory (not scalable for large datasets)  
# MAGIC - No real-time data ingestion  
# MAGIC - No authentication / access control  
# MAGIC
# MAGIC ---

# COMMAND ----------

# MAGIC %md
# MAGIC %md
# MAGIC ## 🛠️ Implementation Guide
# MAGIC
# MAGIC This section walks through the step-by-step implementation of the RAG pipeline using Databricks.
# MAGIC
# MAGIC We will build the system incrementally, starting from environment setup to generating AI-powered responses.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## ⚙️ What to Expect
# MAGIC
# MAGIC Each step includes:
# MAGIC - A brief explanation of the objective  
# MAGIC - Corresponding code implementation  
# MAGIC - Output validation  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 🔄 Implementation Steps
# MAGIC
# MAGIC 1. Install required libraries  
# MAGIC 2. Create and load sample enterprise data  
# MAGIC 3. Perform text chunking  
# MAGIC 4. Generate embeddings  
# MAGIC 5. Create vector index (FAISS)  
# MAGIC 6. Perform semantic search  
# MAGIC 7. Build context from retrieved data  
# MAGIC 8. Generate response using LLM  
# MAGIC 9. Clean and format final answer  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## 📌 Note
# MAGIC
# MAGIC - Ensure each step is executed sequentially  
# MAGIC - Some steps depend on outputs from previous cells  
# MAGIC - Re-run dependent cells if any changes are made  
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC 👉 Let’s start by installing the required libraries.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📦 Install Required Libraries
# MAGIC
# MAGIC Install the dependencies for embeddings and vector search:
# MAGIC
# MAGIC ```python
# MAGIC %pip install sentence-transformers faiss-cpu
# MAGIC dbutils.library.restartPython()
# MAGIC ```
# MAGIC
# MAGIC **Explanation:**
# MAGIC - `sentence-transformers` → Used to generate embeddings (text → vectors)
# MAGIC - `faiss-cpu` → Used for vector similarity search (vector database)
# MAGIC - `dbutils.library.restartPython()` → Restarts the Python session to apply installed packages

# COMMAND ----------

# MAGIC %pip install sentence-transformers faiss-cpu
# MAGIC %pip install transformers
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 📄 Create and Store Raw Data
# MAGIC
# MAGIC Create sample data and store it in a Delta table for further processing.
# MAGIC
# MAGIC **What happens here?**
# MAGIC - Define sample documents as input data  
# MAGIC - Convert data into a Spark DataFrame  
# MAGIC - Save the DataFrame as a Delta table (`rag_raw`)  
# MAGIC - Load and display the stored data  

# COMMAND ----------

data = [
    ("doc1", """PepsiCo sales data for Q1 2025 shows that North America generated $12 billion in revenue, with beverages contributing 60% and snacks contributing 40%. Pepsi, Mountain Dew, and Gatorade were the top-selling beverage brands."""),
    
    ("doc2", """In the APAC region, sales increased by 8% year-over-year due to strong demand for Lay’s and Kurkure products. India contributed significantly to snack category growth, particularly in urban markets."""),
    
    ("doc3", """Supply chain disruptions in Europe impacted product availability during February 2025. Delays in raw material shipments caused a 5% drop in overall sales for the region."""),
    
    ("doc4", """PepsiCo operates using a global distribution network that includes manufacturing plants, warehouses, and retail partners. Efficient logistics planning is critical to maintaining product availability."""),
    
    ("doc5", """The company uses a demand forecasting system powered by machine learning models to predict sales trends and optimize inventory levels across regions."""),
    
    ("doc6", """Mountain Dew sales increased by 12% in North America due to successful marketing campaigns targeting younger consumers through digital platforms."""),
    
    ("doc7", """Kurkure and Lay’s continue to dominate the snacks segment in India, with a combined market share exceeding 45%."""),
    
    ("doc8", """Data pipelines in PepsiCo are built using Databricks Lakehouse architecture, enabling scalable processing of billions of transactions daily."""),
    
    ("doc9", """Retail analytics systems track product performance across thousands of stores, providing insights into consumer behavior and purchasing patterns."""),
    
    ("doc10", """Sustainability initiatives include reducing plastic usage and optimizing supply chain operations to minimize carbon emissions across manufacturing plants."""),
    
    ("doc11", """The finance team monitors revenue, cost, and profit margins using centralized reporting dashboards powered by cloud data platforms."""),
    
    ("doc12", """Inventory management systems ensure optimal stock levels across warehouses, reducing overstock and stockouts while improving operational efficiency.""")
]

df = spark.createDataFrame(data, ["id", "text"])
df.write.mode("overwrite").saveAsTable("rag_raw")

# COMMAND ----------

display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✂️ Chunk the Data
# MAGIC Split large text into smaller chunks for better retrieval.
# MAGIC
# MAGIC **Why chunking?**
# MAGIC - Improves search accuracy  
# MAGIC - Handles large documents efficiently  
# MAGIC - Fits LLM input limits  

# COMMAND ----------

def chunk_text(text, size=150, overlap=30):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

from pyspark.sql.functions import udf, explode, col
from pyspark.sql.types import ArrayType, StringType

# Register UDF
chunk_udf = udf(chunk_text, ArrayType(StringType()))

# Apply chunking
df_chunks = spark.table("rag_raw") \
    .withColumn("chunks", chunk_udf(col("text"))) \
    .withColumn("chunk", explode(col("chunks"))) \
    .select("id", "chunk")

# Save to Delta table
df_chunks.write.mode("overwrite").saveAsTable("rag_chunks")

# COMMAND ----------

display(df_chunks)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧠 Generate Embeddings (Hugging Face — no API key)
# MAGIC Convert text chunks into numerical vector representations.
# MAGIC
# MAGIC **Why embeddings?**
# MAGIC - Enables semantic understanding  
# MAGIC - Allows similarity-based search instead of keyword matching  

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

# COMMAND ----------

display(df_embed)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🔍 Create Vector Database (FAISS)
# MAGIC Store embeddings in a vector index for fast similarity search.
# MAGIC
# MAGIC **Why vector DB?**
# MAGIC - Efficient nearest-neighbor search  
# MAGIC - Scales for large datasets  
# MAGIC - Core component of RAG systems  

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
# MAGIC ### 🔎 Query the Vector Database (semantic search)
# MAGIC
# MAGIC Convert the user query into an embedding and retrieve the most relevant chunks using semantic similarity.
# MAGIC
# MAGIC **What happens here?**
# MAGIC - Query → converted into a vector (embedding)  
# MAGIC - Vector search → finds top matching chunks  
# MAGIC - Returns relevant context for further processing  
# MAGIC
# MAGIC 👉 This step enables **semantic search**, where results are based on meaning rather than exact keyword matches.

# COMMAND ----------

def embed_query(q):
    return model.encode(q).astype("float32")

# 🔥 Better, more descriptive query
query = "Which region generated the highest revenue in PepsiCo sales data?"

qv = np.array([embed_query(query)])

# 🔥 Increase top-k
D, I = index.search(qv, k=5)

retrieved_chunks = [texts[i] for i in I[0]]

print("FULL CONTEXT:\n")
for chunk in retrieved_chunks:
    print("-", chunk)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🤖 Generate Answer using LLM (RAG)
# MAGIC
# MAGIC Use the retrieved chunks as context to generate a final, human-readable answer.
# MAGIC
# MAGIC **What happens here?**
# MAGIC - Combine retrieved chunks into context  
# MAGIC - Pass context + query to the model  
# MAGIC - Generate a grounded response  
# MAGIC
# MAGIC 👉 This step completes the RAG pipeline by combining retrieval with AI reasoning.

# COMMAND ----------

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model
model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model_llm = AutoModelForCausalLM.from_pretrained(model_name)

# Build context
retrieved_chunks = [texts[i] for i in I[0]]
context = "\n".join(retrieved_chunks)

print("Context:\n", context)

# Improved prompt
prompt = f"""
You are an enterprise AI assistant.

Answer ONLY using the context below.
If the answer is not present, say: I don't know.

Context:
{context}

Question:
{query}

Answer:
"""

# Tokenize
inputs = tokenizer(prompt, return_tensors="pt")

# Generate (optimized)
with torch.no_grad():
    outputs = model_llm.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False
    )

# Decode
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("\nRaw Model Output:\n")
print(response)

# COMMAND ----------

# response is already a string in your case

raw_output = response

# Extract answer part again (safe fallback)
if "Answer:" in raw_output:
    answer = raw_output.split("Answer:")[-1].strip()
else:
    answer = raw_output.strip()

# Keep only first meaningful line
answer = answer.split("\n")[0]

print("\nFinal Clean Answer:\n")
print(answer)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🧪 Sample Questions to Try
# MAGIC
# MAGIC Use the following queries to explore the AI assistant and understand how it retrieves and answers from enterprise data.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📊 Sales & Revenue Insights
# MAGIC - Which region generated the highest revenue?
# MAGIC - What were the total sales in North America?
# MAGIC - How did APAC perform in terms of sales growth?
# MAGIC - Which region showed a decline in sales?
# MAGIC - What contributed to revenue in Q1 2025?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🌍 Regional Performance
# MAGIC - Which region had the highest growth rate?
# MAGIC - What happened to sales in Europe?
# MAGIC - How did India contribute to APAC sales?
# MAGIC - Which markets are driving snack sales growth?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🏭 Supply Chain & Operations
# MAGIC - What caused the drop in Europe sales?
# MAGIC - How does PepsiCo manage its supply chain?
# MAGIC - What are the key challenges in the supply chain?
# MAGIC - How do logistics impact product availability?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 📦 Products & Categories
# MAGIC - Which products are performing well in India?
# MAGIC - What are the top-selling beverage brands?
# MAGIC - How do snacks contribute to overall revenue?
# MAGIC - Which category contributes more: beverages or snacks?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🧠 Technology & Data Platform
# MAGIC - How is Databricks used in PepsiCo?
# MAGIC - What is the Lakehouse architecture?
# MAGIC - How are data pipelines structured in PepsiCo?
# MAGIC - How does machine learning help in demand forecasting?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🌱 Sustainability & Strategy
# MAGIC - What sustainability initiatives does PepsiCo have?
# MAGIC - How is PepsiCo reducing carbon emissions?
# MAGIC - What are the company's long-term strategic goals?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ❓ General / Open Queries
# MAGIC - Give a summary of PepsiCo sales performance
# MAGIC - What are key business insights from the data?
# MAGIC - Explain major challenges faced by PepsiCo
# MAGIC - What trends can be observed in the data?
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚠️ Edge Case Testing
# MAGIC - Who is the CEO of PepsiCo?
# MAGIC - What is the stock price today?
# MAGIC - Tell me something not present in the data
# MAGIC
# MAGIC 👉 Expected behavior: The system should respond with **"I don't know"** when the answer is not in context.
# MAGIC
