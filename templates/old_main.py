from flask import Flask, request, render_template, redirect
import json
import os

app = Flask(__name__)
GLOBAL_NUMBER_TEST = 0
GLOBAL_TEMPLATES = {}
NUMBER_QUESTIONS_CYCLE = 0
RESULT = 0

TYPE = ''
SHORT_DESCRIPTION = ''
LONG_DESCRIPTION = ''
NAME = ''
NUMBER_FINAL = 0
RETURN_NUMBER_ANSWERS = 1
NUMBER_ANSWERS = 0
ALL_ANSWERS = 0
ALL_FINAL = 0
RETURN_NUMBER_ANSWERS = 1
RETURN_NUMBER_FINAL = 1
write_to_json_file = {}
MAXIMUM_POINTS = 0


@app.route('/', methods=['POST', 'GET'])
def start():
    global GLOBAL_NUMBER_TEST
    global RESULT
    if request.method == 'GET':
        name = []
        short_description = []
        f = open('static/archive/number_tests.txt', 'r', encoding="utf-8")
        a = f.read()
        f.close()
        for i in range(1, int(a)):
            with open('static/test_' + str(i) + '/tes.json', 'r', encoding='utf-8') as f:
                templates = json.loads(f.read())
                name.append(templates['name'])
                short_description.append(templates['short_description'])
        return render_template('test.html', CYCLE=int(a), NAME=name, SHORT_DESCRIPTION=short_description)
    elif request.method == 'POST':
        GLOBAL_NUMBER_TEST = request.form['test']
        RESULT = 0
        return redirect('/test')


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


@app.route('/test', methods=['POST', 'GET'])
def tests_ok():
    global RESULT
    global GLOBAL_TEMPLATES
    global NUMBER_QUESTIONS_CYCLE
    with open('static/test_' + GLOBAL_NUMBER_TEST + '/tes.json', 'r', encoding='utf-8') as f:
        templates = json.loads(f.read())
        f.close()
    if request.method == 'GET':
        return render_template('test_description.html', DESCRIPTION=templates['full_description'])
    elif request.method == 'POST':
        if NUMBER_QUESTIONS_CYCLE == 0:
            pass
        if NUMBER_QUESTIONS_CYCLE > 0:
            option = request.form['option']
            RESULT += (int(templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['answer_' + str(option)][1]))
        if NUMBER_QUESTIONS_CYCLE != int(templates['num_question']):
            NUMBER_QUESTIONS_CYCLE += 1
            return render_template('test_system.html',
                                   QUESTION=templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['question'],
                                   ANSWER_1=templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['answer_1'][0],
                                   ANSWER_2=templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['answer_2'][0],
                                   ANSWER_3=templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['answer_3'][0],
                                   ANSWER_4=templates['question_' + str(NUMBER_QUESTIONS_CYCLE)]['answer_4'][0])
        elif NUMBER_QUESTIONS_CYCLE == int(templates['num_question']):
            if templates['add'] == 'система':
                a = templates['num_final']
                for i in range(1, int(a) + 1):
                    print(RESULT, templates['final_grade'][str(i)][0])
                    if int(RESULT) <= int(templates['final_grade'][str(i)][0]):
                        return render_template('test_final.html', RESULT=templates['final_grade'][str(i)][1],
                                               ROAD=templates['final_grade'][str(i)][2])
            else:
                a = templates['num_final']
                for i in range(1, int(a) + 1):
                    print(RESULT, templates['final_grade'][str(i)][0])
                    if int(RESULT) <= int(templates['final_grade'][str(i)][0]):
                        return render_template('test_final.html', RESULT=templates['final_grade'][str(i)][1])


