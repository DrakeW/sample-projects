import urllib2
import urllib
from flask import Flask, render_template, request
from utils import all_neighborhoods, categories_to_abbrev, get_closest_cities, all_cities
import chardet
app = Flask(__name__)


app.config['DEBUG'] = True

@app.route('/')
def index():
    return render_template('index.html')



def get_price_range(query):
    lower_price = int(query.partition('$')[2].partition(' ')[0].strip())
    higher_price = int(query.partition('$')[2].partition('$')[2].partition(' ')[0].strip())
    return lower_price, higher_price


def get_category(query):
    return query.split('between')[0].split('near')[0].strip()

def get_city(query):
    return query.partition('near')[2].partition('between')[0].strip()



#also consider result.location
def get_results(url):
    html = urllib2.urlopen(url).read()
    results = []
    while True:
        result = {}
        before, matched, after = html.partition('<p class="row"')
        if matched == '':
            break
        url, matched, after = after.partition('<a href="')[2].partition('<a href="')[2].partition('">')
        result['url'] = 'http://sfbay.craigslist.org/' + url.strip()
        title, matched, after = after.partition('<')
        encoding = chardet.detect(title)['encoding']
        result['title'] = title.strip().decode(encoding)


        """
        posting_html = urllib2.urlopen(result['url']).read()
        encoding = chardet.detect(posting_html)['encoding']
        posting_html = posting_html.decode(encoding)

        description = posting_html.partition('<section id="postingbody">')[2].partition('</section>')[0].replace('<br>', ' ')
        description = ' '.join(description.split()) # clean up extra white space in between words
        result['description'] = description
        """
        result['description'] = ''
        results.append(result)
        html = after
    return results

def get_region(city):
    if city in all_neighborhoods['sby']:
        return 'sby'
    if city in all_neighborhoods['eby']:
        return 'eby'
    if city in all_neighborhoods['pen']:
        return 'pen'



CATEGORY_ONLY_QUERY = "http://sfbay.craigslist.org/%s/"
CATEGORY_AND_PRICE_ONLY_QUERY = "http://sfbay.craigslist.org/search/%s?query=&zoomToPosting=&minAsk=%d&maxAsk=%d"
CATEGORY_AND_LOCATION_ONLY_QUERY = "http://sfbay.craigslist.org/search/%s/%s?query=&zoomToPosting=&minAsk=&maxAsk="
FULL_QUERY = "http://sfbay.craigslist.org/search/%s/%s?query=&zoomToPosting=&minAsk=%d&maxAsk=%d"
@app.route('/search')
def search():
    context = {}
    query = request.args.get('query').strip().lower()
    context['query'] = query

    if 'between' not in query and 'near' not in query:
        url_to_request = CATEGORY_ONLY_QUERY % categories_to_abbrev[query]
    elif 'between' in query and 'near' not in query:
        category = get_category(query)
        url_to_request = CATEGORY_AND_PRICE_ONLY_QUERY % (categories_to_abbrev[category], lower_price, higher_price)
    elif 'near' in query and 'between' not in query:

        category = get_category(query)
        city = get_city(query)

        closest_cities = get_closest_cities(city)

        region = get_region(city)
        url_to_request = CATEGORY_AND_LOCATION_ONLY_QUERY % (categories_to_abbrev[category], region)
        for close_city in closest_cities:
            if close_city in all_neighborhoods[region]:
                url_to_request += '&nh=' + str(all_neighborhoods[region][close_city])
    elif 'between' in query and 'near' in query:

        urls_to_request = []
        category = get_category(query)
        city = get_city(query)
        lower_price, higher_price = get_price_range(query)
        region = get_region(city)
        url_to_request = FULL_QUERY % (categories_to_abbrev[category], region, lower_price, higher_price)
        closest_cities = get_closest_cities(city)
        for close_city in closest_cities:
            if close_city in all_neighborhoods[region]:
                url_to_request = url_to_request + "&nh=" + str(all_neighborhoods[region][close_city])
    else:
        return render_template('message.html', context = {'message': 'This was a bad query'})

    results = get_results(url_to_request)

    for i, result in enumerate(results):
        result['index'] = i + 1

    context['results'] = results
    return render_template('results.html', context=context)

@app.route('/about')
def about():
    return render_template('message.html', context={'message': 'A better craigslist'})



"""
Some things people can do are to store in memory a list of correct words. If people misspell too many things in their ad, then don't display it... make it less sketchy

Other things people can do are custom search. Let people make a query that's like Find an apartment close to Berkeley between $500 to $1000 dollars

distance api:
http://zipcodedistanceapi.redline13.com/rest/DnjlpMRFn3MwDY4WdHn8xdsOsoMMjG4W4nhu999xcW3PU7M8O9gmnJbQ8XCrEHnI/distance.json/94306/94704/mile
"""






#http://maps.googleapis.com/maps/api/distancematrix/json?origins=campbell+CA&destinations=milpitas+CA|los+gatos+CA&mode=driving&sensor=false
