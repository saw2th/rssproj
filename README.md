## RSS project

### To install

```
virtualenv --python=python2.7 env
cd env
. bin/activate
git clone https://github.com/saw2th/rssproj.git rssapp
cd rssapp
pip install -r requirements.txt

python manage.py migrate
```

### Load RSS feed

```
python manage.py get_feed
python manage.py runserver
http://localhost:8000/
```

#### To see flagging
```
python manage.py createsuperuser

http://localhost:8000/admin
login
u:<username>
p:<password>
return to:
http://localhost:8000/
```

#### To run tests
```
python manage.py test
```

### Other things todo
 - unflag
 - improve display
 - typeahead search