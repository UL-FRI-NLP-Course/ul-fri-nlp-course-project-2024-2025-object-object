import re
import requests
import time
import pandas as pd

class WikidataQuery:
	"""
	A class to execute SPARQL queries against the Wikidata Query Service.
	"""
	DEFAULT_ENDPOINT_URL = "https://query.wikidata.org/sparql"
	DEFAULT_USER_AGENT = "NLP-course/2025 (University of Ljubljana, FRI - mc3432@student.uni-lj.si) requests/{}"

	def __init__(self, endpoint_url: str = DEFAULT_ENDPOINT_URL, user_agent: str = None):
		"""
		Initializes the WikidataQuery class.

		Args:
			endpoint_url (str): The URL of the SPARQL endpoint.
			user_agent (str): A custom User-Agent string. If None, a default is used.
							   It's highly recommended to customize this with your project details
							   and contact information as per Wikidata's User-Agent policy.
		"""
		self.endpoint_url = endpoint_url
		if user_agent is None:
			# Format the default user agent with the requests library version
			self.user_agent = self.DEFAULT_USER_AGENT.format(requests.__version__)
		else:
			self.user_agent = user_agent

	def execute_query(self, query: str) -> list:
		"""
		Executes a SPARQL query and returns the results.

		Args:
			query (str): The SPARQL query string.

		Returns:
			list | None: A list of dictionaries representing the result bindings,
						 or None if the query fails after retries.
		"""
		headers = {
			'Accept': 'application/sparql-results+json',
			'User-Agent': self.user_agent
		}
		params = {
			'query': query,
			'format': 'json'
		}

		response = requests.get(self.endpoint_url, headers=headers, params=params, timeout=60)
		response.raise_for_status()

		data = response.json()
		bindings = data.get('results', {}).get('bindings', [])

		if not bindings:
			return pd.DataFrame()

		data = []
		for row in bindings:
			entry = {}
			for key, meta in row.items():
				value = meta.get('value')
				if coordinateMatch := re.match(r"Point\(([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)", value):
					x = float(coordinateMatch.group(1))
					y = float(coordinateMatch.group(2))
					entry[f"{key}_x"] = x
					entry[f"{key}_y"] = y
				else:
					entry[key] = value
			data.append(entry)

		return pd.DataFrame(data)