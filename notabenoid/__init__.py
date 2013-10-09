from flask import Flask, render_template, redirect, request
import urllib, codecs, re

app = Flask('bilingua')

@app.route('/')
def index():
    return "Hello"

page = codecs.open(r'M:\cache_hc\notabenoid.com\book\24992\83961', 'r', 'utf8').read()
table = re.findall(r'(<table id="Tr".*?</table>)', page, re.I | re.S)
print(table)


