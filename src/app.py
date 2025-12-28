from flask import Flask

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG'] = True

# Register routes
from routes import *

if __name__ == '__main__':
    app.run()