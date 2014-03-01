# Since google maps api only lets you call 2500 at a time, this merges the dictionaries returned from different servers
import json
dict1 = json.load(open('city_distance_matrix1.json', 'r'))
dict2 = json.load(open('city_distance_matrix2.json', 'r'))
dict3 = json.load(open('city_distance_matrix3.json', 'r'))
dict4 = dict(dict1.items() + dict2.items() + dict3.items())
print len(dict1) + len(dict2) + len(dict3)
print len(dict4)
f = open('merged_city_distance_matrix.json', 'w')
f.write(json.dumps(dict4))
f.close()
