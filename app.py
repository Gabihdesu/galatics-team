from flask import Flask, render_template

app = Flask(__name__)

# Rota principal: home/index
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')


@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/3D-glob')
def globe():
    return render_template('3D-glob.html')


if __name__ == '__main__':
    app.run(debug=True)  # debug=True é útil durante desenvolvimento
