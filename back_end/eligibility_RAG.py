import os
import json
import re
import faiss
import numpy as np
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

#  Explicit API Key
GEMINI_API_KEY = "API KEY"

#  Load and Clean Grants JSON
file_path = "Capstone\grants.json"

with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

clean_content = re.sub(r"[\x00-\x1F\x7F]", "", content)
grants_data = json.loads(clean_content)

print(f" Total Grants in JSON: {len(grants_data)}")

#  Initialize FAISS
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

grant_texts = []
grant_vectors = []
grant_ids = {}  # Mapping of index → grant_id

#  Process Only First 30 Grants & Skip Empty Grants
max_grants = 30  #  Limit to 30 grants
processed_count = 0

for i, grant in enumerate(grants_data):
    if processed_count >= max_grants:
        break  #  Stop after processing 30 grants

    grant_id = str(grant.get("id", f"unknown_{i}"))
    description = grant.get("description", "")
    full_text = grant.get("fulltext", "")

    #  Skip grants if BOTH fields are missing
    if not description and not full_text:
        print(f"Skipping grant {i}: No description or fulltext found.")
        continue  

    #  Combine description & full_text for embedding
    grant_content = f"{description}\n{full_text}"

    #  Generate Embedding
    embedding = embedding_model.embed_documents([grant_content])[0]

    #  Store Data
    grant_texts.append(grant_content)
    grant_vectors.append(embedding)
    grant_ids[processed_count] = grant_id  #  Use processed_count to maintain indexing

    processed_count += 1  # Track valid grants

print(f" Successfully processed {processed_count} grants!")

#  Convert embeddings to NumPy
grant_vectors = np.array(grant_vectors, dtype=np.float32)
dimension = grant_vectors.shape[1]

#  Initialize FAISS
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(grant_vectors)

vector_store = 

print(f" Stored {vector_store.index.ntotal} grants in FAISS!")

#  Generate Eligibility Questions Using LLM
llm = GoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_output_tokens=1024,
    google_api_key=GEMINI_API_KEY
)

#  Prompt for Generating Questions
question_prompt = PromptTemplate.from_template("""
Analyze the following grant details and generate key eligibility-related questions:

{grant_content}

Focus on:
- Who is eligible?
- Target industries?
- Geographic restrictions?
- Funding limits?
- Application deadlines?

Return questions in a numbered list.
""")

llm_chain_questions = LLMChain(llm=llm, prompt=question_prompt)

#  Generate Eligibility Questions
eligibility_questions_dict = {}
for i, grant_text in enumerate(grant_texts):
    response = llm_chain_questions.run({"grant_content": grant_text})
    eligibility_questions_dict[grant_ids[i]] = response.split("\n")  # ✅ Store as list

print(" Eligibility questions generated!")

#  RAG: Search FAISS Only Within the Specific Grant
import numpy as np

def retrieve_answers(question, grant_index):
    query_embedding = np.array(embedding_model.embed_documents([question]))  # ✅ Convert list to NumPy array
    query_embedding = query_embedding.reshape(1, -1)  #  Now reshape works

    distances, indices = faiss_index.search(query_embedding, 3)

    best_answer = None
    for i in range(len(indices[0])):
        best_index = indices[0][i]
        if best_index == grant_index:  #  Ensure correct grant retrieval
            best_answer = grant_texts[best_index]
            break

    return best_answer if best_answer else "No relevant answer found."
#  Format Eligibility Criteria
criteria_prompt = PromptTemplate.from_template("""
Format the following eligibility questions and answers into a structured eligibility criteria summary:

Questions:
{questions}

Answers:
{answers}

Return a professional, formatted eligibility criteria.
""")

llm_chain_criteria = LLMChain(llm=llm, prompt=criteria_prompt)

#  Process Each Grant
for grant_id, questions in eligibility_questions_dict.items():
    print(f"\n🔹 Processing Grant ID: {grant_id}")

    grant_index = list(grant_ids.values()).index(grant_id)

    answers = [retrieve_answers(q, grant_index) for q in questions]

    formatted_criteria = llm_chain_criteria.run({"questions": questions, "answers": answers})

    print(f"\n Eligibility Criteria for Grant ID {grant_id}:\n{formatted_criteria}\n")
