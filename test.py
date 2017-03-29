

import json
import googleapiclient.discovery

#================================================
#--->  SQL Queries To Big Query

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
      print lst
      return lst

getAllStoriesCount();