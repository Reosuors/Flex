import os
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Greeting (Resource):
    def get(self):
        return "YamenThon is Up & Running!"

api.add_resource(Greeting, '/')

if __name__ == "__main__":
    # Only run the Flask development server when executing this file directly.
    # When using Gunicorn (`gunicorn yeman_server:app`), this block is not executed.
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 8080))
