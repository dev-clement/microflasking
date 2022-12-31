# microflasking

The application is an End-To-End application, so far now, the only part being implemented is only the backend of the application using the micro framework Flask.
This framework has been choosen because of the fact that I actually learning it and also because of the simplicity of the back-end of the application
that needs only to have a database (with an ORM like SQLAlchemy), a routing system (using blueprint), a serializer for passing data from client to server
and the other-way-around (using Flask-Smorest package).

## Back-end

Like said earlier, the back-end of the web application is done using Flask, and written using only what is written inside of the requirements.txt file
There will more on this later on the creation of the app

## Front-end

The front-end would have been done using Flask, because Flask is using Jinja templating engine in order to create front-end inside of the blueprints (that are only used
for back-end purposes actually).

The front-end will be done using one of the following framework:
* Angular
* ReactJS
* VueJS

There will be also a Qt application in order to fetch some back-end endpoint. More on this later also.