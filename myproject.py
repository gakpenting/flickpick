from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from flask_login import login_user, login_required, logout_user, UserMixin, LoginManager, login_manager, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from time import time
from datetime import datetime
from flask_cors import CORS
import os
from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

 
 

basedir = os.path.abspath(os.path.dirname(__file__))

def setup_schema(Base, session):
	# Create a function which incorporates the Base and session information
	def setup_schema_fn():
		for class_ in Base._decl_class_registry.values():
			if hasattr(class_, '__tablename__'):
				if class_.__name__.endswith('Schema'):
					raise ModelConversionError(
						"For safety, setup_schema can not be used when a"
						"Model class ends with 'Schema'"
						)

				class Meta(object):
					model = class_
					sqla_session = session

				schema_class_name = '%sSchema' % class_.__name__
				

				schema_class = type(
					schema_class_name,
					(ma.ModelSchema,),
					{'Meta': Meta}
					)

				setattr(class_, '__marshmallow__', schema_class)

	return setup_schema_fn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SECRET_KEY'] = 'shadowfox'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow()
db.init_app(app)
ma.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
CORS(app)

class Recommendation(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
  recommended_by = db.Column(db.String(128),nullable=False)
  recommender_id = db.Column(db.String(255),default="no url found")
  movie_title = db.Column(db.String(255))
  description = db.Column(db.Text)
  accepted = db.Column(db.Boolean, default=False)


class RecommendationSchema(ma.ModelSchema):
    class Meta:
        model = Recommendation
        fields = ('id','movie_title','recommended_by','recommender_id','description','accepted')

class Movie(db.Model):
    __searchable__ = ['genre']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(255))
    description = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    recommendation = db.relationship('Recommendation', backref="movies", cascade="all, delete-orphan" , lazy='dynamic')

class MovieSchema(ma.ModelSchema):
    class Meta:
        model = Movie
        fields = ("id","name","timestamp","username","description","genre","recommendation")
    recommendation = ma.Nested(RecommendationSchema, many=True)


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class User(db.Model,UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    movies = db.relationship('Movie', backref='author', lazy='dynamic')

    def get_id(self):
        return str(self.id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ("id", "username", "email","movies")
    movies = ma.Nested(MovieSchema, many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def hello():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return render_template('_index.html')
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Congrats you are registered.")
		return render_template('index.html')
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        isValidPassword = user.check_password(password)
        if not isValidPassword:
            return render_template('index.html')
        login_user(user)
        return render_template('_index.html')
    return render_template('index.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@app.route('/explore')
@login_required
def explore():
	return render_template("_index.html")

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('user.html', user=user)

@app.route('/ask_for_movie_recommendation', methods=['POST'])
def ask_for_movie_recommendation():
	post_data = request.get_json()
	mg = post_data['movie_genre']
	mn = post_data['movie_name']
	md = post_data['movie_description']
	ui = post_data['user_name']
	user = User.query.filter_by(username=ui).first()
	post = Movie(name=mn, description=md, genre=mg, user_id=user.id, username=ui)
	db.session.add(post)
	db.session.commit()
	data = get_update_movies(ui)
	print(data)
	return data

@app.route('/accept_recommendation/', methods=['POST'])
def accept_recommendation():
	data = request.get_json()
	rec_id = data['id']
	rec=Recommendation.query.filter_by(id=rec_id).first() 
	rec.accepted = True
	db.session.commit()
	return "accepted"

@app.route('/delete_post/', methods=['POST'])
def delete_post():
	data = request.get_json()
	_id = data['id']
	rec=Movie.query.filter_by(id=_id).first()
	db.session.delete(rec)
	db.session.commit()
	return "deleted"

@app.route('/reject_recommendation/', methods=['POST'])
def reject_recommendation():
	data = request.get_json()
	_id = data['id']
	rec=Recommendation.query.filter_by(id=_id).first()
	db.session.delete(rec)
	db.session.commit()
	return "deleted"

@app.route('/get_my_movies', methods=['POST'])
def get_my_movies():
	response_object = {'status': 'success'}
	param = request.get_json()
	user = param['user']
	movi = User.query.filter_by(username=user).first()
	user_schema = UserSchema()
	result = user_schema.dump(movi).data
	response_object['books'] = result
	return jsonify(response_object)


def get_update_movies(user):
	print('get update called')
	response_object = {'status': 'success'}
	param = request.get_json()
	user = user
	movi = User.query.filter_by(username=user).first()
	user_schema = UserSchema()
	result = user_schema.dump(movi).data
	response_object['books'] = result
	return jsonify(response_object)

@app.route('/get_all_movies', methods=['GET'])
def get_all_movies():
	response_object = {'status': 'success'}
	movi = Movie.query.all()
	rec = User.query.all()
	rr = Recommendation.query.all()
	movie_schema = MovieSchema(many=True)
	gs = users_schema.dump(rec).data
	result = movies_schema.dump(movi).data
	response_object['books'] = result
	return jsonify(response_object)

@app.route('/get_by_genre', methods=['GET'])
def get_by_genre():
	response_object = {'status': 'success'}
	genre = request.args.get('genre', '')
	movi = Movie.query.filter_by(genre=genre)
	movie_schema = MovieSchema(many=True)
	result = movies_schema.dump(movi).data
	response_object['books'] = result
	return jsonify(response_object)

@app.route('/recommend_movie', methods=['POST'] )
def recommend_movie():
	param = request.get_json()
	movie_id = param['movie_id']
	recommended_by = param['recommender_name']
	movie_title = param['movie_recommendation']
	description = param['movie_description']
	user_id = User.query.filter_by(username=recommended_by).first()
	movie=Movie.query.get(movie_id)
	rec=Recommendation(movie_id=movie_id,recommended_by=recommended_by,recommender_id=user_id.id,movie_title=movie_title,description=description)
	movie.recommendation.append(rec)
	db.session.add(movie)
	db.session.commit()
	return "recommendation was sent to user"

@login_manager.unauthorized_handler
def unauthorized():
	return redirect('/login')



if __name__ == "__main__":
    app.run(host='0.0.0.0')