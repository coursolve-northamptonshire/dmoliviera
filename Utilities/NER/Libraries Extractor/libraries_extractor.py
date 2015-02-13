# -- Dependencies
# Note: Install by pip install <package_name>
# requests -- For http request

import requests
import re

from bs4 import BeautifulSoup

BASE_URL_LIBRARY = 'http://www.northamptonshire.gov.uk/en/councilservices/Leisure/libraries/visit-your-library/ListLibraries/Pages/'

if __name__ == "__main__":

    print '\t1. Getting libraries URL.'
    input_file = open('./Data/raw_libraries_data.html', 'r')
    libraries_url = re.findall(r'(' + BASE_URL_LIBRARY + '.*?)\'>', input_file.read(), re.I)
    input_file.close()

    url_output_file = open('./Data/url_libraries.txt', 'w')
    url_output_file.write('\n'.join(libraries_url))
    url_output_file.flush()
    url_output_file.close()

    print '\t2. Getting libraries pages.'
    for url in libraries_url:
        print '\t\tGetting page "{0}"'.format(url[len(BASE_URL_LIBRARY):])
        html = requests.get(url)
        output = open('./Data/libraries/' + url[len(BASE_URL_LIBRARY):], 'w')
        output.write(html.text.encode('utf8'))
        output.flush()
        output.close()

    print '\t3. Getting libraries addresses.'

