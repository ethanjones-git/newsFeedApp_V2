import requests
import json
import pandas as pd

class Bing:
    def __init__(self,api_key):
        # Initalize w api key
        self.api_key= api_key

    def get_topics(self,n):
        '''
        Get trending topics from Bing API
        :param: n is top n trending topics to return from a query
        :return: returns list of topics
        '''

        # API values
        subscription_key = self.api_key
        count = n
        search_url = "https://api.bing.microsoft.com/v7.0/news/trendingtopics"

        # Structure values
        headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        params = {"count": count}

        # Make request
        response = requests.get(search_url, headers=headers, params=params)

        # Get results
        search_results = json.dumps(response.json())

        # Format results to json
        dic = json.loads(search_results)
        dic = json.dumps(dic['value'])
        dic = json.loads(dic)

        # Finalize topics as list
        topics = []
        for i in range(0,len(dic)):
            topics.append(dic[i]['name'])

        return topics

    def get_stories(self,topic):
        '''
        Provide multiple news articles for each trending topic

        :param topic:  i topic from trending topic list
        :return: lists for article, urls, img, date
        '''

        try:

            # Function parameters
            search_url = "https://api.bing.microsoft.com/v7.0/search"
            search_term = topic
            subscription_key = self.api_key

            # Api parameters
            headers = {"Ocp-Apim-Subscription-Key": subscription_key}
            params = {"q": search_term, "responseFilter": "news", "freshness": "day"}

            # Make request
            response = requests.get(search_url, headers=headers, params=params)

            # Get results
            search_results = json.dumps(response.json())

            # Format results as json
            dic = json.loads(search_results)
            dic = json.dumps(dic['news'])
            dic = json.loads(dic)

            # JSON to dataframe
            df = pd.json_normalize(dic['value'], sep='_')
            df.drop_duplicates(subset=['name'], inplace=True)

        except:
            df = None

        return df

