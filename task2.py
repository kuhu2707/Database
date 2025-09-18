#Task 2: Insert user input from a Flask app into MongoDB

from flask import Flask
from flask_pymongo import PyMongo



app=Flask(__name__)

#connecting mongodb with flask
app.config["MONGO_URI"] ="mongodb://localhost:27017/myDatabase"
# mongo = PyMongo(app)

# @app.route('/')
# def helloe():
#     #inseting data into mongodb
#     mongo.db.myCollection.insert_one({'name': 'kuhu'})
#     return "hello kuhu!"



#--------can also be used or write as ----------
db=PyMongo(app).db

@app.route('/')
def hello():
    #inseting data into mongodb
    db.myCollection.insert_one({'name': 'rajat'})
    return "hello kuhu"
    

if __name__ == "__main__":
    app.run(debug=True)