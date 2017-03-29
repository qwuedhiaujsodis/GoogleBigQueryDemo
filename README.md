# Google Big Query Demo
a simple application using Google Cloud Big Query, Webapp2 and Google Python Client Lib

## What You Need To Run
1. Because It is going to work on google You need API Key or login with Google Cloud aplication and connect it your Google Account to run the Application [Google Cloud](https://cloud.google.com/sdk/downloads)
2. Install [Google Python Client Lib](https://developers.google.com/api-client-library/python/start/installation)
```
sudo pip install --upgrade google-api-python-client
```
3. Just run the test Environment
```
dev_appserver.py app.yaml
```
**(OPTIONAL)** You may see `ImportError` for `googleapiclient`. Just go to the *project folder* and run this command:
```
sudo pip install -t lib google-api-python-client
```
