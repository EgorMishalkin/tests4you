from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__, template_folder="templates")


@app.route('/')
def start():
    return render_template('test.html')
    # return 'start'


@app.route('/boys')
def boys():
    return render_template('boys.html')
    # return 'boys'


@app.route('/girls')
def girls():
    return render_template('girls.html')
    # return 'girls'


@app.route('/about')
def about():
    return render_template('about.html')
    # return 'about'


@app.route('/easter')
def easter():
    return render_template('easter.html')
    # return 'easter'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
