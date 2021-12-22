from flask import Flask
from flask import request, make_response, redirect, abort, render_template


app = Flask(__name__)


users = [{'username': 'JPetrov', 'name': 'John', 'surname': 'Petrov', 'age': 19},
         {'username': 'AIvanov', 'name': 'Alex', 'surname': 'Ivanov', 'age': 21}]


@app.route('/', methods=['post', 'get'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        new_user = {'username': f'{name[0]+surname}', 'name': name, 'surname': surname, 'age': 21}
        users.append(new_user)
        # return '{} {}'.format(name, surname)
    return render_template('index.html',
                           users = users)


if __name__ == '__main__':
    app.run(debug=True)
