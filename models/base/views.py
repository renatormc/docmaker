from flask_app.views import views
from flask import  render_template

@views.route("/celular")
def celular():
    return render_template("celular/form.html")