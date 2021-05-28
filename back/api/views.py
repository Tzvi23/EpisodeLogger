from flask import Flask

app = Flask(__name__)
@app.route('/')
def helloWorld():
    return 'Hello from flask'


if __name__ == '__main__':
    app.run()