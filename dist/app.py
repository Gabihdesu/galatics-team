from flask import Flask, render_template

app = Flask(__name__)

# Rota principal: home/index
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/historia')
def historia():
    return render_template('historia.html')

@app.route('/simulador')
def simulador():
    return render_template('simulador.html')

@app.route('/equipe')
def equipe():
    return render_template('equipe.html')



if __name__ == '__main__':
    app.run(debug=True)  # debug=True é útil durante desenvolvimento
