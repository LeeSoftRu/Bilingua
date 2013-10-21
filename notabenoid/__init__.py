from flask import Flask, render_template, redirect, request
import urllib, codecs, re
import lees

app = Flask('bilingua')

dataFolder = r'data\notabenoid\book'

def extractBetween(text, start, end):
    return re.findall('(' + re.escape(start) + '.*?' + re.escape(end) + ')'
        , text, re.I | re.S)

def processCells(cells):
    result = []
    for idx, cell in enumerate(cells):
        cell = re.sub('\d+\.\d+\.\d+ в \d+:\d+</p>', '', cell)
        cell = cell.replace('</p>', '[/p]')
        cell = re.sub('<a.*?</a>', '', cell)
        cell = re.sub(r"\s*&middot; <span class='t1'>\d+:\d+.\d+</span> &rarr; <span class='t2'>\d+:\d+.\d+</span>"
            , '', cell)
        cell = re.sub('<.*?>', '', cell)
        cell = cell.replace('[/p]', '</p>')
        cell = re.sub('(</p>\s*)*$', '', cell, re.S)
        result.append(cell)
    return result

def extractCellsFromFile(bookId, chapterId, pageId):
    global dataFolder
    filePath = dataFolder + r'\{}\{}^\Orig_page={}' \
        .format(bookId, chapterId, pageId)
    text = codecs.open(filePath, 'r', 'utf8').read()
    text = extractBetween(text, '<table id="Tr"', '</table>')
    text = extractBetween(text[0], '<tbody', '</tbody>')

    cellsEng = extractBetween(text[0], "<td class='o'", '</td>')
    cellsRus = extractBetween(text[0], "<td class='t'", '</td>')
    cells = []
    for idx in range(0, len(cellsEng)):
        cells.append(cellsEng[idx])
        cells.append(cellsRus[idx])
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

def createUrlTo(bookId, chapterId, pageId=1, lineNo=None, column=None):
    if lineNo is None:
        if column is None:
            return '/{}/{}/{}'.format(bookId, chapterId, pageId)
        else:
            return '/{}/{}/{}/{}'.format(bookId, chapterId, pageId, column)
    return '/{}/{}/{}/{}/{}' \
        .format(bookId, chapterId, pageId, lineNo, column)

def getPageNavigation(bookId, chapterId, pageId):
    pageId = int(pageId)
    return '' \
        + '<a href="{}">Read in english</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, lineNo=0, column=0)) \
        + '<a href="{}">Read in russian</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, lineNo=0, column=1)) \
        + '<hr/>' \
        + '<a href="{}">Whole page</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId)) \
        + '<a href="{}">Whole page in english</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, column=0)) \
        + '<hr/>' \
        + '<a href="{}">Start to read next page in russian</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId + 1, lineNo=0, column=1)) \
        + '<a href="{}">Start to read next page in english</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId + 1, lineNo=0, column=0)) \
        + ''

@app.route('/')
def index():
    global dataFolder
    files = lees.Disk.findFilesRecursive(dataFolder
        , lees.Path.Filter.fullNameEquals("Orig_page=1"))
    html = "<ol>"
    for file in files:
        text = lees.File.read(file)
        title = re.findall(r"\<h1\>(.*?)\<\/h1\>", text)[0]
        title = title.replace("</a>: ", "</a>:</br>")
        title = re.sub(r'\<\/?a.*?\>', '', title)
        #print(file)
        #print(re.findall(r'\\book\\(\d+)\\(\d+)\^\\Orig_page=1', file))
        bookId, chapterId = re.findall(r'\\book\\(\d+)\\(\d+)\^\\Orig_page=1', file)[0]
        url = createUrlTo(bookId, chapterId, lineNo=0, column=1)
        html += '<li><a href="{}">{}</a><hr/>'.format(url, title)
    return html + '</ol>'

@app.route('/<bookId>/<chapterId>/<pageId>/<lineNo>/<column>')
def readPhrase(bookId, chapterId, pageId, lineNo, column):
    lineNo = int(lineNo)
    column = int(column)

    cells = extractCellsFromFile(bookId, chapterId, pageId)
    cells = [cell for idx, cell in enumerate(cells) if idx % 2 == column]
    if (lineNo > len(cells)):
        url = createUrlTo(bookId, chapterId, int(pageId))
        return redirect(url)
    return '<body style="background-color: #EEEEEE;">' \
        + '<div style="background-color: white; padding: 5px; overflow: scroll; height: 150px; font-size: 200%; border: 1px solid black;">' \
        + cells[ lineNo + 1 ] \
        + '</div>' \
        + '<br/>' \
        + '<a href="{}">Switch</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, lineNo, 0 if column else 1)) \
        + '<hr/>' \
        + '<a href="{}">Next russian</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, lineNo=lineNo+1, column=1)) \
        + '<br/>' \
        + '<a href="{}">Next english</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, lineNo=lineNo+1, column=0)) \
        + '<hr/>' \
        + '<a href="{}">Whole page in english</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId, column=0)) \
        + '<br/>' \
        + '<a href="{}">Whole page</a></br>' \
            .format(createUrlTo(bookId, chapterId, pageId)) \
        + '<hr/>' \
        + '<a href="{}">Home</a></br>' \
            .format('/') \
        + ''

@app.route('/<bookId>/<chapterId>/<pageId>/0')
def readEnglishPage(bookId, chapterId, pageId):
    cells = extractCellsFromFile(bookId, chapterId, pageId)
    cells = [cell for idx, cell in enumerate(cells) if idx % 2 == 0]
    return '' \
        + getPageNavigation(bookId, chapterId, pageId) \
        + '<hr/>' \
        + cellsToTable(cells) \
        + '<hr/>' \
        + getPageNavigation(bookId, chapterId, pageId) \
        + ''

@app.route('/<bookId>/<chapterId>/<pageId>')
def readWholePage(bookId, chapterId, pageId):
    return '' \
        + getPageNavigation(bookId, chapterId, pageId) \
        + '<hr/>' \
        + cellsToTable(extractCellsFromFile(bookId, chapterId, pageId), True) \
        + '<hr/>' \
        + getPageNavigation(bookId, chapterId, pageId) \
        + ''
