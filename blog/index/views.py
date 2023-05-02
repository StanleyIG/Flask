from flask import Blueprint, render_template
from blog.models import User

index = Blueprint("index", __name__, url_prefix="/", static_folder="../static")


@index.route("/")
def main_page():
    return render_template(
        "index.html"
    )