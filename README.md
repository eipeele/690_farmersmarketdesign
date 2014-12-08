690_farmersmarketdesign
=======================

Done in fulfillment of assignment 3 for INLS 690.

#Class attributes:

  *search*:  May appear in the form class.  Describes action of form.
  
  *create_farmerslisting*:  May appear in the form class.  Describes action of form.
  
  *update_inventory*:  May appear in the form class.  Describes action of form.
  
  *create_inventory*:  May appear in the form class.  Describes action of form.
  
  *name*:  May appear in farm input and span class.  Describes data being inputted.
  
  *location*:  May appear in farm input.  Describes data being inputted.
  
  *inventory*:  May appear in ol list.  Describes type of list.
  
  *farmer*:  May appear in li class.  Describes what is being inputted.
  
  *produce*:  May appear in ul class.  Describes type of data.
  
  *fruit*:  May appear in li class.  Describes type of data.
  
  *type*:  May appear in span class.  Describes type of data.
  
  *amount*:  May appear in span class.  Describes type of data.
  
  *price*:  May appear in span class.  Describes type of data.
  
  *vegetable*:  May appear in li class.  Describes type of data.
  
  *directory*:  May appear in ol class.  Describes type of list.
  
  *results*:  May appear in ol class.  Describes type of list.
  
  *resultone*, *resulttwo*, *resultthree*:  May appear in li class.  Orders search result data.

#Rel Attributes:

  *index*:  Used to describe the outbound link as one leading to a listing of items.
  
  *create-form*:  Used to describe the outbound link as one leading to a form in which information will be inputted.
  
  *anchor*:  Used to describe the outbound link as one leading to a hashed anchor tag within another page.
  

 #In order to run this, you will need to do the follow:
  
  -Install [Python](https://www.python.org/)
  
  -Install [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation) and [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) (Instructions are included on the respective webpages)
  
-Download our [API](https://github.com/eipeele/690_farmersmarketdesign/archive/master.zip)

-Ensure that you have the following: 6 templates, 4 JSON files, 1 testserver.py 

-Run python testserver.py

-Add, delete, and modify different attributes via [Chrome](http://www.google.com/chrome/)
