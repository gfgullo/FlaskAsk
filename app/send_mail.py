from flask_mail import Message
from flask import render_template
from flask import current_app
from app import mail


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
    msg.body = render_template(template+".txt", **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)