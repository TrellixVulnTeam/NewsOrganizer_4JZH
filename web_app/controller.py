import flask
from torchtext.data.utils import get_tokenizer

from neural.common.utils import tokenize_text_content
from utils.database import DatabaseConnector

app = flask.Flask(__name__)
connector = DatabaseConnector()
articles = connector.get_articles()
word_tokenizer = get_tokenizer('spacy', language='en_core_web_sm')


@app.route('/news', methods=['GET'])
def get_articles():
    tags_count = connector.get_article_tags_count()
    return flask.render_template('news.html', articles=articles, tags_count=tags_count)


@app.route('/article/<article_index>', methods=['GET'])
def show_article(article_index: int):
    article = articles[int(article_index) - 1]
    tokens = tokenize_text_content(article.content, word_tokenizer=word_tokenizer)

    for tag, position, length, _ in article.named_entities:
        start_token = tokens[position]
        tokens[position] = f'<strong>{start_token}'
        end_token = tokens[position + length - 1]
        tokens[position + length - 1] = f'{end_token} ({tag})</strong>'

    content = ' '.join(tokens)

    return flask.render_template('article.html', article=article, content=content)


app.run(host='127.0.0.1', port=5001)
