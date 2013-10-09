from flask import Flask, render_template, redirect, request
import urllib, codecs, re

app = Flask('bilingua')

@app.route('/')
def index():
    return "Hello"

def extractBetween(text, start, end):
    return re.findall('(' + re.escape(start) + '.*?' + re.escape(end) + ')'
        , text, re.I | re.S)

text = codecs.open(r'M:\cache_hc\notabenoid.com\book\24992\83961', 'r', 'utf8').read()
text = extractBetween(text, '<table id="Tr"', '</table>')
text = extractBetween(text[0], '<tbody', '</tbody>')
cells = extractBetween(text[0], '<td', '</td>')
for idx, cell in enumerate(cells):
    print(idx+1, cell)
