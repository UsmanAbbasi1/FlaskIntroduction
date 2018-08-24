from flask import Flask, render_template_string, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usman:arbiarbi@localhost/flask_intro'
db = SQLAlchemy(app)


# Run this line in python shell to create all tables
# db.create_all()


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR)
    author = db.relationship('Author', backref='country', cascade='all, delete-orphan', lazy='dynamic')


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column('id', db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column('name', db.VARCHAR)


AUTHOR_DATA = {
    'Poe': {'name': 'Poe', 'age': 50},
    'Jane': {'name': 'Jane Austen', 'age': 40},
}


@app.route('/')
def hello_world():
    html1 = """
        <ul>
    """
    authors = ['author1', 'author2', 'author3']
    html1 += ''.join([f'<li>{author}</li>' for author in authors])
    html1 += '</ul>'

    html2 = """
        <ul>
            {% for author in authors %}
            <li>{{author}}</li>
            {% endfor %}
        </ul>
    """

    # rendered_html = render_template_string(html2, authors=authors)
    rendered_html = render_template_string(html1)

    return rendered_html


@app.route('/index/')
def index():
    return render_template('index.html')


@app.route('/authors/list')
def authors():
    return render_template('authors_list.html')


@app.route('/authors/<string:author_name>')
def author_info(author_name):
    author = Author.query.filter_by(name=author_name)
    return render_template('author_info.html', authors=author)


@app.route('/info')
def info():
    return redirect(url_for('request_info'), code=301)


@app.route('/request_info')
def request_info():
    return render_template('request_info.html')


@app.route('/authors')
def authors_info():
    authors = Author.query.all()
    return render_template('author_info.html', authors=authors)


@app.before_request
def before_request():
    print('before request called')


@app.errorhandler(404)
def not_found(error):
    # Ideally you should render some custom template here like this:
    # return render_template('/custom_404.html'), 404
    return 'Page not found.'
