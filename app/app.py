from flask import Flask, render_template, request
from lidls import lidl
from traderjoes import traderjoes

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/secondPage', methods=['GET', 'POST'])
def secondPage():
    result = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        store_a = request.form['store_a']
        store_b = request.form['store_b']

        store_a_results = []
        store_b_results = []

        if store_a == 'traderjoes':
            store_a_results = traderjoes(user_input)
        elif store_a == 'lidl':
            store_a_results = lidl(user_input)

        if store_b == 'traderjoes':
            store_b_results = traderjoes(user_input)
        elif store_b == 'lidl':
            store_b_results = lidl(user_input)
        return render_template('secondPage.html',
                               store_a_results=store_a_results,
                               store_b_results=store_b_results)
    return render_template('secondPage.html')

@app.route('/thirdPage')
def thirdPage():
    return render_template('thirdPage.html')

if __name__ == '__main__':
    app.run(debug=True)