from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route('/')
def start():
    return render_template('test.html')


@app.route('/boys')
def boys():
    return render_template('boys.html')


@app.route('/girls')
def girls():
    return render_template('girls.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/easter')
def easter():
    return render_template('easter.html')


if __name__ == '__main__':
    app.run()
