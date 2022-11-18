# Pator (Paramadina Tutor)

![Logo Pator](https://github.com/drdofx/pator/blob/main/pator/static/assests/images/pator.png.png?raw=True)

## Installation

**Install Flask**

Anaconda:
```
conda install -c conda-forge flask
```
Pip:
```
pip install Flask
``` 
**Clone repo**
```
git clone git@github.com:drdofx/pator.git
``` 
**Cd to repo**
```
cd pator
```
**Make .env from .env.example**
```
cp .env.example .env
```
**Input MySQL database, username, and password to .env**
**Add necessary environment variables**
```
export FLASK_APP=pator
export FLASK_ENV=development 
```
**Run init_db command**
```
flask init-db
```
**Run the application**
```
flask run
```