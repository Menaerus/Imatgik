# Imatgik

## Overview

This is a really simple application for storing images for a set of users.

The app is writen in Python and Flask.

I have chosen that pair because I have never used them before and I wanted the challenge of avoiding JavaScript at all.

## Arquitecture

The *client* side is rendered by a simple Flask app with 2 main views:
- Authorization and Login View
- Image Navigation and Editing View

The *server* side is organized around two basic elements:
- An Authorizer and 
- A Storage

The Authorizer does login and registration (session maintenance is handled by flask-login).

The Storage keeps the images somewhere.

The overall design uses duck typing as an *abstraction* mechanism.

Both Authorizer and Storage are factorized, the app would accept any other implementation without any additional effort.

The factorization is controlled via a simple configuration class (a wrapper over a json file).

### Implementation details

The SimpleAuthorizer uses a sqlite db where each action uses its own connection.

The authorization itself is made storing a cryptographically secure hash scramble of the username and password as the user id. Therefore the password is never stored anywhere.

The SimpleStorage uses the file system where the app is run to store all images. All images of a user are stored in a folder with the user id (provided by the Authorizer) writen as a hex number.

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
