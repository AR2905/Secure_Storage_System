from flask import Flask

app = Flask(__name__)

from ctrl import *

app.run(debug=True)

