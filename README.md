# Imatgik

## Overview

This is a really simple web application for storing images for a set of users.

The app is writen in Python with Flask and Burma as the css provider.

I have chosen that pair because I have never used them before and I wanted the challenge of avoiding JavaScript completely.

## Arquitecture

The *client* side is rendered by a simple Flask app with 2 main views:
- Authorization and Login View (implemented with *auth* Flask Blueprint)
- Image Navigation and Editing View (implemented with *img* Flask Blueprint)

The *server* side is organized around two basic elements:
- An Authorizer and 
- A Storage

The Authorizer does login and registration (session maintenance is handled by flask-login).

The Storage keeps the images and their titles somewhere.

The overall design uses duck typing as an *abstraction* mechanism.

Both Authorizer and Storage are factorized, the app would accept any other implementation without any additional effort.

The factorization is controlled via a simple configuration class (a wrapper over a json file).

### Current Implementation 

Basic *backend* implementation consists of two classes SimpleAuthorizer and SimpleStorage, that implement the methods required as Authorizer and Storage.

SimpleAuthorizer uses a sqlite db where each method uses its own connection.

The authorization itself is made storing a cryptographically secure hash scramble of the username and password as the user id. Therefore the password is never stored anywhere.
The user id is a string, as required by Storage.

SimpleStorage uses the file system where the app is run to store all images. All images of a user are stored in a folder with the user id (provided by the Authorizer) writen as a hex number. The titles are kept in a sqlite database in each user folder.

SimpleStorage does not publish in the urls the place where images are stored. The protection is done using a 'storage' path that defers to SimpleStorage (or any other implementation) the responsability of calling Flask send_file method.

## Possible Continuations and TODOs

This is a list of things I have left behind due to time limitations.

1. Automated UI and navigation tests. Currently, automated tests only take into account the *lib* part of the app, which where the complicated programming takes place.
1. Authorization via Google.
1. Password reset, in current implementation, if you forget your password the images are lost (unless the administrator does something to recover them to your new account).
1. Storage in a cloud service.
1. A better look and feel of the web interface (it shows my poor knowledge of Flask and/or Bulma, or their own limitations).
1. Improve image loading using a buffered approach, have a window of images in the browser ready to show and update the window in the background when using the arrows.
1. Progress bar in uploading an image.

## Known issues

1. In some mobiles, uploading an image produces "File not found". No idea why yet.

## How far is it from production?

A part from the previous item considerations the app cannot be put on production with Flask web server, at least it must be put behind an Nginx (or similar). 

## Installation & Run

### Installation

A Python equiped system is required and then some Flask packages:

`python -m pip install flask`

`python -m pip install flask-login`

Then clone the repo or the other way around... You chose!

### Run
From a bash terminal use:
`FLASK_APP=. flask run`
and access `http://127.0.0.1:5000/` from your browser

Or 

`FLASK_APP=. flask run --host=0.0.0.0`
and access `http://<your-ip>:5000`

### Docker
Or you can use the Dockerfile.

## Tests
Run tests from tests/ folder.

`cd tests`

`python ./ConfigTests.py`

`python ./AuthenticatorTests.py`

`python ./StorageTests.py`
