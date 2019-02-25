from flask import jsonify, Blueprint, abort
#Resource class gives us our HTTP methods
##to create POST, PUT, etc. routes
# from flask_restful import Resource, Api
#new import that includes reqparse
#marshal is the function, marshal_with is a decorater
##function and decorater BOTH accomplish the same thing
##function is nice if you have to perform some other operation on data
##decorater is nice if you don't have to do anything with the data you got
from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

#reqparse lets us define fields on responses to the client
dog_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'breed': fields.String,
    'owner': fields.String
}

def dog_or_404(dog_id):
    try:
        dog = models.Dog.get(models.Dog.id == dog_id)
    except models.Dog.DoesNotExist:
        ##this send ours 404 response for us
        abort(404)
    else:
        return dog

class DogList(Resource):
    #call constructor
    def __init__(self):
        #sets up body parser
        self.reqparse = reqparse.RequestParser()
        #we can define what our requests (or even parts of it) need to look like
        self.reqparse.add_argument(
            'name',
            required=True,
            #help message is sent back whe missing info if above required=True
            help='No dog name provided',
            #location is where data is coming from
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'breed',
            required=True,
            help='No course dog breed provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No  dog owner provided',
            location=['form', 'json']
        )
        #the super is the Resource class
        super().__init__()

    def get(self):
        #loops over all dogs in our models query, creating a new list, and passing that dog to that marshal function
        #marshal function takes in objects you want to serialize, then the fields you want to serialize (that's why we define fields up at the top of this file) into JSON
        dogs = [marshal(dog, dog_fields) for dog in models.Dog.select()]
        ##old way before serializing response
        # return jsonify({'dogs': [{'name': 'Franklin'}]})
        ##new way with marshal serialized response
        return {'dogs': dogs}

    @marshal_with(dog_fields)
    def post(self):
        args = self.reqparse.parse_args()
        #print to take a look at what arts are
        print(args, 'hittingggg ')
        #** is like the spread operator in javascript, takes all the keys and turns them into variables
        #>>> mydict = {'x':1, 'y':2, 'z':3} is what ** is doing
        dog = models.Dog.create(**args)
        #old way
        # return jsonify({'dogs': [{'name': 'Franklin'}]})
        return dog

class Dog(Resource):
    #call constructor
    def __init__(self):
        #sets up body parser
        self.reqparse = reqparse.RequestParser()
        #we can define what our requests (or even parts of it) need to look like
        self.reqparse.add_argument(
            'name',
            required=False,
            #help message is sent back whe missing info if above required=True
            help='No dog name provided',
            #location is where data is coming from
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'breed',
            required=False,
            help='No course dog breed provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'owner',
            required=False,
            help='No  dog owner provided',
            location=['form', 'json']
        )
        #the super is the Resource class
        super().__init__()
        
    #putting in mock data
    #the ones that have id, it will go to routes with /:id
    @marshal_with(dog_fields)
    def get(self, id):
        #old way before marshal
        # return jsonify({'name': 'Franklin'})

        ##can define a function to find our dog or send a 404
        return dog_or_404(id)

    @marshal_with(dog_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Dog.update(**args).where(models.Dog.id==id)
        #we have to execute the update query
        query.execute()
        #old way
        # return jsonify({'name': 'Franklin'})

        #new way with marshal_with
        #just another OPTION for response
        return (models.Dog.get(models.Dog.id == id), 200)

    @marshal_with(dog_fields)
    def delete(self, id):
        query = models.Dog.delete().where(models.Dog.id==id)
        query.execute()
        #old way without marshal_with
        # return jsonify({'name': 'Franklin'})

        #new way without marshal_with
        return 'Dog was successfully deleted.'

#The basic idea of a BluePrint is that it tells our app when it's registered a record of the operations in the file to generate urls
##~ express app.use(fruitsController, /router)
##~ importing the module
dogs_api = Blueprint('resources.dogs', __name__)
#instantiates API
api = Api(dogs_api)
#adds resources and defines them on our API
api.add_resource(
    DogList,
    '/dogs',
    #can name endpoint if you want, optional
    #by default, it just lowercases whatever your class is
    endpoint='dogs'
)
api.add_resource(
    Dog,
    '/dogs/<int:id>',
    #can name endpoint if you want, optional
    #by default, it just lowercases whatever your class is
    endpoint='dog'
)