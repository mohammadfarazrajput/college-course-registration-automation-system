import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
# ---- Load CSV (Semester 3 extracted table) ----
csv_path = r"D:\deep_learning\courseRegisteration\college-course-registration-automation-system\data\extracted_tables\page_1_table_1.csv"

df = pd.read_csv(csv_path)

# Convert to JSON string
sem3_data = df.to_json(orient="records", indent=2)

# ---- Initialize Gemini ----
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0
)

# ---- Prompt Template ----
prompt = ChatPromptTemplate.from_template("""
You are a university academic assistant.

Here is the Semester 3 course data:

{data}

Answer the user's question using ONLY the provided data.
If information is not present, say it is not available.

User question:
{question}
""")

chain = prompt | llm

# ---- Ask Question ----
question = "Give me all semester 3 courses with credits."

response = chain.invoke({
    "data": sem3_data,
    "question": question
})

print(response.content)
