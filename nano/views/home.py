from flask import Flask, Blueprint, render_template, abort
from jinja2 import TemplateNotFound

home = Blueprint("home", __name__)

@home.route("/", methods=["GET"])
def show():
    return render_template("home/index.html")

