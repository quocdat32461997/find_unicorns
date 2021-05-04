# engine.py

# import dependencies
import json
import requests

class Engine(object):
    def __init__(self):
        with open('api_keys.json') as file:
            keys = json.load(file)
            print(keys)
            self.google_api = keys['google']['api']
            self.google_engine_id = keys['google']['engine_id'] 
            self.bing_api = keys['bing']['api']
            self.bing_sub_key = keys['bing']['subscription_key']

        self.google_page = 1

    def search(self, query):
        """
        Retrieve documents given query 
        Args:
            query : str
                Query input
        Returns:
            outputs : list of str
                List of docs
        """

        return query

    def _google_parse(self, inputs):
        """
        Parse search results
        Args:
            inputs : JSON object
        Returns:
            outputs : list of tuples
        """
        inputs = inputs.get('items')
        outputs = [{'title' : item.get('title'), 'description' : item.get('snippet'), 'link' : item.get('link')} for item in inputs]

        return outputs

    def google(self, query):
        """
        Retrieve websites given query by Gooogle API
        Args:
            query : str
                Query input
        Returns:
            outputs : list of tuples
                Lists of tuples: (title, description, link)
        """
        # configur url
        start = (self.google_page - 1) * 50 + 1 # get 50 at a time
        url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}".format(self.google_api, self.google_engine_id, query, start)

        # make search requests
        outputs = requests.get(url).json()

        # parse search results
        outputs = self._google_parse(outputs)

        return outputs

    def _bing_parse(self, inputs):
        """
        Parse search resluts
        Args:
            inputs : JSON object
        Returns:
            outputs : list of tuples
        """
        outputs = inputs.get('webPages')['value']
        outputs = [{'title' : item.get('name'), 'description' : item.get('snippet'), 'link' : item.get('url')} for item in outputs]
        return outputs

    def bing(self, query):
        """
        Retrieve websites given query by Bing API
        Args:
            query : str
                Query input
        Returns:
            outputs : list of str
                List of docs
        """
        # configure url
        url = "https://api.bing.microsoft.com/v7.0/custom/search?q={}&customconfig={}".format(query, self.bing_api)

        # make search requests
        outputs = requests.get(url,
                headers={'Ocp-Apim-Subscription-Key': self.bing_sub_key}).json()

        # parse search resutls
        outputs = self._bing_parse(outputs)

        return outputs
