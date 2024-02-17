import uuid
from tortoise import fields, Tortoise
from tortoise.models import Model


class Exchanger(Model):
    uid = fields.UUIDField(pk=True, default=uuid.uuid4())
    exchanger = fields.CharField(max_length=16)
    courses: fields.ReverseRelation['Courses']


class Courses(Model):
    uid = fields.UUIDField(pk=True, default=uuid.uuid4())
    direction = fields.CharField(max_length=128)
    value = fields.FloatField()
    exchanger: fields.ForeignKeyRelation[Exchanger] = fields.ForeignKeyField('models.Exchanger', related_name='courses')
