from flask_restful import Api
from flask import Flask

from get_number import GetNumber

app = Flask(__name__)
app.secret_key = "Matteo"
api = Api(app)

api.add_resource(GetNumber, "/main")


app.run(port=5000, debug=True)
