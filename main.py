from flask import Flask, request, render_template, redirect, url_for, g
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
        #return redirect(url_for('booking', date=date))
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
        if 'option' in request.form:
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
                    begin = 1
                    result = 0
                    if result <= test1.final_grade[str(i)][0]:
                        return render_template('final_grade_test_window.html', CONCLUSION=test1.final_grade[str(i)][1],
                                               PATH=test1.final_grade[str(i)][2])
                    else:
                        pass
        else:
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


@app.route('/add_test', methods=['POST', 'GET'])
def add_test():
    if request.method == 'GET':
        return render_template('add_test_window.html', NAME_PARAGRAPH='Введите название теста',
                               SHORT_DESCRIPTION_PARAGRAPH='Введите краткое описание теста',
                               LONG_DESCRIPTION_PARAGRAPH='Введите полное описаниетеста')
    elif request.method == 'POST':
        print(request.form['name'], request.form['short_description'], request.form['long_description'],
              request.form['inputState_0'], request.form['category'], request.form['inputState_2'])
        num_ques = request.form.get('inputState_0')
        num_fin = request.form.get('inputState_2')
        return redirect(url_for('add_test_1', num_ques=num_ques, num_fin=num_fin))


@app.route('/add_test_1', methods=['POST', 'GET'])
def add_test_1():
    num_ques = request.args.get('num_ques', None)
    num_fin = request.args.get('num_fin', None)
    if request.method == 'GET':
        return render_template('add_test_1_window.html', NUM_QUES=int(num_ques), NUM_FIN=int(num_fin))
    elif request.method == 'POST':
        for i in range(1, int(num_ques) + 1):
            print(request.form['question_' + str(i)])
            print(request.form['reply_1_' + str(i)], request.form['inputState_1_' + str(i)])
            print(request.form['reply_2_' + str(i)], request.form['inputState_2_' + str(i)])
            print(request.form['reply_3_' + str(i)], request.form['inputState_3_' + str(i)])
            print(request.form['reply_4_' + str(i)], request.form['inputState_4_' + str(i)])
        for i in range(1, int(num_fin) + 1):
            print(request.form['final_' + str(i)], request.form['final_state_' + str(i)])

            
@app.route('/search/<result>', methods=['POST', 'GET'])
def search(result):
    global test
    print(test)
    results = []
    times = 0
    for i in result.split():
        for n in test:
            if i.lower() in n.name.lower():
                results.append(n.name)
                times += 1
    # results = search_bd(result)
    if request.method == 'GET':
        return render_template("search.html", SEARCH=result, VALUE=str(times), test=test)
        # return str(times)
        # return '</br>'.join(results)
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


if __name__ == '__main__':
    main()