@app.route('/add_test', methods=['POST', 'GET'])
def upload_file():
    global NUMBER_ANSWERS
    global TYPE
    global SHORT_DESCRIPTION
    global LONG_DESCRIPTION
    global NAME
    global NUMBER_FINAL
    global ALL_ANSWERS
    global ALL_FINAL
    global write_to_json_file
    NAME_PARAGRAPH = 'Введите название теста'
    NAME_COLOUR = 'primary'
    SHORT_DESCRIPTION_PARAGRAPH = 'Введите краткое описание теста'
    SHORT_DESCRIPTION_COLOUR = 'primary'
    LONG_DESCRIPTION_PARAGRAPH = 'Введите полное описание текста'
    LONG_DESCRIPTION_COLOUR = 'primary'
    if request.method == 'GET':
        return render_template('add_test.html', NAME_PARAGRAPH=NAME_PARAGRAPH, NAME_COLOUR=NAME_COLOUR,
                               SHORT_DESCRIPTION_PARAGRAPH=SHORT_DESCRIPTION_PARAGRAPH,
                               SHORT_DESCRIPTION_COLOUR=SHORT_DESCRIPTION_COLOUR,
                               LONG_DESCRIPTION_PARAGRAPH=LONG_DESCRIPTION_PARAGRAPH,
                               LONG_DESCRIPTION_COLOUR=LONG_DESCRIPTION_COLOUR)

    elif request.method == 'POST':
        c = 0
        if len(request.form['name']) == 0:
            NAME_PARAGRAPH = 'Вы не ввели имя'
            NAME_COLOUR = 'danger'
            c += 1
        if len(request.form['name']) > 45:
            NAME_PARAGRAPH = 'Имя не должно превышать 15 символов'
            NAME_COLOUR = 'danger'
            c += 1
        if len(request.form['short_description']) < 10:
            SHORT_DESCRIPTION_PARAGRAPH = 'Краткое описание не может быть меньше 10 символов'
            SHORT_DESCRIPTION_COLOUR = 'danger'
            c += 1
        if len(request.form['short_description']) > 80:
            SHORT_DESCRIPTION_PARAGRAPH = 'Краткое описание не должно превышать 80 символов'
            SHORT_DESCRIPTION_COLOUR = 'danger'
            c += 1
        if len(request.form['long_description']) < 20:
            print('Описание не может быть меньше 20 символов!')
            LONG_DESCRIPTION_PARAGRAPH = 'Полное описание не может быть меньше 20 символов'
            LONG_DESCRIPTION_COLOUR = 'danger'
            c += 1
        if len(request.form['long_description']) > 1000:
            LONG_DESCRIPTION_PARAGRAPH = 'Полное описание не должно превышать 1000 символов'
            LONG_DESCRIPTION_COLOUR = 'danger'
            c += 1

        if (len(request.form['name'])) > 0 and (len(request.form['name']) < 45):
            NAME_PARAGRAPH = 'success'
            NAME_COLOUR = 'success'
        if (len(request.form['short_description']) > 10) and (len(request.form['short_description']) < 80):
            SHORT_DESCRIPTION_PARAGRAPH = 'success'
            SHORT_DESCRIPTION_COLOUR = 'success'
        if (len(request.form['long_description']) > 20) and (len(request.form['long_description']) < 1000):
            LONG_DESCRIPTION_PARAGRAPH = 'success'
            LONG_DESCRIPTION_COLOUR = 'success'
        if c == 0:
            NUMBER_ANSWERS = int(request.form['inputState_0'])
            NUMBER_FINAL = int(request.form['inputState_2'])
            ALL_ANSWERS = NUMBER_ANSWERS
            ALL_FINAL = NUMBER_FINAL
            NAME = request.form['name']
            SHORT_DESCRIPTION = request.form['short_description']
            LONG_DESCRIPTION = request.form['long_description']
            TYPE = request.form['category']
            write_to_json_file['name'] = NAME
            write_to_json_file['short_description'] = SHORT_DESCRIPTION
            write_to_json_file['full_description'] = LONG_DESCRIPTION
            write_to_json_file['category'] = TYPE
            write_to_json_file['add'] = 'пользователи'

            print(write_to_json_file
                  )
            return redirect('/add_test_1')
        else:
            return render_template('add_test.html', NAME_PARAGRAPH=NAME_PARAGRAPH, NAME_COLOUR=NAME_COLOUR,
                                   SHORT_DESCRIPTION_PARAGRAPH=SHORT_DESCRIPTION_PARAGRAPH,
                                   SHORT_DESCRIPTION_COLOUR=SHORT_DESCRIPTION_COLOUR,
                                   LONG_DESCRIPTION_PARAGRAPH=LONG_DESCRIPTION_PARAGRAPH,
                                   LONG_DESCRIPTION_COLOUR=LONG_DESCRIPTION_COLOUR)


