from flask import Flask, render_template_string, render_template

app = Flask(__name__)

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
    return render_template('/authors_list.html')


@app.route('/authors/<author_name>')
def author_info(author_name):
    return render_template('author_info.html', author=AUTHOR_DATA[author_name])
