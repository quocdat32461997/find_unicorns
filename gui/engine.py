# engine.py

# import dependencies
import json
import requests
import pickle

from read import *
from pagerank import *

class Engine(object):
    def __init__(self):
        with open('api_keys.json') as file:
            keys = json.load(file)
            self.google_api = keys['google']['api']
            self.google_engine_id = keys['google']['engine_id'] 
            self.bing_api = keys['bing']['api']
            self.bing_sub_key = keys['bing']['subscription_key']

        self.data, self.rows, self.columns = readData('finaldata.xlsx')
        with open('tokDict_10k.pkl', 'rb') as file:
            self.tokenDict = pickle.load(file)
        with open('tokPostings_10k.pkl', 'rb') as file:
            self.tokPostings = pickle.load(file)

        self.hubs, self.authority = HITS(self.data, self.rows)
        self.pr = pageRank(self.data, self.rows)

        self.search_page = 1
        self.query = None
        self.vs_matrix = None

    def get_text(self, link):
        # get first 100 characters
        return self.data[self.data['Link'] == link]['Text'].values[0][:200] + '...'

    def search(self, query):
        """
        Args:
            query : str
            page : int
                By default, get every 10 pages
        Returns;
            vs_outputs : list of dict
                List of dict: Title, Description, Link
        """
        # refresh search
        if not self.query or query != self.query:
            self.query = query
            self._search(query)
            self.search_page = 1

        # perform retreival here
        self.vs_outputs = np.array(self.vs_matrix[(self.search_page -1) * 10: self.search_page + 10])
        if self.vs_outputs.shape == (1,0):
            return None
        else:
            outputs = [{'title' : out[2], 'description' : self.get_text(out[3]), 'link' : out[3]} for out in self.vs_outputs]
            return outputs

    def _search(self, query):
        """
        Retrieve documents given query 
        Args:
            query : str
                Query input
        Returns:
            outputs : list of str
                List of docs
        """
        self.vs_matrix = vector_space_model(query, self.tokenDict, self.tokPostings, self.rows, self.data)

    def hits(self):
        if self.vs_outputs.shape == (1,0):
            return None
        else:
            # copy vs_outputs
            vs_outputs = {x[3]: (self.get_text(x[3]), x[2]) for x in self.vs_outputs}
            # retrieve hub scores by links
            scores = {x:self.hubs[x] for x in vs_outputs.keys()}
            # sort by hub score
            scores = sorted(scores.items(), key = lambda x: x[-1], reverse = True)

            # get outputs
            outputs = [{'title' : vs_outputs[x[0]][-1], 'description' : vs_outputs[x[0]][0], 'link' : x[0]} for x in scores]
            return outputs

    def pagerank(self):

        if self.vs_outputs.shape == (1,0):
            return None
        else:
            # copy vs _outputs
            vs_outputs = {x[3]: (self.get_text(x[3]), x[2]) for x in self.vs_outputs}
            # retrieve hub scores by links
            scores = {x:self.pr[x] for x in vs_outputs.keys()}
            # sort by hub score
            scores = sorted(scores.items(), key = lambda x: x[-1], reverse = True)

            # get outputs
            outputs = [{'title' : vs_outputs[x[0]][-1], 'description' : vs_outputs[x[0]][0], 'link' : x[0]} for x in scores]
            return outputs

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

    def google(self):
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
        start = (self.search_page - 1) * 10 + 1 # get 10 at a time
        url = "https://www.googleapis.com/customsearch/v1?key={}&cx={}&q={}&start={}".format(self.google_api, self.google_engine_id, self.query, start)

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

    def bing(self):
        """
        Retrieve websites given query by Bing API
        Args:
        Returns:
            outputs : list of str
                List of docs
        """
        # configure url
        start = (self.search_page - 1) * 10 + 1
        url = "https://api.bing.microsoft.com/v7.0/custom/search?q={}&customconfig={}&count=10&offset={}".format(self.query, self.bing_api, start)

        # make search requests
        outputs = requests.get(url,
                headers={'Ocp-Apim-Subscription-Key': self.bing_sub_key}).json()

        # parse search resutls
        outputs = self._bing_parse(outputs)

        return outputs
