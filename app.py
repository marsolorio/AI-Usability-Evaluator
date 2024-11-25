from flask import Flask, render_template, request
from some_module import evaluate_website  # Replace with your actual evaluation function

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    url = request.form['url']
    evaluation_result = evaluate_website(url)  # This should return a dictionary
    return render_template('result.html', result=evaluation_result)

if __name__ == "__main__":
    app.run(debug=True)
