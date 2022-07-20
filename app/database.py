"""
This module contains all database interfacing methods for the MFlix
application. You will be working on this file for the majority of M220P.

Each method has a short description, and the methods you must implement have
docstrings with a short explanation of the task.

Look out for TODO markers for additional help. Good luck!
"""
import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from dateutil import parser


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:

        db = g._database = PyMongo(current_app).db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def createBook(book_name,category,rent_per_day):
    book_name = book_name.lower().strip()
    comment_doc = {"bookName": book_name,"category": category,"rentPerDay": rent_per_day}
    return db.books.insert_one(comment_doc)
def searchBook(book_name):
    book_name = book_name.lower().strip()
    return list(db.books.find({"bookName": {"$regex": book_name, "$options": "$i"}},{"_id":0}))
def searchBookWithRange(min_price,max_price):
    return list(db.books.find({"rentPerDay": {"$gte":  min_price, "$lte": max_price}},{"_id":0}))
def searchBookWithFields(category,book_name,min_price,max_price):
    book_name = book_name.lower().strip()
    return list(db.books.find({"rentPerDay": {"$gte":  min_price, "$lte": max_price}, "bookName": {"$regex": book_name, "$options": "$i"},"category": category}, {"_id": 0}))
   

def issueBook(book_name,person_name,issue_date):
    book_name = (book_name.lower()).strip()
    book = db.books.find({"bookName":book_name})
    if(not book):
        return {"error": "no such book exist"}
    person_name = (person_name.lower()).strip()
    issue_date = datetime.strptime(issue_date, '%d/%m/%Y')
    issue_date = issue_date.isoformat()
    
    transaction_doc = {"bookName": book_name,"personName":person_name,"issueDate": issue_date}
    db.transactions.insert_one(transaction_doc)
    return {"message": "book issued successfully"}


def returnBook(book_name, person_name, return_date):
    book_name = (book_name.lower()).strip()
    book = db.books.find_one({"bookName": book_name})
    if(not book):
        return {"error": "no such book exist"}
    person_name = (person_name.lower()).strip()
    return_date = datetime.strptime(return_date, '%d/%m/%Y')
    return_date = return_date.isoformat()
    transaction = db.transactions.find_one({"personName": person_name, "bookName": book_name})
    
    return_date = parser.parse(return_date)
    issue_date = parser.parse(transaction["issueDate"])
    delta = return_date-issue_date
    rent = delta.days*book["rentPerDay"]
    final_transaction = db.transactions.find_one_and_update({"personName": person_name, "bookName": book_name}, {'$set': {"returnDate": return_date, "rent":rent}},{"_id":0})
    final_transaction["rent"] = rent
    return final_transaction
    
def bookIssued(book_name):
    book_name = book_name.lower().strip()
    book = db.books.find_one({"bookName": book_name})
    people_issued_book = db.transactions.count_documents({"bookName": book_name})
    people_currently_issued = db.transactions.find({"returnDate": {"$exists": False}, "bookName": book_name},{"_id":0,})
    response = {"noOfTimesBookIssued": people_issued_book, "currentIssuers": list(people_currently_issued)}
    return response

def rentGenerated(book_name):
    book_name = book_name.lower().strip()
    book = db.books.find_one({"bookName": book_name})
    rent_generated = db.transactions.aggregate([{"$match": {"returnDate": {"$exists": True},"bookName":book_name}}, {"$group": {"_id": "$bookName", "TotalSum": {"$sum": "$rent"}}}])
    all_rents = list(rent_generated)
    return {"totalRentGenerated": all_rents[0]["TotalSum"]}

def booksIssuedOnPersonName(person_name):
    person_name = person_name.lower().strip()
    list_books_issued = db.transactions.find({"personName": person_name},{"_id":0})
    return {"booksIssued": list(list_books_issued)}

def booksIssuedInDateRange(start_date,end_date):
    start_date = datetime.strptime(start_date, '%d/%m/%Y')
    start_date = start_date.isoformat()
    end_date = datetime.strptime(end_date, '%d/%m/%Y')
    end_date = end_date.isoformat()
    books_issued = list(db.transactions.find({"issueDate":{"$gte":start_date, "$lte": end_date}},{"_id":0}))
    
    return {"booksIssued": books_issued,"totalCount": len(books_issued)}

