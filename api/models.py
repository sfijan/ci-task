from peewee import *

database = PostgresqlDatabase('citask', **{'user': 'postgres'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Player(BaseModel):
    current_club = TextField(null=True)
    dob = DateField()
    first_name = TextField()
    last_name = TextField()
    modified = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    nationality = TextField()
    player_id = AutoField()
    preffered_pos = TextField(null=True)

    class Meta:
        table_name = 'player'

