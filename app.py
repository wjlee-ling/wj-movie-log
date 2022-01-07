"""
ver: 1.1 왜 안돼
to-do:
User class, Admin instance 추가
1. Movie -> add : poster col 
2. 댓글: email 추가 (관련 email validator도) + 언제 댓글 달았는지 추가  + 지울 수 있게끔 수정
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from forms import CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] =  'eyf4-DEN34-3v!dD' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_log.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #to supress warning

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), index=True, unique=True, nullable=False)
    director = db.Column(db.String(20), index=True)
    imdb = db.Column(db.String(80))
    review = db.relationship('Review', backref='movie', lazy='dynamic', cascade='all, delete, delete-orphan')
    comments = db.relationship('Comment', backref='movie', lazy='dynamic',cascade='all, delete, delete-orphan')
    watch_log = db.relationship('WatchLog', backref='movie', lazy='dynamic',cascade='all, delete, delete-orphan')

class WatchLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    where = db.Column(db.String(10))
    when = db.Column(db.String(10))

class Review(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    text = db.Column(db.String(30))

class Comment(db.Model):
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    id = db.Column(db.Integer, primary_key=True)
    commenter = db.Column(db.String(10), nullable=False)
    text = db.Column(db.String(50), nullable=False)

## routing
@app.route("/", methods=['GET', 'POST'])
def index():
    movies = Movie.query.all()
    return render_template("index.html", movies = movies)

@app.route("/about-me")
def about():
    return render_template("about.html")

@app.route("/movie/<int:id>", methods= ['GET', 'POST'])
def movie(id):
    movie = Movie.query.get_or_404(id, description="There is no movie with the given ID.")
    #movie = Movie.query.get(id).first_or_404(description = "There is no movie with this ID.")
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
    # 처음 access시 오류 안 나게 하는 코드

        new_comment = Comment(movie_id= id, commenter=comment_form.user_name.data, text=comment_form.comment.data)

        # db에 추가
        db.session.add(new_comment)
        # 오류시 db 원상복구
        try:
            db.session.commit()
        except:
            db.session.rollback()

    return render_template("movie.html", template_form = comment_form, movie= movie)


if __name__ == "__main__":
    app.run()