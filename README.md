get-nytimes-articles
====================

Python tools for getting data from the New York Times Article API. Retrieves JSON from the API, stores it, parses it into a CSV file.

New York Times Article API Docs: http://developer.nytimes.com/docs/read/article_search_api_v2

Requesting an API Key for the Times API: http://developer.nytimes.com/docs/reference/keys

## Dependencies
Python v2.7 (not tested on any others)
Modules:
- urllib2 (HTTPError)
- json
- datetime
- time
- sys
- argparse
- logging

## Why store the JSON files? Why not just parse them?
The New York Times is nice enough to allow programmatic access to its articles, but that doesn't mean I should query the API every time I want data. Instead, I query it once and cache the raw data, lessening the burden on the Times API. Then, I parse that raw data into whatever format I need - in this case a tab-delimited file with only some of the fields - and leave the raw data alone. Next time I have a research question that relies on the same articles, I can just re-parse the stored JSON files into whatever format helps me answer my new question.

## Usage
Within the script, set your query parameters on line 54. See the Times API docs for available filters. The example query returns all articles for a given date range (set in lines 118 and 119).

```python getTimesArticles.py -j JSON_FOLDER_PATH -c OUTPUT_FILE -k API_KEY```

## Planned improvements
- accept query parameters from command line
- solve KeyError issues in parse module
- make script smart about whether or not to keep fetching for that day (i.e., stop when no more articles)
- get better info from API calls with errors so can re-request
- make script smart about running multi-day processes (i.e., respect the API limit and wait when more than 10K calls are needed)
