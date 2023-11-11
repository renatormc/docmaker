from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route("/celular")
def celular():
    return render_template("celular/form.html")