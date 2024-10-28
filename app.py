import streamlit as st
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from google.generativeai import configure, GenerativeModel

# Load environment variables
load_dotenv()
import os
print("Pinecone API Key:", os.getenv("PINECONE_API_KEY"))

pinecone_api_key = os.getenv("PINECONE_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
pinecone_index_name = "avg-sales"

# Initialize Pinecone client with the new setup
pc = Pinecone(api_key=pinecone_api_key)

# Check if index exists, else create it
if pinecone_index_name not in pc.list_indexes().names():
    pc.create_index(
        name=pinecone_index_name,
        dimension=1000,  # Adjust the dimension according to your embeddings
        metric='cosine',  # or 'euclidean' based on your preference
        spec=ServerlessSpec(
            cloud='aws',  # Adjust according to your region
            region='us-east-1'  # Adjust based on your region
        )
    )

# Configure Google Gemini API
configure(api_key=google_api_key)
chat_model = GenerativeModel('gemini-chat-model')  # Replace with the actual model name

def search_embeddings(query):
    """Retrieve the most relevant data based on the user query."""
    results = pc.index(pinecone_index_name).query(query, top_k=1, include_values=True)
    return results['matches'][0]['values'] if results['matches'] else None

def generate_power_query_response(context, user_query):
    """Generate a Power Query response using Google Gemini."""
    prompt = f"Based on this context:\n{context}\n\nGenerate Power Query code for the query: '{user_query}'"
    response = chat_model.generate_content(prompt)
    return response.text

# Streamlit Interface
st.title("AI Agent for Power Query Generation")
query = st.text_input("Ask your question about Power Query:")
if st.button("Generate Power Query"):
    if query:
        context = search_embeddings(query)
        if context:
            answer = generate_power_query_response(context, query)
            st.write("Generated Power Query:", answer)
        else:
            st.write("No relevant data found.")