@app.route('/add_test_1', methods=['POST', 'GET'])
def add_test1():
    global write_to_json_file
    global NUMBER_ANSWERS
    global RETURN_NUMBER_ANSWERS
    global MAXIMUM_POINTS
    print(RETURN_NUMBER_ANSWERS, NUMBER_ANSWERS)
    if request.method == 'GET':
        return render_template('add_test_1.html', ALL_ANSWERS=ALL_ANSWERS,
                               RETURN_NUMBER_ANSWERS=RETURN_NUMBER_ANSWERS)

    elif request.method == 'POST':
        NUMBER_ANSWERS -= 1
        RETURN_NUMBER_ANSWERS += 1
        time_list_of_numbers_answers = []
        time_list_of_numbers_answers.append(int(request.form['inputState_1']))
        time_list_of_numbers_answers.append(int(request.form['inputState_2']))
        time_list_of_numbers_answers.append(int(request.form['inputState_3']))
        time_list_of_numbers_answers.append(int(request.form['inputState_4']))
        MAXIMUM_POINTS += max(time_list_of_numbers_answers)
        if NUMBER_ANSWERS != 0:
            a = ('question' + '_' + str(int(RETURN_NUMBER_ANSWERS - 1)))
            write_to_json_file[a] = {"answer_1": [request.form['reply_1'], request.form['inputState_1']],
                                     "answer_2": [request.form['reply_2'], request.form['inputState_2']],
                                     "answer_3": [request.form['reply_3'], request.form['inputState_3']],
                                     "answer_4": [request.form['reply_4'], request.form['inputState_4']]}
            return render_template('add_test_1.html', ALL_ANSWERS=ALL_ANSWERS,
                                   RETURN_NUMBER_ANSWERS=RETURN_NUMBER_ANSWERS)
        elif NUMBER_ANSWERS <= 0:
            RETURN_NUMBER_ANSWERS -= ALL_ANSWERS
            NUMBER_ANSWERS = ALL_ANSWERS
            write_to_json_file['final_grade'] = {}
            return redirect('/add_test_2')


@app.route('/add_test_2', methods=['POST', 'GET'])
def add_test2():
    global NUMBER_FINAL
    global RETURN_NUMBER_FINAL
    if request.method == 'GET':
        return render_template('add_test_2.html', ALL_FINAL=ALL_FINAL, RETURN_NUMBER_FINAL=RETURN_NUMBER_FINAL,
                               MAXIMUM_POINTS=MAXIMUM_POINTS)

    elif request.method == 'POST':
        NUMBER_FINAL -= 1
        RETURN_NUMBER_FINAL += 1
        write_to_json_file['final_grade'][(str(RETURN_NUMBER_ANSWERS))] = [request.form['final'],
                                                                           request.form['inputState_13']]
        if NUMBER_FINAL != 0:
            return render_template('add_test_2.html', ALL_FINAL=ALL_FINAL, RETURN_NUMBER_FINAL=RETURN_NUMBER_FINAL,
                                   MAXIMUM_POINTS=MAXIMUM_POINTS)
        elif NUMBER_FINAL <= 0:
            RETURN_NUMBER_FINAL -= ALL_FINAL
            NUMBER_FINAL = ALL_FINAL
            f = open('static/archive/number_tests.txt', 'r', encoding="utf-8")
            a = f.read()
            b = (int(a) + 1)
            f.close()
            f = open('static/archive/number_tests.txt', 'w')
            f.write(str(b))
            f.close()
            #
            m = os.getcwd()
            path = str(m) + "/static"
            os.chdir(path)
            x = 'test_' + str(b)
            x1 = 'test_' + str(b - 1)
            os.mkdir(x)
            with open(f'{x}/tes.json', 'w', encoding="utf-8") as fp:
                json.dump(write_to_json_file, fp, ensure_ascii=False)


if __name__ == '__main__':
    app.run()
