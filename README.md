# GoogleBigQueryDemo
a simple application using Google Cloud Big Query, Webapp2 and Google Python Client Lib

## What You Need To Run
1. Because It is going to work on google You need API Key or login with Google Cloud aplication and connect it your Google Account to run the Application [Google Cloud](https://cloud.google.com/sdk/downloads)
2. Installing [Google Python Client Lib](https://developers.google.com/api-client-library/python/start/installation)
3. Install Google Api Client
```
sudo pip install --upgrade google-api-python-client
```
4. Just run the test Environment
```
dev_appserver.py app.yaml
```
**(OPTIONAL)** In the run time, `ImportError` for `googleapiclient` happens sometimes. Just go to the project Folder and Run this command:
```
sudo pip install -t lib google-api-python-client
```
