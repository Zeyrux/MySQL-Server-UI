import secrets
import os

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from application.Database import Database


CLOSE_WINDOW = "<script>window.onload = window.close();</script>"


class App:
    def __init__(self) -> None:
        self.app = Flask(__name__)
        self.app.secret_key = secrets.token_urlsafe(16)
        self.app.config["SESSION_TYPE"] = "filesystem"
        self.app.config["UPLOAD_FOLDER"] = os.path.join(
            "application", "upload")
        if not os.path.isdir(self.app.config["UPLOAD_FOLDER"]):
            os.mkdir(self.app.config["UPLOAD_FOLDER"])
        self.database = Database()
        self.register_routes()

    def register_routes(self):
        @self.app.route("/", methods=["GET"])
        def login():
            return render_template("login.html")

        @self.app.route("/login", methods=["GET"])
        def save_login():
            self.database.connect(request.args["database"])
            return redirect(url_for("homepage"))

        @self.app.route("/create_database", methods=["GET"])
        def create_database():
            self.database.create_new_database(request.args["database"])
            return redirect(url_for("homepage"))

        @self.app.route("/homepage", methods=["GET"])
        def homepage():
            return render_template("homepage.html")

        @self.app.route("/text_sql", methods=["GET"])
        def text():
            text = request.args["text"]
            fetch_one = True if "fetch_one" in request.args else False
            response = self.database.execute_text(text, fetch_one)
            return redirect(url_for("homepage", response=response))

        @self.app.route("/file_sql", methods=["POST"])
        def file():
            fetch_one = True if "fetch_one" in request.args else False
            file = request.files["file"]
            filename = secure_filename(file.filename)
            filepath = os.path.join(
                self.app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            response = self.database.execute_file(
                filepath, fetch_one=fetch_one)
            os.remove(filepath)
            return redirect(url_for("homepage", response=response))
