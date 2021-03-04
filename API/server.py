from fastapi import FastAPI
from pymongo import MongoClient
from models import *
from typing import Optional

app = FastAPI()
client = MongoClient(
    "Тут сами"
)
db = client.mygovno
collection = db.mygovno


@app.post("/create/")
async def create_item(user: User):
    path = {
        "_id": user.name + "_" + user.family,
        "password": user.password,
        "age": user.age
    }

    if collection.count_documents({"_id": path["_id"]}) == 0:
        collection.insert_one(path)

    return user


@app.put("/edit/")
async def edit(user: User):
    path = {
        "password": user.password,
        "age": user.age
    }

    collection.update_one({"_id": user.name + "_" + user.family}, {"$set": path})

    return user


@app.delete("/delete/")
async def delete(user: Delete):
    collection.remove({"_id": user.name})   

    return f"Deleted user {user.name}"


@app.get("/search")
async def search(first_name: Optional[str], last_name: Optional[str]):
    for i in collection.find({"_id": first_name + "_" + last_name}):
        return {
            "name": first_name,
            "family": last_name,
            "password": i["password"],
            "age": i["age"]
        }


@app.get("/search_all")
async def search():
    return [
        {
            "name": i["_id"].split("_")[0],
            "family": i["_id"].split("_")[1],
            "password": i["password"],
            "age": i["age"]
        }
        for i in collection.find()]

#За то всё работает
