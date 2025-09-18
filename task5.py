#Task 5: Connect a Streamlit app to MongoDB to show generated results live.

import streamlit as st
import pymongo
from datetime import datetime
import time


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["AI"]
collection = db["AI_Task"]



st.title("Live Generated Results")


def get_results():
    results = list(collection.find().sort("timestamp", -1).limit(10))
    return results


placeholder = st.empty()

while True:
    with placeholder.container():
       
        results = get_results()
        
        if results:
            for record in results:
                st.write(f"**Prompt:** {record.get('prompt', '')}")
                st.write(f"**Result:** {record.get('result', '')}")
                st.caption(f" {record.get('timestamp', '')}")
                st.markdown("---")
        else:
            st.warning(" No results found in the database.")

    time.sleep(5)  
