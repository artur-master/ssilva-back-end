## ssilva-backend

### requirements
- Python 3.x.y
- Postgres 9
- Virtualenv https://pypi.org/project/virtualenv/

### setup
- clone project
```
> git clone https://anhht83@bitbucket.org/avalanchaerp/ssilva-backend.git
```
- access root directory
- create virtual environment
```
> virtualenv venv
```
- acvite virtual environment
```
> source venv/scripts/activate
```
- download packages
```
> pip install -r requirements.txt
```

#### Connect database
- open file `.env`
- change `DATABASE_URL` to your db connection

#### Migrate & Seed/Fixture
```
> python data.py
```

### Start a local web server
Run follow commands
```
> source venv/scripts/activate
> python manage.py runserver
```