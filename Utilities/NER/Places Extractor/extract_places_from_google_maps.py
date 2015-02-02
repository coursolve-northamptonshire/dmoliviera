#!/usr/bin/env python
# coding=utf8
import re

INPUT_FILE = './Data/Input/list_of_places_in_northamptonshire_Google Maps.html'
OUTPUT_FILE = './Data/Output/list_of_places_in_northamptonshire_google_maps.txt'
REGEX = r'infoWindow:{title:\'(.+?)(?:,\sNorthamptonshire)?\s←\','

if __name__ == '__main__':
    print('Initiated NE Extraction...')

    places = [place for place in re.findall(REGEX, open(INPUT_FILE, 'r').read(), re.IGNORECASE)]
    places = list(set(places))
    
    output = open(OUTPUT_FILE, 'w')
    [output.write(place+'\n') for place in places]
    output.flush()
    output.close()

print(places)
print('Found {0} places.'.format(len(places)))
print('Finished Process.')
