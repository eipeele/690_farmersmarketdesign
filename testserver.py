from flask import Flask, request, render_template, make_response
from flask.ext.restful import Api, Resource, reqparse, abort

import json
import string
import random
from datetime import datetime

# define our priority levels
#PRIORITIES = ( 'closed', 'low', 'normal', 'high' )

# load help requests data from disk
with open('data.json') as data:
    data = json.load(data)

#
# define some helper functions
#
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def error_if_produce_not_found(produce_id):
    if produce_id not in data["produce"]:
        message = "Help produce {} doesn't exist".format(produce_id)    
        abort(404, message=message)

def error_if_farmer_not_found(farmer_id):
    if farmer_id not in data["farmer"]:
        message = "Help farmer {} doesn't exist".format(farmer_id)    
        abort(404, message=message)

def filter_and_sort_farmers(q='', sort_by='time'):
   filter_function = lambda x: q.lower() in (
        x[1]['jobTitle'] + x[1]['worksFor']).lower()
   filtered_farmer = filter(filter_function,
                                  data["farmers"].items())
   key_function = lambda x: x[1][sort_by]
   return sorted(filtered_farmer, key=key_function, reverse=True)

#def filter_and_sort_produce(q='', sort_by='name'):
 #   filter_function = lambda x: q.lower() in (
  #      x[1]['releaseDate'] + x[1]['itemCondidtion']).lower()
   # filtered_produce = filter(filter_function,
    #                               data["produce"].items())
    #key_function = lambda x: x[1][sort_by]
    #return sorted(filtered_produce, key=key_function, reverse=True)
        
def render_farmer_as_html(farmer):
   return render_template(
       'data.html',
        farmer=farmer)
        #priorities=reversed(list(enumerate(PRIORITIES))))

def render_farmer_list_as_html(farmers):
    return render_template(
        'data.html',
        farmers=farmers)
    
#def render_produce_as_html(produce):
 #  return render_template(
  #      'produce.html',
   #     produce=produce
        #priorities=PRIORITIES)

def nonempty_string(x):
    s = str(x)
    if len(x) == 0:
        raise ValueError('string is empty')
    return s

#
# specify the data we need to create a new help request
#
new_farmer_parser = reqparse.RequestParser()
for arg in ['name', 'worksFor']:
    new_farmer_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

new_produce_parser = reqparse.RequestParser()
for arg in ['name', 'offers', 'releaseDate', 'itemCondition', 'sale']:
    new_farmer_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))

#
# specify the data we need to update an existing help request
#
update_farmer_parser = reqparse.RequestParser()
update_farmer_parser.add_argument(
    'name', type=str, default='')
update_farmer_parser.add_argument(
    'worksFor', type=str, default='')

update_produce_parser = reqparse.RequestParser()
update_produce_parser.add_argument(
    'name', type=str, default='')
update_produce_parser.add_argument(
    'offers', type=str, default='')
update_produce_parser.add_argument(
    'releaseDate', type=str, default='')
update_produce_parser.add_argument(
    'itemCondition', type=str, default='')
update_produce_parser.add_argument(
    'sale', type=str, default='')

#
# specify the parameters for filtering and sorting help requests
#
query_parser = reqparse.RequestParser()
query_parser.add_argument(
    'q', type=str, default='')
query_parser.add_argument(
    'sort-by', type=str, choices=('name'), default='name')
        
#
# define our (kinds of) resources
#
class Farmer(Resource):
    def get(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        return make_response(
            render_farmer_as_html(
                data["farmer"][farmer_id]), 200)

    def patch(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        farmer = data["farmer"][farmer_id]
        update = update_farmer_parser.parse_args()
        farmer['name'] = update['name']
        if len(update['worksFor'].strip()) > 0:
            farmer.setdefault('worksFor', []).append(update['worksFor'])
        return make_response(
            render_farmer_as_html(farmer), 200)

class Produce(Resource):
    def get(self, produce_id):
        error_if_produce_not_found(produce_id)
        return make_response(
            render_produce_as_html(
                data["produce"][produce_id]), 200)

    def patch(self, produce_id):
        error_if_produce_not_found(produce_id)
        produce = data["produce"][produce_id]
        update = update_produce_parser.parse_args()
        produce['name'] = update['name']
        if len(update['offers'].strip()) > 0:
            produce.setdefault('offers', []).append(update['offers'])
        return make_response(
            render_produce_as_html(produce), 200)

class FarmerAsJSON(Resource):
    def get(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        farmer = data["farmers"][farmer_id]
        #farmer["@context"] = data["@context"]
        return farmer
    
class FarmerList(Resource):
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_farmer_list_as_html(
                filter_and_sort_farmers(
                   q=query['q'], sort_by=query['sort-by'])), 200)

    def post(self):
        farmer = new_farmer_parser.parse_args()
        farmer['time'] = datetime.isoformat(datetime.now())
        farmer['worksFor'] = worksFor
        farmer[generate_id()] = farmer
        return make_response(
            render_farmer_list_as_html(
                filter_and_sort_farmer()), 201)

class FarmerListAsJSON(Resource):
    def get(self):
        return data

#
# assign URL paths to our resources
#
app = Flask(__name__)
api = Api(app)
api.add_resource(FarmerList, '/farmers')
#api.add_resource(ProduceList, '/produce')
api.add_resource(FarmerListAsJSON, '/farmers.json')
api.add_resource(Farmer, '/farmer/<string:farmer_id>')
api.add_resource(Produce, '/produce/<string:produce_id>')
api.add_resource(FarmerAsJSON, '/request/<string:farmer_id>.json')

# start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)

