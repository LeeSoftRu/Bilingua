from flask import Flask

app = Flask('bilingua')
from notabenoid import *
app.run(debug=True)
