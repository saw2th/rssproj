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
http://localhost:8000/
```

#### To see flagging
```
http://localhost:8000/admin
login
u:stephen
p:lastword
return to:
http://localhost:8000/
```

### Other things todo
 - unflag
 - improve display
 - typeahead search