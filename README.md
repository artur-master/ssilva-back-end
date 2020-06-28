# ssilva-backend

## requirements
- Python 3.x.y
- Postgres 9
- Virtualenv https://pypi.org/project/virtualenv/

## setup
```
- access root directory
- create virtual environment
```
> virtualenv venv
```
- acvite virtual environment
```
For window
> source venv/scripts/activate

For MacOS or *nix 
> source venv/bin/activate
```
- install packages
```
> pip install -r requirements.txt
```

### Connect database
- copy and replace `sgi_web_back_project/.env.sample` file to `sgi_web_back_project/.env` file
- change `DATABASE_URL` to your db connection

### Migrate & Seed/Fixture (Create database and import sample data)
```
> python data.py
```

## Start a local web server
Run follow commands
```
> source venv/scripts/activate
> python manage.py runserver
```

- Base API endpoint: htp://<root app>/api
- Admin: htp://<root app>/admin  
