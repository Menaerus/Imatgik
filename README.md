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

However, there is a disturbing implementation detail. Since the SimpleStorage uses the local file system, there is a violation of the isolation principle when we have to tell the Flask Blueprint that its static folder is where SimpleStorage stores the images.

## Possible Continuations

This is a list of things I have left behind due to time limitations.

1. Authorization via Google
1. Password reset, in current implementation, if you forget your password the images are lost (unless the administrator does something to recover them to your new account).
1. Storage in a cloud service
1. A better look and feel of the web interface (it show my poor knowledge of Flask, or its own limitations)

## How far is it from production?

A part from the previous item considerations the app cannot be put on production with Flask web server, at least it must be put behind an Nginx (or similar). 

## Installation

A Python equiped system is required and then some Flask packages:

`python -m pip install flask`

`pip install flask-login`

Then clone the repo.

## Run
From a bash terminal use:
`FLASK_APP=. flask run`
and access `http:127.0.0.1:5000/` from your browser

## Tests
Run tests from tests/ folder.

`cd tests`

`python ./ConfigTests.py`

`python ./AuthenticatorTests.py`

`python ./StorageTests.py`
