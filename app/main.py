import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from argparse import ArgumentParser
from datetime import datetime
import shutil

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

_ = load_dotenv()
bearer_token = os.environ.get("BEARER_TOKEN")

class TwitterAPI:
  def __init__(self, usernames, fields):
    self.usernames = usernames
    self.fields = fields

    url = self.create_userlookup_url()
    json_response = self.connect_to_user_endpoint(url)
    self.id_dict = json.loads(json.dumps(json_response, indent=4, sort_keys=True))

  def bearer_user_oauth(self, r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


  def bearer_tweets_oauth(self, r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r

  def connect_to_user_endpoint(self, url):
    response = requests.request("GET", url, auth=self.bearer_user_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

  def connect_to_endpoint(self, url, auth, params=None):
    response = requests.request("GET", url, auth=auth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


  def create_userlookup_url(self):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.

    user_fields = "user.fields=id"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format("usernames="+self.usernames, user_fields)
    return url

  def convert_to_csv(self, json_data, username):
    # Parse JSON data
    data = json.loads(json_data)

    # Convert JSON data to DataFrame
    data_df = pd.json_normalize(data['data'])

    # Save DataFrame to CSV
    data_df.to_csv(f'twitter_{username}_data.csv', index=False)

  def create_tweet_lookup_url(self, userid):
    # Replace with user ID below
    self.userid = userid
    return "https://api.twitter.com/2/users/{}/tweets".format(self.userid)

  def get_params(self, max_results=5):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": self.fields, "max_results": max_results}

  def get_tweets(self):

    username_list = self.usernames.split(',')
    for i in range(len(username_list)):
      url = self.create_tweet_lookup_url(self.id_dict['data'][i]['id'])
      params = self.get_params()
      print(params, url)
      json_response = self.connect_to_endpoint(url, self.bearer_tweets_oauth, params)
      self.convert_to_csv(json.dumps(json_response, indent=4, sort_keys=True), 'data/'+username_list[i])

      print(f'---------- Completed data extraction for {username_list[i]} ---------')




class CleanData:

  def __init__(self, filepath):
    self.filepath = filepath


  def load_data(self):
    self.data = pd.read_csv(self.filepath)
    self.data_length = len(self.data)


    return self.data

  def view_data(self):
    return self.data

  def extract_from_lists(self, col_name):
      for i in range(self.data_length):
          try:
              if '[' in self.data[col_name].iloc[i]:
                  self.data[col_name].iloc[i] = eval(self.data[col_name].iloc[i])[0]
          except:
              continue

  def extract_user_retweet(self, col_name):
      self.data['retweeted_post'] = None
      for i in range(self.data_length):
          try:
              if '[' in self.data[col_name].iloc[i]:
                  self.data['retweeted_post'].iloc[i] = eval(self.data[col_name].iloc[i])[1]
          except:
              continue

  def extract_user_impressions(self):
      for i in range(self.data_length):
          try:
              if 'count' in self.data['views'].iloc[i]:
                  self.data['views'].iloc[i] = json.loads(self.data['views'].iloc[i].replace("'", '"'))['count']
          except:
              continue

  def convert_dates(self):
      for i in range(self.data_length):
          date_string = self.data['date'].iloc[i]
          # Convert to datetime object
          date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
          # Format datetime object to the desired format
          self.data['date'].iloc[i] = date_object.strftime("%Y-%m-%d")

  def rename_columns(self):

    map = {"author_id":"user_id", "created_at": "date", "text":"tweet", "public_metrics.bookmark_count": "bookmarks",
          "public_metrics.impression_count":"impressions", "public_metrics.like_count":"likes",
          "public_metrics.quote_count":"quotes", "public_metrics.reply_count":"replies",
          "public_metrics.retweet_count":"retweets"}

    # Step 2, apply the map
    self.data = self.data.rename(columns=map)

  def filter_dates(self, start_date= '2023-06-01', end_date = '2024-05-27'):

    # Filter the dataframe
    self.data = self.data[(self.data['date'] >= start_date) & (self.data['date'] <= end_date)]

  def export_to_csv(self, path='cleaned/'):
    if not os.path.exists(path):
        # Create the directory
        os.makedirs(path)
    file_name = self.filepath.split('/')[-1]
    self.data.to_csv(os.path.join(data_directory, file_name), index=False)

def get_args():
    parser = ArgumentParser()
    parser.add_argument('--usernames', default = 'PeterObi', help = 'Should be separated by a comma, no space in between', type=str)
    parser.add_argument('--search_fields', default = "author_id,text,created_at,public_metrics", type=str)
    parser.add_argument('--clean_data', default=True, help='Set False if you don\'t want to clean the data. Default is True')
    pars = parser.parse_args()
    return pars

if __name__ == '__main__':
  
    # Load the arguments
    pars = get_args()
    data_directory = '/data'
    # Check if the directory does not exist
    if not os.path.exists(data_directory):
        # Create the directory
        os.makedirs(data_directory)
        
    # Load the API class
    api = TwitterAPI(pars.usernames, pars.search_fields)
    # Fetch the tweets for the individual user
    api.get_tweets()

    # Optional. Set clean_data argument to false if you don't want to run
    # Data Cleaning.
    if pars.clean_data == True:

        files = os.listdir(data_directory)

        # Iterate over the files and do something with each file
        for file_name in files:
            file_path = os.path.join(data_directory, file_name)
                
            # Load the class
            obj = CleanData(file_path)
            # Load the data
            obj.load_data()
            
            # convert date from timestamp to yyyy-mm-dd
            obj.convert_dates()

            ## Step 4, incase there are lists in usernames, retweets, impressions, extract for the target user

            # for likes
            obj.extract_from_lists('likes')

            # for quotes
            obj.extract_from_lists('quotes')

            # for impressions
            obj.extract_user_impressions()

            # for retweets
            obj.extract_user_retweet('user_id')

            ## save to csv file
            obj.export_to_csv()