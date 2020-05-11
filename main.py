from flask import Flask, request, render_template
from data import db_session
from data import tests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test4u_secret_key'


def main():
    global test
    db_session.global_init("db/tests.sqlite")
    session = db_session.create_session()
    test = session.query(tests.Test).all()
    app.run()


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'GET':
        return render_template("main_window.html", test=test)
    elif request.method == 'POST':
        pass


#def description_test()


if __name__ == '__main__':
    main()
