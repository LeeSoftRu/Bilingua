from flask import Flask

app = Flask('bilingua')
from notabenoid import *
from subtitles import *
app.run(debug=True)
