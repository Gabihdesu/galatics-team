from flask import Flask, render_template

app = Flask(__name__)

# Rota principal: home/index
@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

if __name__ == '__main__':
    app.run(debug=True)  # debug=True é útil durante desenvolvimento
