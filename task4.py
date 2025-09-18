#Task 4: Query the database to retrieve all prompts generated today. 

import streamlit as st
import pymongo
from datetime import datetime


client = pymongo.MongoClient("mongodb://localhost:27017")
db = client['AI']
collection = db['AI_Task']

st.title("Prompts Generated Today ")

today = datetime.now().date()
start = datetime.combine(today, datetime.min.time())
end = datetime.combine(today, datetime.max.time())


prompts_today = list(
    collection.find({
        "timestamp": {"$gte": start, "$lte": end}
    })
)


if prompts_today:
    st.subheader("Today's Prompts:")
    for p in prompts_today:
        st.write(f" **Prompt:** {p.get('prompt')}")
        st.write(f" **Result:** {p.get('result')}")
        st.write(f" **Time :** {p.get('timestamp')}")
        st.markdown("---")
else:
    st.write("No prompts generated today.")
