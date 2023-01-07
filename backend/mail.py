from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = "i190633@nu.edu.pk"
app.config["MAIL_PASSWORD"] = "1234"
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
mail = Mail(app)


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        msg = Message(
            "FastHire",
            sender="noreply@demo.com",
            recipients=["i190633@nu.edu.pk"],
        )
        msg.body = "Dear Candidate,\n\n\nYour details have been received by us successfuly. Your information is confidential and will not be shared to anyone.\nYour interview will be conducted by using your camera and microphone. When prompted to allow camera or video click Allow. Whenever you are ready to give the interview,\nClick on this link below: \n\nhttp://localhost:3000/interview.\n\n\n\nInstructions:\n1- Click on Listen button to hear the question.\n2- Click on Record to record your response.\n3- Click on Save Answer to save your answer and see the text deteced by us.\n4-Click on Next Question to switch to the next question. Click listen button again to listen to the new question.\n5-Click on Submit to submit your answer."
        mail.send(msg)
        return render_template("emailSent.html")

    return render_template("index.html")


app.run(debug=True)
