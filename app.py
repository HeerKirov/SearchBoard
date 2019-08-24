from flask import Flask, render_template, request, Response
from bs4 import BeautifulSoup
import json
import requests


def load_config():
    ret = {}
    with open('config.properties') as f:
        for line in f.readlines():
            splits = line.split('=', 2)
            if len(splits) >= 2:
                ret[splits[0]] = splits[1]
    return ret


def select(s, selector):
    res = s.select(selector)
    if res is not None:
        if isinstance(res, list):
            if len(res) > 0:
                return res[0]
            else:
                return None
        else:
            return res
    else:
        return None


def request_for_baidu(word, offset):
    ret = []
    res = requests.get('http://www.baidu.com/s', {'wd': word, 'pn': offset})
    soup = BeautifulSoup(res.text, 'html.parser')
    result_container = soup.select('div.result.c-container')
    for result in result_container:
        title = select(result, 'h3.t a')
        img = select(result, 'div.general_image_pic img')
        content = select(result, 'div.c-abstract')
        source = select(result, 'div.f13 a.c-showurl')
        source_span = select(source, 'span') if source is not None else None
        source_txt = source_span.text if source_span is not None else source.text if source is not None else None
        source_cert = source_span is not None
        ret.append({
            'title': title.text,
            'img': img['src'] if img is not None else None,
            'content': content.text if content is not None else None,
            'source': source_txt,
            'source_cert': source_cert if source_txt is not None else None,
            'link': title['href']
        })
    return ret


app = Flask(__name__, static_url_path='/search/static/')
config = load_config()

PREFIX = config.get('prefix', '')
DEBUG = bool(config.get('debug', 'False'))


@app.route('%s/' % (PREFIX,))
def index():
    return render_template('index.html', prefix=PREFIX)


@app.route('%s/s/' % (PREFIX,))
def search():
    word = request.args.get('word') or None
    offset = int(request.args.get('offset', 0))

    results = request_for_baidu(word, offset)
    return Response(json.dumps({
        'results': results,
        'count': len(results)
    }), mimetype='application/json')


if __name__ == '__main__':
    app.run()
