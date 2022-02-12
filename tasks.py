from datetime import datetime
from celery import Celery
from flask_mail import Message

app = Celery('tasks', broker = 'redis://localhost:6379/0')

@app.task
def enviarCorreo(voz,mail):
    nombre = voz.nombre
    email = voz.email
    nombreConcurso = voz.concurso.nombre
    print("Inicio envio mail a {}".format(email))
    subject = "{}, tu voz ha sido procesada".format(nombre)
    msg = Message(subject, sender = 'supervoicesinfo@gmail.com', recipients = [email])
    msg.body = 'Tu voz ha sido publicada en la página del concurso {}. ¡Mucha suerte!'.format(nombreConcurso)
    mail.send(msg)
    return "Mail enviado!"

@app.task
def hola(nombre):
    return 'Hola %s' % nombre
