from tortoise import fields
from tortoise.models import Model


class Rate(Model):
    id = fields.IntField(pk=True)
    date = fields.DateField()
    cargo_type = fields.CharField(max_length=255)
    rate = fields.DecimalField(max_digits=10, decimal_places=2)
