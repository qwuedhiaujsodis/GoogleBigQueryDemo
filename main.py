
from __future__ import absolute_import
import cgi
import datetime
import urllib
import wsgiref.handlers
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import webapp2
import json
import googleapiclient.discovery

#================================================
#--->  SQL ti BigQuery ...

# [START sync_query]
def sync_query(
        bigquery, query, project_id='hacknews-freelance', 
        timeout=10000, num_retries=5, use_legacy_sql=False):
    query_data = {
        'query': query,
        'timeoutMs': timeout,
        'useLegacySql': use_legacy_sql
    }
    return bigquery.jobs().query(
        projectId=project_id,
        body=query_data).execute(num_retries=num_retries)
# [END sync_query]
def getAllStoriesCount():
      query = '''
        #standardSQL
        SELECT
            count(*)
        FROM
            `bigquery-public-data.hacker_news.stories`;
      '''
      bigquery = googleapiclient.discovery.build('bigquery', 'v2', developerKey= "_API_KEY_")
      query_job = sync_query(bigquery, query)
      page = bigquery.jobs().getQueryResults(**query_job['jobReference']).execute(num_retries=2)
      results = []
      results.extend(page.get('rows', []))
      #print results[0]['f'][0]['v']
      return results[0]['f'][0]['v']

def getLeastScoreTitle():
      query = '''
        #standardSQL
        SELECT
        title
        FROM
        `bigquery-public-data.hacker_news.stories`
        ORDER BY score
        LIMIT 1;
      '''
      bigquery = googleapiclient.discovery.build('bigquery', 'v2')
      query_job = sync_query(bigquery, query)
      page = bigquery.jobs().getQueryResults(**query_job['jobReference']).execute(num_retries=2)
      results = []
      results.extend(page.get('rows', []))
      #print results[0]['f'][0]['v']
      return results[0]['f'][0]['v']

def getMostWantedNewsIn2010():
      query = '''
        #standardSQL
        SELECT
        url
        FROM
        `bigquery-public-data.hacker_news.stories`
        WHERE
        time_ts >= '2010-01-01' AND time_ts <= '2010-12-30'

        ORDER BY score DESC
        limit 1;
      '''
      bigquery = googleapiclient.discovery.build('bigquery', 'v2')
      query_job = sync_query(bigquery, query)
      page = bigquery.jobs().getQueryResults(**query_job['jobReference']).execute(num_retries=2)
      results = []
      results.extend(page.get('rows', []))
      #print results[0]['f'][0]['v']
      return results[0]['f'][0]['v']

def getNyWiCount():
      query = '''
        #standardSQL
        SELECT
        Count(url)
        FROM
        `bigquery-public-data.hacker_news.stories`
        WHERE
        url like '%nytimes.com%'
      '''
      bigquery = googleapiclient.discovery.build('bigquery', 'v2')
      query_job = sync_query(bigquery, query)
      page = bigquery.jobs().getQueryResults(**query_job['jobReference']).execute(num_retries=2)
      results = []
      results.extend(page.get('rows', []))
      ny = results[0]['f'][0]['v']
      query = '''
        #standardSQL
        SELECT
        Count(url)
        FROM
        `bigquery-public-data.hacker_news.stories`
        WHERE
        url like '%wired.com%'
      '''
      bigquery = googleapiclient.discovery.build('bigquery', 'v2')
      query_job = sync_query(bigquery, query)
      page = bigquery.jobs().getQueryResults(**query_job['jobReference']).execute(num_retries=2)
      results = []
      results.extend(page.get('rows', []))
      wi = results[0]['f'][0]['v']
      lst = [ny, wi]
      return lst

# ===========================================================
#    DB Models...

class Table_A(db.Model):
      StoriCount = db.IntegerProperty()
      date = db.DateTimeProperty(auto_now_add=True)

def TableA_key(name=None):
      return db.Key.from_path('TableA', name or 'default')

class Table_B(db.Model):
      StoryTitle = db.StringProperty()
      date = db.DateTimeProperty(auto_now_add=True)

def TableB_key(name=None):
      return db.Key.from_path('TableB', name or 'default')

class Table_C(db.Model):
      BestStory = db.StringProperty()
      date = db.DateTimeProperty(auto_now_add=True)

def TableC_key(name=None):
      return db.Key.from_path('TableC', name or 'default')

class Table_D(db.Model):
      NYTimes = db.StringProperty()
      Wired = db.StringProperty()
      date = db.DateTimeProperty(auto_now_add=True)

def TableD_key(name=None):
      return db.Key.from_path('TableD', name or 'default')

# ============================================================
# Main Page Loader ...


class MainPage(webapp2.RequestHandler):
    def get(self):
        guestbook_name=self.request.get('guestbook_name')
        greetings_query = Greeting.all().ancestor(
            guestbook_key(guestbook_name)).order('-date')
        greetings = greetings_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
        AllStoriesCount = getAllStoriesCount()
        LeastScoreTitle = getLeastScoreTitle()
        MostWanted2010 = getMostWantedNewsIn2010()
        nyWiCount = getNyWiCount()
        SaveToDB(AllStoriesCount, LeastScoreTitle, MostWanted2010, nyWiCount)
        template_values = {
            'storiesCount' : AllStoriesCount,
            'leastScoreTitle' : LeastScoreTitle,
            'mostWanted2010' : MostWanted2010,
            'nyWiCount' : nyWiCount
        }

        path = os.path.join(os.path.join(os.path.dirname(__file__), 'html') , 'index.html')
        self.response.out.write(template.render(path, template_values))

def SaveToDB(AllStoriesCount, LeastScoreTitle, MostWanted2010, nyWiCount):
      tA = Table_A(parent=TableA_key(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))))
      tA.StoriCount = int(AllStoriesCount)
      tA.put()
      tB = Table_B(parent=TableB_key(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))))
      tB.StoryTitle = LeastScoreTitle
      tB.put()
      tC = Table_C(parent=TableC_key(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))))
      tC.BestStory = MostWanted2010
      tC.put()
      tD = Table_D(parent=TableD_key(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))))
      tD.NYTimes = int(nyWiCount[0])
      tD.Wired = int(nyWiCount[1])
      tD.put()
      




application = webapp2.WSGIApplication([
    ('/', MainPage),
  ],
  debug=True
)


def main():
  application.RUN()


if __name__ == '__main__':
  main()