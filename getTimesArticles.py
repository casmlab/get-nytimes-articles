import urllib2
import json
import datetime
import time
import sys
import argparse
import logging
from urllib2 import HTTPError

# helper function to iterate through dates
def daterange( start_date, end_date ):
    if start_date <= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            yield start_date + datetime.timedelta( n )
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            yield start_date - datetime.timedelta( n )

# helper function to get json into a form I can work with       
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

# helpful function to figure out what to name individual JSON files        
def getJsonFileName(date, page, json_file_path):
    json_file_name = ".".join([date,str(page),'json'])
    json_file_name = "".join([json_file_path,json_file_name])
    return json_file_name

# helpful function for processing keywords, mostly    
def getMultiples(items, key):
    values_list = ""
    if len(items) > 0:
        num_keys = 0
        for item in items:
            if num_keys == 0:
                values_list = item[key]                
            else:
                values_list =  "; ".join([values_list,item[key]])
            num_keys += 1
    return values_list
    
# get the articles from the NYTimes Article API    
def getArticles(date, api_key, json_file_path):
    # LOOP THROUGH THE 101 PAGES NYTIMES ALLOWS FOR THAT DATE
    for page in range(101):
        try:
            request_string = "http://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date=" + date + "&end_date=" + date + "&page=" + str(page) + "&api-key=" + api_key
            response = urllib2.urlopen(request_string)
            content = response.read()
            if content:
                json_file_name = getJsonFileName(date, page, json_file_path)
                json_file = open(json_file_name, 'w')
                json_file.write(content)
                json_file.close()
            else:
                break
            time.sleep(3)
        except HTTPError:
            logging.error("something went wrong with page %s on %s . Here's the URL of the call: %s", page, date, request_string)

# parse the JSON files you stored into a tab-delimited file
def parseArticles(date, csv_file_name, json_file_path):
    for file_number in range(101):
        # get the articles and put them into a dictionary
        try:
            file_name = getJsonFileName(date,file_number, json_file_path)
            in_file = open(file_name, 'r')
            articles = convert(json.loads(in_file.read()))
            in_file.close()
        except IOError as e:
			logging.error("IOError in %s page %s: %s %s", date, file_number, e.errno, e.strerror)
			continue
            
        # open the CSV for appending
        try:
            out_file = open(csv_file_name, 'ab')
        except IOError as e:
			logging.error("IOError: %s %s", date, file_number, e.errno, e.strerror)
			continue
        
        # loop through the articles putting what we need in a CSV   
        try:
            for article in articles["response"]["docs"]:
                # if (article["source"] == "The New York Times" and article["document_type"] == "article"):
                keywords = ""
                keywords = getMultiples(article["keywords"],"value")
    
                # should probably pull these if/else checks into a module
                variables = [
                    article["pub_date"], 
                    keywords, 
                    str(article["headline"]["main"]).decode("utf8").replace("\n","") if "main" in article["headline"].keys() else "", 
                    str(article["source"]).decode("utf8") if "source" in article.keys() else "", 
                    str(article["document_type"]).decode("utf8") if "document_type" in article.keys() else "", 
                    article["web_url"] if "web_url" in article.keys() else "",
                    str(article["news_desk"]).decode("utf8") if "news_desk" in article.keys() else "",
                    str(article["section_name"]).decode("utf8") if "section_name" in article.keys() else "",
                    str(article["snippet"]).decode("utf8").replace("\n","") if "snippet" in article.keys() else "",
                    str(article["lead_paragraph"]).decode("utf8").replace("\n","") if "lead_paragraph" in article.keys() else "",
                    ]
                line = "\t".join(variables)
                out_file.write(line.encode("utf8")+"\n")
        except KeyError as e:
            logging.error("KeyError in %s page %s: %s %s", date, file_number, e.errno, e.strerror)
            continue
        except (KeyboardInterrupt, SystemExit):
            raise
        except: 
            logging.error("Error on %s page %s: %s", date, file_number, sys.exc_info()[0])
            continue
        
        out_file.close()
        
# Main function where stuff gets done

def main():
    parser = argparse.ArgumentParser(description="A Python tool for grabbing data from the New York Times Article API.")
    parser.add_argument('-j','--json', required=True, help="path to the folder where you want the JSON files stored")
    parser.add_argument('-c','--csv', required=True, help="path to the file where you want the CSV file stored")
    parser.add_argument('-k','--key', required=True, help="your NY Times Article API key")
    # parser.add_argument('-s','--start-date', required=True, help="start date for collecting articles")
    # parser.add_argument('-e','--end-date', required=True, help="end date for collecting articles")
    args = parser.parse_args()
    
    json_file_path = args.json
    csv_file_name = args.csv
    api_key = args.key    
    start = datetime.date( year = 2013, month = 2, day = 6 )
    end = datetime.date( year = 2013, month = 2, day = 7 )
    log_file = "".join([json_file_path,"getTimesArticles.log"])
    logging.basicConfig(filename=log_file, level=logging.INFO)
    
    logging.info("Getting started.") 
    try:
        # LOOP THROUGH THE SPECIFIED DATES
        for date in daterange( start, end ):
            date = date.strftime("%Y%m%d")
            logging.info("Working on %s." % date)
            getArticles(date, api_key, json_file_path)
            parseArticles(date, csv_file_name, json_file_path)
    except:
        logging.error("Unexpected error: %s", str(sys.exc_info()[0]))
    finally:
        logging.info("Finished.")

if __name__ == '__main__' :
    main()
    
