from flask import Flask
from models import db, UsuarioAdmin, Concurso, Voz
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import ffmpeg
import re, os
from celery import Celery

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kevin:A$QLPa55wordForK@172.24.41.201/VoicesProject'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'supervoicesinfo@gmail.com'
app.config['MAIL_PASSWORD'] = 'JHJ4N4Sk64pAzsg'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'

db.app = app
db.init_app(app)
mail= Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'],include=['app'])
celery.conf.update(app.config)

@celery.task
def enviarCorreo(nombre,email,nombreConcurso):
	subject = "{}, tu voz ha sido procesada".format(nombre)
	print("Inicio envio mail a {}".format(email))
	msg = Message(subject, sender = 'supervoicesinfo@gmail.com', recipients = [email])
	msg.body = 'Tu voz ha sido publicada en la página del concurso {}. ¡Mucha suerte!'.format(nombreConcurso)
	with app.app_context():
		mail.send(msg)
		print("Mail enviado!")

def convertir_archivo(urlEntrada):
	print("Convirtiendo archivo {}".format(urlEntrada))
	stream = ffmpeg.input(urlEntrada)
	ruta, ext = os.path.splitext(urlEntrada)
	urlSalida = ruta + ".mp3"
	urlSalida = urlSalida.replace("Archivos_Originales","Archivos_Convertidos")
	stream = ffmpeg.output(stream, urlSalida)
	stream = ffmpeg.overwrite_output(stream)
	ffmpeg.run(stream)
	print("Archivo convertido. Ruta {}".format(urlSalida))

@celery.task
def convertir_voces():
	with app.app_context():
		vocesAProcesar = Voz.query.filter_by(procesado=False).all()
		for voz in vocesAProcesar:
			print("Inicio conversion de voz de {}".format(voz.email))
			urlSalida = convertir_archivo(voz.url_voz_original)
			voz.procesado = True
			voz.url_voz_convertida = urlSalida
			db.session.commit()
			enviarCorreo.delay(voz.nombre,voz.email,voz.concurso.nombre)

@scheduler.task('interval', id='job_process', seconds=60, misfire_grace_time=120)
def cronTask():
	with scheduler.app.app_context():
		convertir_voces.delay()

if __name__ == '__main__':
	app.run(debug=True)
