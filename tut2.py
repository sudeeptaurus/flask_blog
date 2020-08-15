from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about')
def hello_1():
    name = "harry"
    return render_template('about.html', name2 = name)

@app.route('/bootstrap')
def hello_2():
    return render_template('bootstrap.html')

app.run(debug=True)
