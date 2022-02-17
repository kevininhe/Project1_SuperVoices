from flask import Flask, request
from models import db, UsuarioAdmin, Concurso, Voz
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import ffmpeg
import re
import os
from celery import Celery
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import create_acees_token, get_jwt_identity
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

from schemas import Concurso_Schema

app = Flask(__name__)
ma = Marshmallow(app)
api = Api(app)

app.config.from_object('config')

db.app = app
db.init_app(app)
mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# User----------------------------------------------------------------------------------------------------------------------------------


class ResourceSingIn(Resource):
    def post(self):
        ansDefault = "Usuario o contraseña incorrecta", 401
        usuario = UsuarioAdmin.query.filter_by(
            email=request.json["email"]).first()
        if usuario:
            if check_password_hash(
                    UsuarioAdmin.password, request.json["password"].enconde(
                        "utf-8")
            ):
                access_token = create_acees_token(
                    identity=str(usuario.id), expires_delta=timedelta(hours=1)
                )
                ansDefault = {"access_token": access_token}, 200
        return ansDefault


class ResourceSingUp(Resource):
    def post(self):
        nuevoAdmin = UsuarioAdmin(
            email=request.json["email"],
            password=generate_password_hash(
                request.json["password"].encode("utf-8")
            ).decode("utf-8"),
            nombre=request.json["nombre"],
            apellido=request.json["apellido"],
        )
        db.session.add(nuevoAdmin)
        access_token = create_acees_token(
            identity=str(nuevoAdmin.id), expires_delta=timedelta(hours=1)
        )
        return {"access_token": access_token}, 200

# Concurso------------------------------------------------------------------------------------------------------------------------------

class ResourcesConcurso(Resource):
	def get(self):
		concursos = (
			Concurso.query.filter_by(UsuarioAdmin = get_jwt_identity()).order_by(Concurso.id.desc()).items
		)
		return Concurso_Schema.dump(concursos)

# Initialize Celery
celery = Celery(
    app.name, broker=app.config['CELERY_BROKER_URL'], include=['app'])
celery.conf.update(app.config)


@celery.task
def enviarCorreo(nombre, email, nombreConcurso):
    subject = "{}, tu voz ha sido procesada".format(nombre)
    print("Inicio envio mail a {}".format(email))
    msg = Message(subject, sender='supervoicesinfo@gmail.com',
                  recipients=[email])
    msg.body = 'Tu voz ha sido publicada en la página del concurso {}. ¡Mucha suerte!'.format(
        nombreConcurso)
    with app.app_context():
        mail.send(msg)
        print("Mail enviado!")


def convertir_archivo(urlEntrada):
    print("Convirtiendo archivo {}".format(urlEntrada))
    stream = ffmpeg.input(urlEntrada)
    ruta, ext = os.path.splitext(urlEntrada)
    urlSalida = ruta + ".mp3"
    urlSalida = urlSalida.replace(
        "Archivos_Originales", "Archivos_Convertidos")
    stream = ffmpeg.output(stream, urlSalida)
    stream = ffmpeg.overwrite_output(stream)
    ffmpeg.run(stream)
    print("Archivo convertido. Ruta {}".format(urlSalida))
    return urlSalida


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
            enviarCorreo.delay(voz.nombre, voz.email, voz.concurso.nombre)


@scheduler.task('interval', id='job_process', seconds=60, misfire_grace_time=120)
def cronTask():
    with scheduler.app.app_context():
        convertir_voces.delay()


api.add_resource(ResourceSingIn, '/singIn')     
api.add_resource(ResourceSingUp, '/singUp')

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0', port=5001)
    app.run(debug=True)
