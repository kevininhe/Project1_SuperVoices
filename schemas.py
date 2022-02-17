from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow


class AdminSchema(Schema):
    id = fields.Integer()
    email = fields.Str()
    password = fields.Str()
    nombre = fields.Str()
    apellido = fields.Str()


Admin_Schema = AdminSchema()
Admin_Schema = AdminSchema(many=True)


class ConcursoSchema(Schema):
    id = fields.Integer()
    nombre = fields.Str()
    url_imagen = fields.Str()
    url_concurso = fields.Str()
    fecha_inicio = fields.DateTime()
    fecha_fin = fields.DateTime()
    fecha_creacion = fields.DateTime()
    valor_pago = fields.Float()
    guion_voz = fields.Str()
    recomendaciones = fields.Str()
    email_admin = fields.Str()


Concurso_Schema = ConcursoSchema()
Concurso_Schema = ConcursoSchema(many=True)


class VozSchema(Schema):
    id = fields.Integer()
    email = fields.Str()
    nombre = fields.Str()
    apellido = fields.Str()
    fecha_creacion = fields.DateTime()
    procesado = fields.Boolean()
    url_voz_original = fields.Str()
    url_voz_convertida = fields.Str()
    observaciones = fields.Str()
    concurso_id = fields.Integer()

Voz_Schema = VozSchema()
Voz_Schema = VozSchema(many = True)