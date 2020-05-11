from flask import Flask, request, render_template, redirect
from data import db_session
from data import tests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test4u_secret_key'
begin = 1
result = 0


def main():
    global test
    db_session.global_init("db/tests.sqlite")
    session = db_session.create_session()
    test = session.query(tests.Test).all()
    # test = request.form.get(session.query(tests.Test).all(), 'test')
    app.run()


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'GET':
        return render_template("main_window.html", test=test)
    elif request.method == 'POST':
        return redirect('/' + request.form['button_choice_test'])


@app.route('/<test_id>', methods=['POST', 'GET'])
def description_test(test_id):
    if request.method == 'GET':
        for item in test:
            if str(item.id) == test_id:
                return render_template('description_test_window.html', item=item)
            else:
                pass
    elif request.method == 'POST':
        return redirect('/decision' + '/' + test_id)


@app.route('/decision/<test_id>', methods=['POST', 'GET'])
def decision_test(test_id):
    global cycle
    global begin
    global result
    test1 = ''
    if request.method == 'GET':
        for item in test:
            if str(item.id) == test_id:
                test1 = item
                cycle = item.questions['num_question']
        return render_template('decision_test_window.html',
                               QUESTION=test1.questions['question_' + str(begin)]['question'],
                               ANSWER_1=test1.questions['question_' + str(begin)]['answer_1'][0],
                               ANSWER_2=test1.questions['question_' + str(begin)]['answer_2'][0],
                               ANSWER_3=test1.questions['question_' + str(begin)]['answer_3'][0],
                               ANSWER_4=test1.questions['question_' + str(begin)]['answer_4'][0]
                               )
    elif request.method == 'POST':
        for item in test:
            if str(item.id) == test_id:
                test1 = item
                result += int(test1.questions['question_' + str(begin)]['answer_' + str(request.form['option'])][1])
                break
        if begin != int(cycle):
            begin += 1
            for item in test:
                if str(item.id) == test_id:
                    test1 = item
            return render_template('decision_test_window.html',
                                   QUESTION=test1.questions['question_' + str(begin)]['question'],
                                   ANSWER_1=test1.questions['question_' + str(begin)]['answer_1'][0],
                                   ANSWER_2=test1.questions['question_' + str(begin)]['answer_2'][0],
                                   ANSWER_3=test1.questions['question_' + str(begin)]['answer_3'][0],
                                   ANSWER_4=test1.questions['question_' + str(begin)]['answer_4'][0]
                                   )
        elif begin == int(cycle):
            for item in test:
                if str(item.id) == test_id:
                    test1 = item
            for i in range(1, len(test1.final_grade) + 1):
                if result <= test1.final_grade[str(i)][0]:
                    return render_template('final_grade_test_window.html', CONCLUSION=test1.final_grade[str(i)][1],
                                           PATH=test1.final_grade[str(i)][2])
                else:
                    pass


if __name__ == '__main__':
    main()
