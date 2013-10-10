from flask import Flask, render_template, redirect, request
import urllib, codecs, re

app = Flask('bilingua')

def extractBetween(text, start, end):
    return re.findall('(' + re.escape(start) + '.*?' + re.escape(end) + ')'
        , text, re.I | re.S)

def processCells(cells):
    result = []
    for idx, cell in enumerate(cells):
        cell = re.sub('\d+\.\d+\.\d+ в \d+:\d+</p>', '', cell)
        cell = cell.replace('</p>', '[/p]')
        cell = re.sub('<a.*?</a>', '', cell)
        cell = re.sub('<.*?>', '', cell)
        cell = cell.replace('[/p]', '</p>')
        cell = re.sub('(</p>\s*)*$', '', cell, re.S)
        if cell:
            #print(cell)
            result.append(cell)
    return result

def extractCellsFromFile(bookId, chapterId, pageId):
    filePath=r'M:\cache_hc\notabenoid.com\book\{}\{}^\Orig_page={}' \
        .format(bookId, chapterId, pageId)
    text = codecs.open(filePath, 'r', 'utf8').read()
    text = extractBetween(text, '<table id="Tr"', '</table>')
    text = extractBetween(text[0], '<tbody', '</tbody>')
    cells = extractBetween(text[0], '<td', '</td>')
    return processCells(cells)

def cellsToTable(cells, boldOdd=False):
    table = '<table>'
    for idx, cell in enumerate(cells):
        table += '<tr><td style="border: 1px solid silver">' \
            + ('<b>' if boldOdd and idx % 2 == 0 else '') \
            + cell \
            + ('</b>' if boldOdd and idx % 2 == 0 else '') \
            + '</td></tr>'
    table += '</table>'
    return table

@app.route('/')
def index():
    return redirect('/24992/83961/1/1/0')

@app.route('/<bookId>/<chapterId>/<pageId>/<lineNo>/<column>')
def readWhilePage(bookId, chapterId, pageId, lineNo, column):
    return cellsToTable(extractCellsFromFile(bookId, chapterId, pageId), True)

@app.route('/<bookId>/<chapterId>/<pageId>/0')
def readEnglishPage(bookId, chapterId, pageId):
    cells = extractCellsFromFile(bookId, chapterId, pageId)
    cells = [cell for idx, cell in enumerate(cells) if idx % 2 == 0]
    return cellsToTable(cells)
