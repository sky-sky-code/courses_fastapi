import uuid

from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.pydantic.creator import PydanticMeta, PydanticModel


class Exchanger(Model):
    courser: fields.ReverseRelation['Courses']
    uid = fields.UUIDField(pk=True, default=uuid.uuid4())
    exchanger = fields.CharField(max_length=16)


class Courses(Model):
    direction = fields.CharField(max_length=128)
    value = fields.FloatField()
    exchanger: fields.ForeignKeyRelation['Exchanger'] = fields.ForeignKeyField('models.Courses', related_name='courses')


Exchanger_Pydantic = pydantic_model_creator(Exchanger, name='Excganger')
