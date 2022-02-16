from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class UsuarioAdmin(UserMixin,db.Model):
	__tablename__ = 'usuarioadmin'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	nombre = db.Column(db.String(200))
	apellido = db.Column(db.String(200))

class Concurso(db.Model):
	__tablename__ = 'concurso'
	id = db.Column(db.Integer, primary_key=True)
	nombre = db.Column(db.String(200))
	url_imagen = db.Column(db.String(300))
	url_concurso = db.Column(db.String(300))
	fecha_inicio = db.Column(db.Date())
	fecha_fin = db.Column(db.Date())
	fecha_creacion = db.Column(db.DateTime())
	valor_pago = db.Column(db.Float)
	guion_voz = db.Column(db.String(1000))
	recomendaciones = db.Column(db.String(1000))
	email_admin = db.Column(db.String(100))
	voces = db.relationship('Voz', backref='concurso',lazy='dynamic')

class Voz(db.Model):
	__tablename__ = 'voz'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100))
	nombre = db.Column(db.String(200))
	apellido = db.Column(db.String(200))
	fecha_creacion = db.Column(db.DateTime())
	procesado = db.Column(db.Boolean)
	url_voz_original = db.Column(db.String(300))
	url_voz_convertida = db.Column(db.String(300))
	observaciones = db.Column(db.String(1000))
	concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id'))
