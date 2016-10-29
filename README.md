# Udacity Full Stack Nanodegree Project: Item Catalog

A web application that provides a list of items within a variety of categories. Users can sign in using google sign-in and add/edit/delete Items.

This application is built using Python and the [Flask](http://flask.pocoo.org/) lightweight web framework. An sqlite database is used for storing the catalog data.

List of libraries/frameworks/APIs found in this project:
* [Flask](http://flask.pocoo.org/) A lightweight web framework for Python
* [SQLAlchemy](www.sqlalchemy.org) - Python SQL Toolkit and Object Relational Mapper
* [Bootstrap](http://getbootstrap.com/) - CSS Framework for quick and easy basic grid layout and css elements
* [Google Sign-In for Websites](https://developers.google.com/identity/sign-in/web/sign-in) - Get users into your apps quickly and securely, using a registration system they already use and trust


Instructions for running app:  
* For this project, the students were given a pre-setup Vagrant VM as their environment for running the code.  
* Here are links to [Vagrant](http://vagrantup.com/), [VirtualBox](https://www.virtualbox.org/), and the [VM repository](http://github.com/udacity/fullstack-nanodegree-vm)) for setting up the dev environment.  
* Should you choose not to use the VM, you will require Python 2.7, Flask, and SQLAlchemy installed on your system.
* To populate the database with dummy data, run the command: `python populate_db.py`
* To startup the server, run the command: `python app.py`
* The server should now be running on port 8000 of localhost. http://localhost:8000/