import os

from api import (
    FollowView,
    FollowViewAdd,
    LikeView,
    MediasView,
    NoneViewSelf,
    NoteView,
    UserView,
)
from flasgger import Swagger
from flask import Flask, render_template, send_from_directory
from flask_restful import Api

root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, "templates")
static_directory = os.path.join(root_dir, "static")
UPLOAD_FOLDER = os.path.join(root_dir, "static/images")


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/<path:path>")
    def send_static(path):
        return send_from_directory(static_directory, path)

    api = Api(app)
    Swagger(app, template_file="swagger.json")
    api.add_resource(UserView, "/api/users/me")
    api.add_resource(FollowView, "/api/users/<int:id>")
    api.add_resource(FollowViewAdd, "/api/users/<int:id>/follow")
    api.add_resource(NoteView, "/api/tweets")
    api.add_resource(NoneViewSelf, "/api/tweets/<int:id>")
    api.add_resource(MediasView, "/api/medias")
    api.add_resource(LikeView, "/api/tweets/<int:id>/likes")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=8000, debug=True)
