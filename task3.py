#Task 3: Create a schema for storing AI-generated content (prompt, result, timestamp).

import pymongo
import streamlit as st  
from datetime import datetime        
from transformers import pipeline 

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
print(client)
    
# Creating DB 
db = client['AI']

# Creating collection (table) inside DB
collection = db['AI_Task']

# Hugging Face pipeline
generator = pipeline("text-generation", model="distilgpt2")

# Streamlit app
st.title("AI Generator with MongoDB")

user_prompt = st.text_area("Enter your prompt here:")

if st.button("Generate and save"):
    if user_prompt.strip():
        # Generate text
        response = generator(
            user_prompt,
            max_length=100,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )
        raw_text = response[0]["generated_text"]

       
        generated_text = raw_text[len(user_prompt):].strip()

        
        doc = {
            "prompt": user_prompt,
            "result": generated_text,
            "timestamp": datetime.now()
        }

        
        collection.insert_one(doc)

        
        st.success("Saved successfully")
        st.subheader("Generated Result")
        st.write(generated_text)

else:
    st.warning("Please enter a prompt before generating")
