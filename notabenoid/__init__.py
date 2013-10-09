from flask import Flask, render_template, redirect, request

app = Flask('bilingua')

@app.route('/')
def index():
    return "Hello, World"
