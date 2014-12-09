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
with open('data_produce.json') as data_produce:
    data_produce = json.load(data_produce)
with open('data_event.json') as event:
    event = json.load(event)        

#
# define some helper functions
#
def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def error_if_produce_not_found(produce_id):
    if produce_id not in data_produce:
        message = "Help produce {} doesn't exist".format(produce_id)    
        abort(404, message=message)

def error_if_farmer_not_found(farmer_id):
    if farmer_id not in data:
        message = "Help farmer {} doesn't exist".format(farmer_id)    
        abort(404, message=message)

def error_if_event_not_found(event_id):
    if event_id not in event:
        message = "Help event {} doesn't exist".format(event_id)    
        abort(404, message=message)

def filter_and_sort_farmers(q='', sort_by='name'):
   filter_function = lambda x: q.lower() in (
        x[1]['name'] + x[1]['worksFor']).lower()
   filtered_farmer = filter(filter_function,
                                  data.items())
   key_function = lambda x: x[1][sort_by]
   return sorted(filtered_farmer, key=key_function, reverse=True)

def filter_and_sort_produces(q='', sort_by='name'):
    filter_function = lambda x: q.lower() in (
        x[1]['name'] + x[1]['itemCondition']).lower()
    filtered_produce = filter(filter_function,
                                  data_produce.items())
    key_function = lambda x: x[1][sort_by]
    return sorted(filtered_produce, key=key_function)

def filter_and_sort_events(q='', sort_by='name'):
    filter_function = lambda x: q.lower() in (
        x[1]['name'] + x[1]['organizer']).lower()
    filtered_event = filter(filter_function,
                                  event.items())
    key_function = lambda x: x[1][sort_by]
    return sorted(filtered_event, key=key_function, reverse=True)       
        
def render_farmer_as_html(farmer):
   return render_template(
       'farmer.html',
        farmer=farmer)
        #priorities=reversed(list(enumerate(PRIORITIES))))

def render_farmer_list_as_html(farmers):
    return render_template(
        'farmers.html',
        farmers=farmers)
    
def render_produce_as_html(produce):
   return render_template(
      'produce.html',
       produce=produce)
        #priorities=PRIORITIES)

def render_produce_list_as_html(produces):
    return render_template(
        'produces.html',
        produces=produces)

def render_event_as_html(event):
   return render_template(
      'event.html',
       event=event)

def render_event_list_as_html(events):
    return render_template(
        'events.html',
        events=events)

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
for arg in ['name', 'offers', 'itemCondition']:
    new_produce_parser.add_argument(
        arg, type=nonempty_string, required=True,
        help="'{}' is a required value".format(arg))
for arg in ['releaseDate', 'sale']:
    new_produce_parser.add_argument(
        arg, type=str, required=False)

new_event_parser = reqparse.RequestParser()
for arg in ['name', 'startDate']:
    new_event_parser.add_argument(
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

update_event_parser = reqparse.RequestParser()
update_event_parser.add_argument(
    'name', type=str, default='')
update_event_parser.add_argument(
    'startDate', type=str, default='')

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
                data[farmer_id]), 200)

    def patch(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        farmer = data[farmer_id]
        update = update_farmer_parser.parse_args()
        print update
        farmer['name'] = update['name']
        if len(update['worksFor'].strip()) > 0:
            farmer['worksFor'] = update['worksFor']
        return make_response(
            render_farmer_as_html(farmer), 200)

    def delete(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        farmer = data[farmer_id]
        del data[farmer_id]
        return make_response(
        render_farmer_as_html(farmer), 204)

class Produce(Resource):
    def get(self, produce_id):
        error_if_produce_not_found(produce_id)
        return make_response(
            render_produce_as_html(
                data_produce[produce_id]), 200)

    def patch(self, produce_id):
        error_if_produce_not_found(produce_id)
        produce = data_produce[produce_id]
        update = update_produce_parser.parse_args()
        print update
        produce['name'] = update['name']
        if len(update['offers'].strip()) > 0:
            produce['offers'] = update['offers']
        return make_response(
            render_produce_as_html(produce), 200)

    def delete(self, produce_id):
        error_if_produce_not_found(produce_id)
        produce = data_produce[produce_id]
        del data_produce[produce_id]
        return make_response(
        render_produce_as_html(produce), 204)

class FarmerAsJSON(Resource):
    def get(self, farmer_id):
        error_if_farmer_not_found(farmer_id)
        farmer = data['farmer'][farmer_id]
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
        farmer['name'] = name
        farmer['worksFor'] = worksFor
        farmers[generate_id()] = farmer
        return make_response(
        render_farmer_list_as_html(
        filter_and_sort_farmers()), 201)

class ProduceList(Resource):
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_produce_list_as_html(
                filter_and_sort_produces(
                   q=query['q'], sort_by=query['sort-by'])), 200)

    def post(self):
        produce = new_produce_parser.parse_args()
        data_produce[generate_id()] = produce
        return make_response(
            render_produce_list_as_html(
                filter_and_sort_produces()), 201)

class FarmerListAsJSON(Resource):
    def get(self):
        return data

class Event(Resource):
    def get(self, event_id):
        error_if_event_not_found(event_id)
        return make_response(
            render_event_as_html(
                event[event_id]), 200)

    def patch(self, event_id):
        error_if_event_not_found(event_id)
        event = data_event[event_id]
        update = update_event_parser.parse_args()
        print update
        event['name'] = update['name']
        if len(update['startDate'].strip()) > 0:
            event['startDate'] = update['startDate']
        return make_response(
            render_event_as_html(event), 200)

    def delete(self, event_id):
        error_if_event_not_found(event_id)
        event = data_event[event_id]
        del data_event[event_id]
        return make_response(
        render_event_as_html(event), 204)    

class EventList(Resource):
    def get(self):
        query = query_parser.parse_args()
        return make_response(
            render_event_list_as_html(
                filter_and_sort_events(
                   q=query['q'], sort_by=query['sort-by'])), 200)

    def put(self):
        event = new_event_parser.parse_args()
        event['name'] = name
        event['startDate'] = startDate
        event[generate_id()] = event
        return make_response(
            render_event_list_as_html(
                filter_and_sort_event()), 201)

#
# assign URL paths to our resources
#
app = Flask(__name__)
api = Api(app)
api.add_resource(FarmerList, '/farmers')
api.add_resource(ProduceList, '/produces')
api.add_resource(EventList, '/events')
api.add_resource(FarmerListAsJSON, '/farmers.json')
api.add_resource(Farmer, '/farmer/<string:farmer_id>')
api.add_resource(Produce, '/produce/<string:produce_id>')
api.add_resource(Event, '/event/<string:event_id>')
api.add_resource(FarmerAsJSON, '/request/<string:farmer_id>.json')

# start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)

