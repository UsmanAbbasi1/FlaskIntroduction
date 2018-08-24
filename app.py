from flask import Flask, render_template_string, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# URI for different dbs are provided in Flask docs. We are using postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usman:arbiarbi@localhost/flask_intro'
db = SQLAlchemy(app)


# Run this line in python shell to create all tables
# db.create_all()


class Country(db.Model):
    """Model for storing countries"""
    __tablename__ = 'country'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.VARCHAR)
    author = db.relationship('Author', backref='country', cascade='all, delete-orphan', lazy='dynamic')


class Author(db.Model):
    """Model for storing authors"""
    __tablename__ = 'author'
    id = db.Column('id', db.Integer, primary_key=True)
    # Foreign key to country from which author belongs
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    name = db.Column('name', db.VARCHAR)


@app.route('/')
def hello_world():
    """hello world to show how to render html code from view"""
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


@app.route('/authors/<string:author_name>')
def author_info(author_name):
    """
    Get author from db and pass them in template
    :param author_name: name of author to fetch from db
    """
    author = Author.query.filter_by(name=author_name)
    return render_template('author_info.html', authors=author)


@app.route('/info')
def info():
    """Example to show how to redirect from one view to another"""
    # url_for takes name of view and params and create a url for that view
    return redirect(url_for('request_info'), code=301)


@app.route('/request_info')
def request_info():
    return render_template('request_info.html')


@app.route('/authors')
def authors_info():
    """Get all authors from db and pass them in template"""
    authors = Author.query.all()
    return render_template('author_info.html', authors=authors)


@app.route('/countries', methods=['POST', 'GET'])
def countries():
    """Example to handle POST and GET requests"""
    if request.method == 'GET':
        return render_template('forms/country_form.html')
    elif request.method == 'POST':
        # data passed from front-end i.e template in form is available in request.form
        db.session.add(Country(name=request.form['name']))
        db.session.commit()
        return 'Successfully added new country!'


@app.before_request
def before_request():
    """
    @app.before_request decorator makes this function to be called before every request
    This function can be used to do work needs to be done before every request
    """
    print('before request called')


@app.errorhandler(404)
def not_found(error):
    """
    @app.errorhandler() decorator is used to return the custom response if error is raised by any view.
    404 here suggests that this function should be called only if 404 exception is raised
    """
    # Ideally you should render some custom template here like this:
    # return render_template('/custom_404.html'), 404
    return 'Page not found.'
