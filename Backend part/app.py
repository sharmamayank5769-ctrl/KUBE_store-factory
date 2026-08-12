from flask import Flask

app = Flask(__name__)  

from controller import *   

# routes yahan

if __name__ == '__main__':
    app.run(debug=True)