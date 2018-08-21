from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def hello_world():
    html1 = """
        <ul>
        <ul>
    """
    authors = ['author1', 'author2', 'author3']
    html1 += ''.join([f'<li>{author}</li>' for author in authors])

    html2 = """
        <ul>
            {% for author in authors %}
            <li>{{author}}</li>
            {% endfor %}
        </ul>
    """

    rendered_html = render_template_string(html2,authors=authors)

    return rendered_html
