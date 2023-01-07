from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "i190633@nu.edu.pk"
app.config["MAIL_PASSWORD"] = "Metalmgsv@5"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        msg = Message(
            "Hey", sender="noreply@demo.com", recipients=["i190633@nu.edu.pk"]
        )
        msg.body = "From my NU id MOmin"
        mail.send(msg)
        return "Sent Email!"

    return render_template("index.html")


app.run(debug=True)
