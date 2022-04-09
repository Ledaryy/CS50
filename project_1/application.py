import os
import requests



from flask import (
    Flask,
    session,
    redirect,
    url_for,
    request,
    render_template,
    jsonify
)
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#postgres://xuyazebdhruvlk:87d1ab284b99585250d3f2233f11e4ba75760e831a8a250d0c680b106fb40cde@ec2-54-246-90-10.eu-west-1.compute.amazonaws.com:5432/dflpa40tjbn6be






  
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session.pop("user_id", None)
#Login & password
        username = request.form.get("username")
        try:
            password = int(request.form.get("password"))
        except ValueError:
            return render_template("error.html", message = "Use only numbers in password")
#Database
        if db.execute("SELECT * FROM users WHERE username = :username AND userpassword = :password", 
                    {"username":username, "password":password}).rowcount == 1:
            user = db.execute("SELECT * FROM users WHERE username = :username",
                    {"username":username}).fetchone()
#Session      
            session["user_id"] = user.id
            return redirect(url_for('user', user=user.username))
        return render_template("error.html", message=" Wrong username/password")
    return render_template("index.html")

@app.route("/user/<string:user>", methods=["GET"])
def user(user):
    if request.method == "GET":
        if "user_id" in session:
            users = db.execute("SELECT * FROM users").fetchall()
            return render_template("main.html", users = users)
    return render_template("error.html", message="User not logged in")
        

@app.route("/registration", methods=["POST", "GET"])
def registration():
    users = db.execute("SELECT * FROM users").fetchall()
    if request.method == "POST":
        username = str(request.form.get("username"))
        try:
            password = int(request.form.get("password"))
        except ValueError:
            return render_template("error.html", message="Use only numbers in password")
        
        if db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount >= 1:
            return render_template("error.html", message="User already exist")
        
        db.execute("INSERT INTO users (username, userpassword) VALUES (:username, :userpassword)",
                    {"username":username, "userpassword":password})
        db.commit()
        return render_template("success.html", message="Registration completed")
    
    return render_template("registration.html")

@app.route("/logout", methods = ["POST"])
def logout():
    if request.method == "POST":
        session.pop("user_id", None)
        return render_template("success.html", message = "Logout completed")
    return render_template("error.html", message = "method not allowed")

@app.route("/search", methods = ["POST", "GET"])
def search():
    if request.method == "POST":
        books = request.form.get("search")
        if books == "":
           return render_template("error.html", message = "Type the book name first")
        class Books:
            isbn = db.execute("SELECT * FROM books WHERE isbn LIKE :ISBNCODE", {"ISBNCODE":'%'+books+'%'}).fetchall()
            author = db.execute("SELECT * FROM books WHERE author LIKE :AUTHORCODE", {"AUTHORCODE":'%'+books+'%'}).fetchall()
            title = db.execute("SELECT * FROM books WHERE title LIKE :TITLECODE", {"TITLECODE":'%'+books+'%'}).fetchall()

        return render_template("books.html", books = Books, booksSearch = books)
    return render_template("error.html", message = "Something go wrong (you used GET for search!)")

@app.route("/book/<book>", methods = ["POST", "GET"])   
def book(book):
    if db.execute("SELECT * FROM books WHERE isbn = :ISBNCODE", {"ISBNCODE":book}).rowcount == 0:
        return render_template("error.html", message="We dont have book with that ISBN code")
    bookInfo = db.execute("SELECT * FROM books WHERE isbn = :ISBNCODE", {"ISBNCODE":book}).fetchone()
    bookisbn = book
    if request.method == "POST":
        score = request.form.get("inlineRadioOptions")
        reviewtext = request.form.get("review")
        if score is None:
            score = 0
        if reviewtext == "":
            reviewtext = "No text"
        if db.execute("SELECT username FROM users WHERE id = :userid", {"userid":session["user_id"]}).rowcount == 0:
            return render_template("error.html", message = "You are not logged in")
        else:
            user = db.execute("SELECT * FROM users WHERE id = :userid", {"userid":session["user_id"]}).fetchone()
        if db.execute("SELECT * FROM reviews WHERE username = :USERNAME AND bookisbn = :ISBNCODE", {"USERNAME":user.username, "ISBNCODE":bookisbn}).rowcount == 1:
            return render_template("error.html", message = "You cant submit multiple reviews for the same book")
        db.execute("INSERT INTO reviews (username, bookisbn, review, score) VALUES(:username, :bookisbn, :review, :score)", 
                                        {"username":user.username, "bookisbn":bookisbn, "review":reviewtext, "score":score })
        db.commit()
        
    if db.execute("SELECT * FROM reviews WHERE bookIsbn = :ISBNCODE", {"ISBNCODE":book}).rowcount == 0:
        review = ""
    else:
        review = db.execute("SELECT * FROM reviews WHERE bookIsbn = :ISBNCODE", {"ISBNCODE":book}).fetchall()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "z4TB9KudCF5ImXc74SI32A", "isbns": bookisbn})
    
    data = res.json()
    averageRating = data["books"][0]['average_rating']
    ratingCount = data["books"][0]['work_ratings_count']

    return render_template("bookPage.html", book=bookInfo, review = review, average = averageRating, count = ratingCount)
    
@app.route("/api/<isbn>")
def book_api(isbn):
    
    if db.execute("SELECT * FROM books WHERE isbn = :ISBNCODE", {"ISBNCODE":isbn}).rowcount == 0:
        return jsonify({"error": "Invalid ISBN number"}), 404
    else:
        book = db.execute("SELECT * FROM books WHERE isbn = :ISBNCODE", {"ISBNCODE":isbn}).fetchone()
        reviews = db.execute("SELECT * FROM reviews WHERE bookIsbn = :ISBNCODE", {"ISBNCODE":isbn}).fetchall()
        counter = 0
        score = 0
        for review in reviews:
            counter += 1
            score += int(review.score)
        average_score = score / counter
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.publicationyear,
            "isbn": isbn,
            "review_count": counter,
            "average_score": average_score
        })
     