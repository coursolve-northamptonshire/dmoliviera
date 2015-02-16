# -- Dependencies
# Note: Install by pip install <package_name>
# requests -- For http request

from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join

import requests
import re

BASE_URL_LIBRARY = 'http://www.northamptonshire.gov.uk/en/councilservices/Leisure/libraries/visit-your-library/ListLibraries/Pages/'
INDEX_NAME = 0
INDEX_ADDRESS = 1
INDEX_CITY = 2
INDEX_GEO_LOCATION = 3
INDEX_TELEPHONE = 4
INDEX_FAX = 5
INDEX_EMAIL = 6 

HEADER = ['name', 'address', 'city', 'geo_location', 'telephone', 'fax', 'email']
PATTERN_EXTRACT_ATTRIBUTES_FROM_HTML = r'<h2>Contact details</h2><p>(.*?)Library Manager: '
PATTERN_EXTRACT_VALUE_FROM_A_TAG = r'">(.*?)</a>'
FILE_LIBRARY_LIST = './Data/raw_labraries_data.html'
FILE_URL_LIBRARIES = './Data/url_libraries.txt'
FILE_LIBRARIES_DATA = './Data/labraries_data.tsv'
FOLDER_LIBRARIES = './Data/libraries/'

IS_TO_GET_URL_LIBRARY = False # Set True with you want to refresh libraries url
IS_TO_GET_LIBRARIES_PAGE = False # Set True with you want to refresh libraries page

if __name__ == "__main__":

    print '\t1. Getting libraries URL.'
    if IS_TO_GET_URL_LIBRARY:
        input_file = open(FILE_LIBRARY_LIST, 'r')
        libraries_url = re.findall(r'(' + BASE_URL_LIBRARY + '.*?)\'>', input_file.read(), re.I)
        input_file.close()

        url_output_file = open(FILE_URL_LIBRARIES, 'w')
        url_output_file.write('\n'.join(libraries_url))
        url_output_file.flush()
        url_output_file.close()

    print '\t2. Getting libraries pages.'
    if IS_TO_GET_LIBRARIES_PAGE:
        for url in libraries_url:
            print '\t\tGetting page "{0}"'.format(url[len(BASE_URL_LIBRARY):])
            html = requests.get(url)
            output = open('./Data/libraries/' + url[len(BASE_URL_LIBRARY):], 'w')
            output.write(html.text.encode('utf8'))
            output.flush()
            output.close()

    print '\t3. Getting libraries addresses.'
    output = open(FILE_LIBRARIES_DATA, 'w')
    output.write('\t'.join(HEADER) + '\n')
    count = 1
    filename_list = [filename for filename in listdir(FOLDER_LIBRARIES) if isfile(join(FOLDER_LIBRARIES, filename)) and not filename.endswith('.swp')]
    for filename in filename_list: 
        
        print '\t\t'+str(count)+'.','Analyzing html from ' + filename[:-5]
        count += 1

        raw_patterns = re.findall(PATTERN_EXTRACT_ATTRIBUTES_FROM_HTML, open(FOLDER_LIBRARIES + filename,'r').read(), re.I)[0]
        raw_patterns = raw_patterns.replace('<br /><br />', '<br />')
        raw_patterns = raw_patterns.split('<br />')

        # Cleaning variables
        raw_patterns[INDEX_GEO_LOCATION] = re.findall(PATTERN_EXTRACT_VALUE_FROM_A_TAG, raw_patterns[INDEX_GEO_LOCATION], re.IGNORECASE)
        raw_patterns[INDEX_GEO_LOCATION] = raw_patterns[INDEX_GEO_LOCATION][0] if raw_patterns[INDEX_GEO_LOCATION] else 'NA'

        raw_patterns[INDEX_TELEPHONE] = raw_patterns[INDEX_TELEPHONE][len('Tel: '):] if raw_patterns[INDEX_TELEPHONE] else 'NA'
        raw_patterns[INDEX_TELEPHONE] = raw_patterns[INDEX_TELEPHONE].replace(' ', '-')
        
        if raw_patterns[INDEX_FAX].startswith('Fax: '):
            raw_patterns[INDEX_FAX] = raw_patterns[INDEX_FAX][len('Fax: '):]
            raw_patterns[INDEX_FAX] = raw_patterns[INDEX_FAX].replace(' ', '-')
            raw_patterns[INDEX_EMAIL] = re.findall(PATTERN_EXTRACT_VALUE_FROM_A_TAG, raw_patterns[INDEX_EMAIL],re.IGNORECASE)
            raw_patterns[INDEX_EMAIL] = raw_patterns[INDEX_EMAIL][0] if raw_patterns[INDEX_EMAIL] else 'NA'
        else:
            raw_patterns[INDEX_EMAIL] = re.findall(PATTERN_EXTRACT_VALUE_FROM_A_TAG, raw_patterns[INDEX_EMAIL-1],re.IGNORECASE)
            raw_patterns[INDEX_EMAIL] = raw_patterns[INDEX_EMAIL][0] if raw_patterns[INDEX_EMAIL] else 'NA'
            raw_patterns[INDEX_FAX] = 'NA'


        raw_patterns = filter(str, raw_patterns)
        if raw_patterns:
            output.write('\t'.join(raw_patterns) + '\n')
        else:
            print '\t\t Not found data.'

    output.flush()
    output.close()
