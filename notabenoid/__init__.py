from flask import Flask, render_template, redirect, request
import urllib, codecs, re

app = Flask('bilingua')

def extractBetween(text, start, end):
    return re.findall('(' + re.escape(start) + '.*?' + re.escape(end) + ')'
        , text, re.I | re.S)

@app.route('/')
def index():
    text = codecs.open(r'M:\cache_hc\notabenoid.com\book\24992\83961', 'r', 'utf8').read()
    text = extractBetween(text, '<table id="Tr"', '</table>')
    text = extractBetween(text[0], '<tbody', '</tbody>')
    cells = extractBetween(text[0], '<td', '</td>')

    page = '<table border=1>'
    for idx, cell in enumerate(cells):
        cell = re.sub('\d+\.\d+\.\d+ в \d+:\d+</p>', '', cell)
        cell = cell.replace('</p>', '[/p]')
        cell = re.sub('<a.*?</a>', '', cell)
        cell = re.sub('<.*?>', '', cell)
        cell = cell.replace('[/p]', '</p>')
        cell = re.sub('(</p>\s*)*$', '', cell, re.S)

        if not cell:
            continue

        print(cell)

        page += '<tr><td>' + cell + '</td></tr>'
    page += '</table>'

    return page
