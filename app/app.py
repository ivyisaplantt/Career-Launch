from flask import Flask, render_template, request
from lidls import scrape_product_info

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/secondPage', methods=['GET', 'POST'])
def secondPage():
    result = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        result = scrape_product_info(user_input)
        return render_template('secondPage.html', result=result)
    return render_template('secondPage.html')

@app.route('/thirdPage')
def thirdPage():
    return render_template('thirdPage.html')

if __name__ == '__main__':
    app.run(debug=True)