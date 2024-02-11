import uuid

from tortoise import fields, Tortoise
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.pydantic.creator import PydanticMeta, PydanticModel


class Exchanger(Model):
    uid = fields.UUIDField(pk=True, default=uuid.uuid4())
    exchanger = fields.CharField(max_length=16)
    courses: fields.ReverseRelation['Courses']


class Courses(Model):
    uid = fields.UUIDField(pk=True, default=uuid.uuid4())
    direction = fields.CharField(max_length=128)
    value = fields.FloatField()
    exchanger: fields.ForeignKeyRelation[Exchanger] = fields.ForeignKeyField('models.Exchanger', related_name='courses')


Tortoise.init_models(["models"], "models")


class ExchangerMeta(PydanticMeta):
    include = ('exchanger', 'courses')
    exclude = ('courses__uid',)


Exchanger_Pydantic = pydantic_model_creator(Exchanger, name='Exchanger', meta_override=ExchangerMeta)

