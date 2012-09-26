from app import db
import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique= True)
	email = db.Column(db.String(120), index=True, unique= True)
# 	role = db.Column(db.SmallInteger, default=ROLE_USER)
# 	posts = db.relationship('Post', backref='user',lazy='dynamic')
# 	comments = db.relationship('Comment', backref='user',lazy='dynamic')
# 	tags = db.relationship('Tag', backref='user',lazy='dynamic')

# class Post(db.Model):
# 	id = db.Column(db.BigInteger, primary_key=True)
# 	title = db.Column(db.String(150))
# 	content = db.Column(db.Text)
# 	poster = db.Column(db.Integer, db.ForeignKey('user.id'))
# 	comments = db.relationship('Comment', backref='post', lazy='dynamic')
# 	post_time = db.Column(db.DateTime, default=datetime.datetime.now())

# class Comment(db.Model):
# 	id = db.Column(db.BigInteger, primary_key=True)
# 	content = db.Column(db.Text)
# 	commenter = db.Column(db.Integer, db.ForeignKey('user.id'))
# 	post = db.Column(db.BigInteger, db.ForeignKey('post.id'))
# 	comment_time = db.Column(db.DateTime, default=datetime.datetime.now())

# class Tag(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	tag_name = db.Column(db.String(100), index=True, unique=True)
# 	tagger = db.Column(db.Integer, db.ForeignKey('user.id'))
