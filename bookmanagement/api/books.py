from crypt import methods
from venv import create
from flask import Blueprint, request, jsonify
from bookmanagement.db import  rentGenerated, createBook, searchBook, searchBookWithRange, searchBookWithFields, issueBook, returnBook, bookIssued, rentGenerated, booksIssuedOnPersonName, booksIssuedInDateRange

from flask_cors import CORS
from bookmanagement.api.utils import expect
from datetime import datetime


books_api_v1 = Blueprint(
    'books_api_v1', 'books_api_v1', url_prefix='/api/v1/books')

CORS(books_api_v1)


@books_api_v1.route('/create', methods=["POST"])
def create_book():
    post_data = request.get_json()
    createBook(post_data["book_name"],
               post_data["category"], post_data["rent_per_day"])
    return jsonify({"status": 'book created succesfully'})


@books_api_v1.route('/<book_name>/search', methods=["GET"])
def search_book(book_name):
    books = searchBook(book_name)
    return jsonify({"books": books, "totalRecords": len(books)})


@books_api_v1.route('/search/pricerange', methods=["GET"])
def search_book_price_range():
    min_price = int(request.args.get('min_price',0))
    max_price = int(request.args.get('max_price',100))
    books = searchBookWithRange(min_price,max_price)
    return jsonify({"books": books, "totalRecords": len(books)})


@books_api_v1.route('/search/fields', methods=["POST"])
def search_book_fields():
    post_data = request.get_json()
    books = searchBookWithFields(
        post_data["category"], post_data["book_name"], post_data["min_price"], post_data["max_price"])
    return jsonify({"books": books, "totalRecords": len(books)})


@books_api_v1.route('/issue', methods=["POST"])
def issue_book():
    post_data = request.get_json()
    res = issueBook(post_data["book_name"],
                    post_data["person_name"], post_data["issue_date"])
    return jsonify(res)


@books_api_v1.route('/return', methods=["POST"])
def return_book():
    post_data = request.get_json()
    res = returnBook(post_data["book_name"],
                     post_data["person_name"], post_data["return_date"])
    return jsonify(res)


@books_api_v1.route('/<book_name>/issued', methods=["GET"])
def book_issued(book_name):
    res = bookIssued(book_name)
    return jsonify(res)


@books_api_v1.route('/<book_name>/rent/generated', methods=["GET"])
def rent_generated(book_name):
    res = rentGenerated(book_name)
    return jsonify(res)


@books_api_v1.route('/issued/persons/<person_name>', methods=["GET"])
def books_issued_on_person_name(person_name):

    res = booksIssuedOnPersonName(person_name)
    return(jsonify(res))


@books_api_v1.route('/issued/date', methods=["GET"])
def books_issued_in_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    res = booksIssuedInDateRange(start_date, end_date)
    return jsonify(res)
