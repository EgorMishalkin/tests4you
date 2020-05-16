from flask import Flask, request, render_template, redirect, url_for, g
from data import db_session
from data import tests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test4u_secret_key'
begin = 1
result = 0


@app.route('/', methods=['POST', 'GET'])
def start():
    global test2
    db_session.global_init("db/tests.sqlite")

    session = db_session.create_session()
    test2 = session.query(tests.Test).all()
    if request.method == 'GET':
        for name in session.query(tests.Test).filter(tests.Test.id == 1):
            print(name)
        #session.commit()
        return render_template("main_window.html", test=test2)
    elif request.method == 'POST':
        # return redirect(url_for('booking', date=date))
        return redirect('/' + request.form['button_choice_test'])


@app.route('/<test_id>', methods=['POST', 'GET'])
def description_test(test_id):
    if request.method == 'GET':
        for item in test2:
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
        for item in test2:
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
            for item in test2:
                if str(item.id) == test_id:
                    test1 = item
                    result += int(test1.questions['question_' + str(begin)]['answer_' + str(request.form['option'])][1])
                    break
            if begin != int(cycle):
                begin += 1
                for item in test2:
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
                for item in test2:
                    if str(item.id) == test_id:
                        test1 = item
                for i in range(1, len(test1.final_grade) + 1):
                    begin = 1
                    if result <= test1.final_grade[str(i)][0]:
                        CONCLUSION = test1.final_grade[str(i)][1]
                        PATH = test1.final_grade[str(i)][2]
                        result = 0
                        return redirect(url_for('final_result', CONCLUSION=CONCLUSION, PATH=PATH))
                    else:
                        pass
        else:
            for item in test2:
                if str(item.id) == test_id:
                    test1 = item
            return render_template('decision_test_window.html',
                                   QUESTION=test1.questions['question_' + str(begin)]['question'],
                                   ANSWER_1=test1.questions['question_' + str(begin)]['answer_1'][0],
                                   ANSWER_2=test1.questions['question_' + str(begin)]['answer_2'][0],
                                   ANSWER_3=test1.questions['question_' + str(begin)]['answer_3'][0],
                                   ANSWER_4=test1.questions['question_' + str(begin)]['answer_4'][0]
                                   )


@app.route('/final_result')
def final_result():
    CONCLUSION = request.args.get('CONCLUSION', None)
    PATH = request.args.get('PATH', None)
    return render_template('final_grade_test_window.html', CONCLUSION=CONCLUSION, PATH=PATH)


@app.route('/add_test', methods=['POST', 'GET'])
def add_test():
    if request.method == 'GET':
        return render_template('add_test_window.html', NAME_PARAGRAPH='Введите название теста',
                               SHORT_DESCRIPTION_PARAGRAPH='Введите краткое описание теста',
                               LONG_DESCRIPTION_PARAGRAPH='Введите полное описаниетеста')
    elif request.method == 'POST':
        num_ques = request.form.get('inputState_0')
        num_fin = request.form.get('inputState_2')
        name = request.form.get('name')
        short_description = request.form.get('short_description')
        long_description = request.form.get('long_description')
        category = request.form.get('category')
        return redirect(
            url_for('add_test_1', num_ques=num_ques, num_fin=num_fin, name=name, short_description=short_description,
                    long_description=long_description, category=category))


@app.route('/add_test_1', methods=['POST', 'GET'])
def add_test_1():
    name = request.args.get('name', None)
    num_ques = request.args.get('num_ques', None)
    num_fin = request.args.get('num_fin', None)
    short_description = request.args.get('short_description', None)
    long_description = request.args.get('long_description', None)
    category = request.args.get('category', None)
    add_data_questions = {}
    add_data_final = {}
    if request.method == 'GET':
        return render_template('add_test_1_window.html', NUM_QUES=int(num_ques), NUM_FIN=int(num_fin))
    elif request.method == 'POST':
        # add_data_questions['cover'] = 'static/preview/1.png'
        # add_data_questions['name'] = str(name)
        # add_data_questions['short_description'] = str(short_description)
        # add_data_questions['long_description'] = str(long_description)
        # add_data_questions['category'] = str(category)
        # add_data_questions['add'] = 'пользователи'
        add_data_questions['num_question'] = num_ques
        for i in range(1, int(num_ques) + 1):
            add_data_questions['question_' + str(i)] = {}
            add_data_questions['question_' + str(i)]['question'] = request.form['question_' + str(i)]
            add_data_questions['question_' + str(i)]['answer_1'] = [request.form['reply_1_' + str(i)],
                                                                    int(request.form[
                                                                            'inputState_1_' + str(i)])]
            add_data_questions['question_' + str(i)]['answer_2'] = [request.form['reply_2_' + str(i)],
                                                                    int(request.form[
                                                                            'inputState_2_' + str(i)])]
            add_data_questions['question_' + str(i)]['answer_3'] = [request.form['reply_3_' + str(i)],
                                                                    int(request.form[
                                                                            'inputState_3_' + str(i)])]
            add_data_questions['question_' + str(i)]['answer_4'] = [request.form['reply_4_' + str(i)],
                                                                    int(request.form[
                                                                            'inputState_4_' + str(i)])]

            # print(request.form['reply_1_' + str(i)], request.form['inputState_1_' + str(i)])
            # print(request.form['reply_2_' + str(i)], request.form['inputState_2_' + str(i)])
            # print(request.form['reply_3_' + str(i)], request.form['inputState_3_' + str(i)])
            # print(request.form['reply_4_' + str(i)], request.form['inputState_4_' + str(i)])
        # print(add_data_questions)
        for i in range(1, int(num_fin) + 1):
            add_data_final[str(i)] = [int(request.form['final_state_' + str(i)]), request.form['final_' + str(i)],
                                      'static/preview/2.png']
            # print(request.form['final_' + str(i)], request.form['final_state_' + str(i)])
        add_test_in_sql(name, short_description, long_description, category, add_data_questions, add_data_final)
        return redirect('/')


def add_test_in_sql(name, short_description, long_description, category, add_data_questions, add_data_final):
    db_session.global_init("db/tests.sqlite")
    print('Добавление теста в базу данных...')
    test = tests.Test()
    test.cover = 'static/preview/1.png'
    test.name = name
    test.short_description = short_description
    test.long_description = long_description
    test.category = category
    test.add = 'пользователи'
    test.questions = add_data_questions
    test.final_grade = add_data_final

    session = db_session.create_session()
    session.add(test)
    session.commit()

    print('Тест успешно добавлен')


@app.route('/boys', methods=['POST', 'GET'])
def boys():
    if request.method == 'GET':
        return render_template('boys.html', test=test2)
    elif request.method == 'POST':
        # return redirect(url_for('booking', date=date))
        return redirect('/' + request.form['button_choice_test'])


@app.route('/girls', methods=['POST', 'GET'])
def girls():
    if request.method == 'GET':
        return render_template('girls.html', test=test2)
    elif request.method == 'POST':
        # return redirect(url_for('booking', date=date))
        return redirect('/' + request.form['button_choice_test'])


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        return render_template('users.html', test=test2)
    elif request.method == 'POST':
        # return redirect(url_for('booking', date=date))
        return redirect('/' + request.form['button_choice_test'])


@app.route('/easter')
def easter():
    return render_template('easter.html')


if __name__ == '__main__':
    app.run(debug=True)
