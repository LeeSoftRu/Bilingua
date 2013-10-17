from flask import Flask, render_template, redirect, request
import urllib, codecs, re
import lees

app = Flask('bilingua')

@app.route('/subtitles/')
def index():
    rus = lees.Disk.findFiles('./data/subtitles'
        , lees.Path.Filter.fullNameEndsWith('.rus.srt')
        , addFolder=False)
    return "<br>".join(rus)
