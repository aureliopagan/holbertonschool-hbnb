from flask import Flask
from app.facade.facade import Facade

app = Flask(__name__)
facade = Facade()

@app.route('/')
def home():
    return "Welcome to the API!"

# Additional routes can be defined here

if __name__ == '__main__':
    app.run(debug=True)