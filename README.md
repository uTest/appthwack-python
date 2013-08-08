appthwack-python
================

The official [AppThwack](https://appthwack.com) python client.

Status
======

Currently under active development.

Installation
============

### Source

    $ git clone git@github.com:appthwack/appthwack-python.git
    $ python setup.py install

### Pip

    $ pip install appthwack

Usage
=====

Configure the AppThwack client:

```python
import appthwack

API_KEY = '...'
api = appthwack.AppThwackApi(API_KEY)
```

Select a project:

```python
#...

project = api.project(id=1234)
project = api.project(name='Mutt Cuts')
projects = api.projects()
```

Select a device pool:

```python
#...

device_pool = project.device_pool(id=42)
device_pool = project.device_pool(name='72 Sheepdog')
device_pools = project.device_pools()
```

Upload your app and test content:

```python
#...

apk = api.upload('/src/samsonite.apk')
tests = api.upload('/src/gotworms.apk')
```

Schedule AppThwack AppExplorer test run:

```python
#...

name = 'Seabass and the fellas'
run = project.schedule_app_explorer_run(apk, tests, name, device_pool))
```

Schedule Calabash test run:

```python
#...

name = 'His head fell off!'
run = project.schedule_calabash_run(apk, tests, name, device_pool)
```

Schedule JUnit/Robotium test run:

```python
#...

name = 'Totally redeem yourself!'
run = project.schedule_junit_run(apk, tests, name, device_pool)
```

Get run execution status:

```python
#...

status = run.status() # new, queued, running, completed
```

Get run results:
```python
#...

results = run.results()
print results # [12345]: Run Hello World! by admin is 'completed' with result 'pass'.

```

Dependencies
============

This project was built on the shoulders of others:

*  [requests](http://docs.python-requests.org/en/latest/) by Kenneth Reitz

Documentation
=============

The latest AppThwack API documentation can be found [here](https://appthwack.com/docs/api).

Contributing
============

If you would like to contribute, simply fork the repository, push your changes and send a pull request.

License
=======

MIT License. More information can be found [here](https://github.com/appthwack/appthwack-python/blob/master/LICENSE.md).
