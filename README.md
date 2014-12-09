690_farmersmarketdesign
=======================
The following class and rel attributes are used throughout this framework to help describe the links and forms.

#Class attributes:

  *search*:  May appear in the form class.  Describes action of form.
  
  *add_farmer*:  May appear in the form class.  Describes action of form.
  
  *add_produce*:  May appear in the form class.  Describes action of form.
  
  *add_event*:  May appear in the form class.  Describes action of form.
  
  *update-farmer*:  May appear in the form class.  Describes action of form.
  
  *update-produce*:  May appear in the form class.  Describes action of form.
  
  *update-event*:  May appear in the form class.  Describes action of form.
  
  *delete-event*:  May appear in the form class.  Describes action of form.
  
  *delete-farmer*:  May appear in the form class.  Describes action of form.
  
  *delete-produce*:  May appear in the form class.  Describes action of form.
  
  *create_inventory*:  May appear in the form class.  Describes action of form.
  
  *name*:  May appear in farm input and span class.  Describes data being inputted.
  
  *query*:  May appear in input of form class.  Describes action of form.
  
  *description*"  May appear in form input.  Describes data being inputted.
  
  *location*:  May appear in farm input.  Describes data being inputted.
  
  *add*:  May appear in input class of form.  Describes action of class.
  
  *type*:  May appear in span class.  Describes type of data.

 #Rel Attributes:

  *alternate*:  Used to describe the link as an alternate representation of the resource.

  *collection*:  Used to describe the outbound link as a group of items.
  
  *item*:  Used to describe the outbound link as an item belonging to the collection.
  
  *create-form*:  Used to describe the outbound link as one leading to a form in which information will be inputted.
  
  *anchor*:  Used to describe the outbound link as one leading to a hashed anchor tag within another page.
  

#In order to run this, you will need to do the follow:
 
  -Install [Python](https://www.python.org/)
  
  -Install [Flask](http://flask.pocoo.org/docs/0.10/installation/#installation) and [Flask-RESTful](http://flask-restful.readthedocs.org/en/latest/installation.html) (Instructions are included on the respective webpages)
  
-Download our [API](https://github.com/eipeele/690_farmersmarketdesign/archive/master.zip)

-Ensure that you have the following: 6 templates, 4 JSON files, 1 testserver.py 

-Run python testserver.py

-Add, delete, and modify different attributes via [Chrome](http://www.google.com/chrome/)
