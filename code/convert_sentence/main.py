from nltk import tokenize
import requests
import nltk
import json
import logging
cache = {}
def sent_word(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    logging.basicConfig(level=logging.INFO,format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',datefmt='%m-%d %H:%M:%S')
    logging.info('inside sent word function')
    url = request.form['url']
    #print(request_json)
    #url = 'http://www.gutenberg.org/files/1342/1342-0.txt'
    if url in cache:
        logging.info('using cache')
        return """<img src="%s" border="1"></img>"""% cache[url]
    r = requests.get(url)
    input_data = r.content.decode(encoding='UTF-8')
    input_data = input_data.replace('\r\n', '')
    logging.info("text preporcessed")
    nltk.download('punkt')
    logging.info('after dwnloading punkt')
    data = tokenize.sent_tokenize(input_data)
    logging.info("sentences tokenized")
    histogram = {}
    for line in data:
        word_count = len(line.split())
        if word_count in histogram:
            histogram[word_count] += 1
        else:
            histogram[word_count] = 1
    data = json.dumps({'url': histogram})
    r = requests.post('https://us-central1-cc-mapreduce.cloudfunctions.net/histogram', json=data)
    print("response from histogram", r.text)
    img = "data:image/png;base64," + r.text
    cache[url] = img
    return """<img src="%s" border="1"></img>"""% img
   