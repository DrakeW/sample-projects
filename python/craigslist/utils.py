import urllib2
import urllib
import json
import time
import operator


def get_neighborhoods(url):
    html = urllib2.urlopen(url).read()
    neighborhood_string = html.partition('<option value="">all neighborhoods</option>')[2].partition('</select>')[0].strip()
    nh = {}
    for x in neighborhood_string.split('/option>'):
        neighborhood = x.partition('>')[2].partition('<')[0]
        if neighborhood is '':
            continue
        value = int(x.partition('value="')[2].partition('"')[0])
        nh[neighborhood] = value
    return nh



def get_for_sale_abbrevs(url):
    html = urllib2.urlopen(url).read()
    for_sale_string = html.partition('<legend id="searchlegend">')[2].partition('<option value="')[2].partition('</select>')[0].strip()
    abbreviations = {}
    for x in for_sale_string.split('option value="'):
        abbrev = x.partition('"')[0]
        full_name = x.partition('>')[2].partition('<')[0].strip()
        abbreviations[full_name] = abbrev
    return abbreviations


GOOGLE_DISTANCE_API_URL = 'http://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&mode=driving&sensor=false'
def format_google_distance_url(origin, destinations):
    destination_string = ""
    for destination in destinations:
        destination_string += destination + '|'
    destination_string = destination_string[:-1]
    return GOOGLE_DISTANCE_API_URL % (urllib.quote(origin), urllib.quote(destination_string))

city_distances = json.load(open('city_distance_matrix.json', 'r'))
def get_city_distances(city):
    return city_distances[city]

    origin = city + ' CA'
    destinations = []
    for dest_city in all_cities:
        destinations.append(dest_city + ' CA')

    city_distance_info = json.loads(urllib2.urlopen(format_google_distance_url(origin, destinations)).read())
    distances = {}
    for i, city in enumerate(all_cities):
        km_distance = float(city_distance_info['rows'][0]['elements'][i]['distance']['text'].partition(' ')[0])
        distances[city] = km_distance

    return distances

def get_closest_cities(city):
    distances = get_city_distances(city)
    sorted_distances = sorted(distances.iteritems(), key=operator.itemgetter(1))
    close_cities = []
    # get 5 closest cities
    for i in range(1, 6):
        city, distance = sorted_distances[i]
        close_cities.append(city)
    return close_cities



def build_city_distance_matrix():
    cities_misread = []
    city_matrix_data = {}
    for city in all_cities:
        try:
            city_matrix_data[city] = get_city_distances(city)
            print city_matrix_data[city]
        except:
            cities_misread.append(city)
            print 'misread', city
        time.sleep(20)
    print 'cities misread', cities_misread
    f = open('city_distance_matrix.json', 'w')
    f.write(json.dumps(city_matrix_data))
    f.close()



neighborhoods_to_abbrev_eby = get_neighborhoods('http://sfbay.craigslist.org/search/baa/sby?query=&zoomToPosting=&minAsk=&maxAsk=&nh=31')
#http://sfbay.craigslist.org/search/baa/eby?query=&zoomToPosting=&minAsk=&maxAsk=&nh=47
#sby
neighborhoods_to_abbrev_sby = {'campbell': 31, 'cupertino': 32, 'gilroy': 33, 'hollister': 158, 'los gatos': 34, 'milpitas': 109, 'morgan hill': 119, 'mountain view': 35, 'san jose downtown': 36, 'san jose east': 37, 'san jose north': 38, 'san jose south': 39, 'san jose west': 40, 'santa clara': 41, 'saratoga': 43, 'sunnyvale': 44, 'willow glen': 45}

#http://sfbay.craigslist.org/search/baa/sby?query=&zoomToPosting=&minAsk=&maxAsk=&nh=31
#eby
neighborhoods_to_abbrev_eby = {'hercules, pinole, san pablo, el sob': 56, 'richmond / point / annex': 65, 'berkeley': 48, 'san leandro': 67, 'dublin / pleasanton / livermore': 53, 'oakland rockridge / claremont': 66, 'oakland downtown': 58, 'oakland north / temescal': 62, 'concord / pleasant hill / martinez': 51, 'oakland hills / mills': 60, 'hayward / castro valley': 55, 'pittsburg / antioch': 113, 'vallejo / benicia': 68, 'alameda': 46, 'danville / san ramon': 52, 'lafayette / orinda / moraga': 57, 'brentwood / oakley': 142, 'albany / el cerrito': 47, 'oakland lake merritt / grand': 61, 'walnut creek': 69, 'fremont / union city / newark': 54, 'oakland west': 64, 'emeryville': 112, 'fairfield / vacaville': 154, 'oakland piedmont / montclair': 63, 'berkeley north / hills': 49, 'oakland east': 59}

#http://sfbay.craigslist.org/search/baa/pen?query=&zoomToPosting=&minAsk=&maxAsk=&nh=70
#pen
neighborhoods_to_abbrev_pen = {"los altos": 78, "menlo park": 79, "brisbane": 73, "belmont": 71, "half moon bay": 161, "redwood city": 84, "san mateo": 88, "san carlos": 87, "daly city": 75, "mountain view": 81, "pacifica": 82, "woodside": 162, "atherton": 70, "burlingame": 74, "portola valley": 163, "palo alto": 83, "south san francisco": 89, "redwood shores": 85, "east palo alto": 76, "san bruno": 86, "millbrae": 80, "foster city": 77, "coastside/pescadero": 115}



categories_to_abbrev = get_for_sale_abbrevs('http://sfbay.craigslist.org/sss/')
categories_to_abbrev = {'garage sales': 'gms', 'barter': 'bar', 'cell phones': 'moa', 'free stuff': 'zip', 'household': 'hsa', 'general': 'foa', 'jewelry': 'jwa', 'bikes': 'bia', 'all services offered': 'bbb', 'appliances': 'ppa', 'motorcycle parts &amp; acc': 'mpa', 'cds/dvd/vhs': 'ema', 'toys+games': 'taa', 'tools': 'tla', 'video gaming': 'vga', 'collectibles': 'cba', 'business': 'bfa', 'antiques': 'ata', 'all gigs': 'ggg', 'materials': 'maa', 'cars+trucks': 'cta', 'boats': 'boo', 'clothes+acc': 'cla', 'electronics': 'ela', 'furniture': 'fua', 'sporting': 'sga', 'all resume': 'res', 'all jobs': 'jjj', 'all for sale / wanted': 'sss', 'all housing': 'hhh', 'auto parts': 'pta', 'all personals': 'ppp', 'all community': 'ccc', 'baby+kids': 'baa', 'arts+crafts': 'ara', 'recreational vehicles': 'rva', 'wanted': 'waa', 'atvs/utvs/snowmobiles': 'sna', 'farm+garden': 'gra', 'tickets': 'tia', 'motorcycles': 'mca', 'photo+video': 'pha', 'computers': 'sya', 'beauty+hlth': 'haa', 'books': 'bka', 'music instr': 'msa', 'all event': 'eee', 'heavy equipment': 'hva'}




all_cities = set()
all_neighborhoods = {'sby': neighborhoods_to_abbrev_sby, 'eby': neighborhoods_to_abbrev_eby, 'pen': neighborhoods_to_abbrev_pen}
for neighborhoods in all_neighborhoods.values():
    for neighborhood in neighborhoods:
        all_cities.add(neighborhood)
all_cities = list(all_cities)
if __name__ == '__main__':
    print get_closest_cities('palo alto')
    #build_city_distance_matrix()
