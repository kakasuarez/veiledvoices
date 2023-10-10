from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    comments = db.relationship('Comment', backref='post')

    def __repr__(self):
        return f'<Post "{self.title}">'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return f'<Comment "{self.content[:20]}...">'

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts, len=len)


@app.route('/<int:post_id>/', methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == "POST":
        comment = Comment(content=request.form.get("content"), post_id=post_id)
        db.session.add(comment)
        db.session.commit()
    return render_template('post.html', post=post)

@app.route('/new', methods=["GET", "POST"])
def new_post():
    if request.method == "GET":
        return render_template("new_post.html")
    post = Post(content=request.form["content"], title=request.form["title"])
    db.session.add(post)
    db.session.commit()
    return redirect(url_for("post", post_id=post.id))



if __name__ == '__main__':
	app.run()
