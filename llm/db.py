from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri)
collection = client.journals.entries

def get_entries(user_id, limit=3):
    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit)
    return [
        f"Prompt: {d['generated_prompt']}\nJournal: {d['user_entry']}\nAdvice: {d['ai_advice']}\nTime: {d['timestamp']}"
        for d in cursor
    ]
def save(user_id, prompt, entry, advice):
    collection.insert_one({
        "user_id": user_id,
        "generated_prompt": prompt,
        "user_entry": entry,
        "ai_advice": advice,
        "timestamp": datetime.now()
    })

def get_hist(user_id):
    cursor = collection.find({"user_id":user_id})
    return [f"Journal: {d['user_entry']}\nDate: {d['timestamp']}"
            for d in cursor]



if __name__ == "__main__":
    uid = "sayantan123"
    save(
        uid,
        "W?",
        "I",
        "Y"
    )
    for item in get_hist(uid):
        print(item)
        print("-" * 50)

