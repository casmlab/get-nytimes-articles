get-nytimes-articles
====================

Python tools for getting data from the New York Times Article API. Retrieves JSON from the API, stores it, parses it into a CSV file.

New York Times Article API Docs: http://developer.nytimes.com/docs/read/article_search_api_v2

Requesting an API Key for the Times API: http://developer.nytimes.com/docs/reference/keys

## Usage
Within the script, set your query parameters on line 54. See the Times API docs for available filters.

```python getTimesArticles.py -j JSON_FOLDER_PATH -c OUTPUT_FILE -k API_KEY```

## Planned improvements
- accept query parameters from command line
- solve KeyError issues in parse module
- make script smart about whether or not to keep fetching for that day (i.e., stop when no more articles)
- make script smart about running multi-day processes (i.e., respect the API limit and wait when more than 10K calls needed)
