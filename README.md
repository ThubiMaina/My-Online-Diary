# My-Online-Diary
![Coverage Status](https://coveralls.io/repos/github/ThubiMaina/My-Online-Diary/badge.svg?branch=Mydiary-v1)
[![Build Status](https://travis-ci.org/ThubiMaina/My-Online-Diary.svg?branch=Mydiary-v1)](https://travis-ci.org/ThubiMaina/My-Online-Diary)
___
![diary](https://user-images.githubusercontent.com/31989539/42674910-477c815c-867a-11e8-9241-3c76d5978f7a.jpg)

## You can access the site 
#### [here](https://thubimaina.github.io/My-Online-Diary/)

___

## My Online Diary

A diary is a record of personal experiences, thoughts and feelings. A diary can be considered as a friend you talk to and thats why most start with dear diary, . One can talk about people they meet, exciting things we do , memories of places basically every thing we encounter.
#### Note:
* Should be in first person
This app allows you to plan for your day and record all memories
___
### Prerequisites

* Python 3.4 and above
____

### Installation

clone the repo:git
```
$  git clone https://github.com/ThubiMaina/My-Online-Diary.git
```
and cd into the folder:
```
$ /MyDiary
```
create a virtual environment for the project.
```
$ virtualenv <virtualenv-name>
```
and activate virtual environment
```
$ cd virtualenv-name\Scripts\activate
```

Run the command `$ pip install -r requirements.txt` to install necessary libraries.

### Run 

To test our project on your terminal run 

* ```set FLASK_APP=run.py``` on windows
or
* ```export FLASK_APP=run.py``` on a unix environment

then

``` flask run ```

Use post man to test the endpoints this is the  [link](https://mydiar.herokuapp.com/)
* For example use [https://mydiar.herokuapp.com/api/auth/register/](https://mydiar.herokuapp.com/api/auth/register/) to register a new user

### Api Endpoints

| Endpoint | Functionality |
| -------- | ------------- |
| POST /api/auth/v1/register | Creates a user account |
| POST /api/auth/v1/login | Logs in a user |
| GET /api/v1/users | All users registered viewed by the admin |
| POST /api/v1/entries  | Adds a new diary entry |
| GET /api/v1/entries  | Gets all  diary entries |
| GET /api/v1/entries/<entry_id>  | Gets a single entry |
| PUT /api/v1/entries/<entry_id> | Updates an entry |
| DELETE /api/v1/entries/<entry_id> | Remove a diary entry |
| POST /api/v1/entries/<entry_id>/contents | Add a contents to an entry |
| GET /api/v1/entries/<entry_id>/contents | Get all contents of an entry |
