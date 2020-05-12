from flask import Flask, request, render_template, redirect
from data import db_session
from data import tests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test4u_secret_key'


def main():
    global test
    db_session.global_init("db/tests.sqlite")

    test = tests.Test()

    session = db_session.create_session()
    session.commit()
    test = session.query(tests.Test).all()
    # test = request.form.get(session.query(tests.Test).all(), 'test')
    app.run()


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'GET':
        return render_template("main_window.html", test=test)
    elif request.method == 'POST':
        return redirect('/' + request.form['button_choice_test'])


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


@app.route('/<test_id>', methods=['POST', 'GET'])
def description_test(test_id):
    if request.method == 'GET':
        for item in test:
            if str(item.id) == test_id:
                return render_template('description_test_window.html', item=item)
            else:
                return render_template('error.html')
    elif request.method == 'POST':
        # создание запроса
        dec = '/decision' + '/' + test_id
        # ссылка на решение
        return redirect(dec)


@app.route('/decision/<numb>', methods=['POST', 'GET'])
def decision_test(numb):
    # numb - номер теста
    if request.method == 'GET':
        return render_template('test_system.html', QUESTION=numb, ANSWER_1=numb,
                               ANSWER_2=numb, ANSWER_3=numb, ANSWER_4=numb)
    elif request.method == 'POST':
        option = request.form['options']
        # return option
        return render_template('test_system.html', QUESTION=option, ANSWER_1=option,
                               ANSWER_2=option, ANSWER_3=option, ANSWER_4=option)


if __name__ == '__main__':
    main()
