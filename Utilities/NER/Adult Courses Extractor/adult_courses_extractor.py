# -- Dependencies
# Note: Install by pip install <package_name>
# requests -- For http request

import requests
import re

from bs4 import BeautifulSoup

if __name__ == "__main__":

    max_pages = 46
    url_pattern = 'https://www.northamptonshire.gov.uk/en/councilservices/EducationandLearning/adults/coursebooking/secure/Pages/searchresults.aspx?viewAll=true&page={0}'
    output_file = open('./Data/adult_course_list.txt', 'w')
    header = ['code', 'name', 'day', 'period',  'start_date', 'weeks', 'location', 'venue', 'places_available',  'full_fee', 'remitted_fee']
    output_file.write('\t'.join(header) + '\n')

    for index in range(1, max_pages+1):
        html = requests.get(url_pattern.format(index)).content
        soup = BeautifulSoup(html, from_encoding='utf8')
        table = soup.findAll('table', 'searchresultsgrid')[0]
        row_list = BeautifulSoup(str(table), from_encoding='UTF8').findAll('tr')
        for row in row_list[1:]:
            columns = BeautifulSoup(str(row), from_encoding='UTF8').findAll('td')
            columns = map(lambda column: column.get_text().strip().encode('utf8'), columns)
            output_file.write('\t'.join(columns) + '\n')
