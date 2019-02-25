import datetime

from peewee import *

DATABASE = SqliteDatabase('dogs.sqlite')

class Dog(Model):
    name = CharField()
    owner = CharField()
    breed = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    ##Meta gives our class instructions on how to build our class
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Dog], safe=True)
    DATABASE.close()