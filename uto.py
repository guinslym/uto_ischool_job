#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
# -*- coding: utf-8 -*-

import json
import requests
import urllib2
from bs4 import BeautifulSoup
import time
start = time.time()

url_root = 'http://current.ischool.utoronto.ca'


def get_url_content(url):
  get_url = lambda x: requests.get(x)
  content = get_url(url)
  return BeautifulSoup(content.text, "xml")

URL = 'http://current.ischool.utoronto.ca/jobsite/archive?page='


def code_country(country):
  if(country == 'Canada'):
    return 1
  else:
    return country

def code_province(province):
  print(province)
  if(province == u'Ontario'):
    return 11
  elif(province == u'ON'):
    return 11
  else:
  	return province

def detail_location(location):
  size = len(location.split(','))
  if size == 3:
    city, province, country = location.split(',')
    return {'city': city.strip(), 'province':province.strip(), 'country':country.strip()}
  elif size > 3:
  	location = location.split(',')
  	return {'city': location[0].strip(), 'province': '', 'country': location[3].strip()}
  else:
  	return location

def detail_date(posted):
  size = len(posted.split(','))
  if size == 2:
    info = posted.split(',')
    year = info[1].strip()
    month_day = info[0].split(',')
    month, day = month_day[0].split(' ')
    return {'year': int(year), 'month':month, 'day':int(day)}
  else:
    return posted

def detail_deadline(deadline):
  size = len(deadline.split())
  if size == 3:
    month, day, year = deadline.split()
    return {'year': int(year), 'month':month, 'day':int(day)}
  else:
    return deadline


def find_job_type_and_duration(url):
  soup = get_url_content(url)
  soup = soup.find('div', {'class': 'field field-type-text field-field-job-type'})
  if soup != None:
    s = soup.find('div', {'class': 'field-item odd'})
    div = s.find('div').text
    print('time' in div)
  #print(soup)
  pass


def find_number_of_pages():
  pagination = get_url_content(URL+'0')
  uls = pagination.find('li', {'class', 'pager-last last'})
  last_page_url = uls.find('a')['href']
  last_page_url = last_page_url.split('=')[1]
  last_page_url  = last_page_url.replace('&order', '')
  last_page = int(last_page_url)
  return last_page

def find_category_and_job_type(url, html_class):
  soup = get_url_content(url)
  soup = soup.find('div', {'class': html_class })
  if soup != None:
    soup = soup.find_all('div', {'class': 'field-item odd'})
    for elem in soup:
      s = elem.find('div', {'class': 'field-label-inline-first'})
      new_element = BeautifulSoup(str(elem).replace(str(s), ''))
      return new_element.text.strip()
  else:
    return ''

total_pages = find_number_of_pages()

#for page in range(0,total_pages + 1):
job_posts = []
for page in range(0,2):
  #print(page)
  soup = get_url_content(URL+str(page))
  soup = soup.find_all('table')[1]
  soup = soup.find_all('tr')[1::]
  
  taille_soup = len(soup)
  decompte = 0
  for rows in soup:
    decompte = decompte + 1
    print "page ", page , " -- ", decompte, "/", taille_soup, ' de fait.'
    tds = rows.find_all('td')	
    job_title = (tds[0]).text
    job_title = job_title.strip()
    organization = (tds[1]).text.strip()
    location = (tds[2]).text.strip()
    location = detail_location(location)
    category = (tds[3]).text.strip()
    posted = (tds[4]).text.strip()
    posted = detail_date(posted)
    deadline = (tds[5]).text.strip()
    deadline = detail_deadline(deadline)
    link = tds[0]
    job_link = link.find('a')['href']
    #other page
    url = url_root + job_link
    job_type = find_category_and_job_type(url, 'field field-type-text field-field-job-type')
    student = find_category_and_job_type(url, 'field field-type-text field-field-job-forstudent')
    #print(job_type)
    job_duration = find_category_and_job_type(url, 'field field-type-text field-field-job-duration')
    job_posts.append({'job_title': job_title, 
  									'organization': organization,
  									'location': location,
  									'category': category,
  									'posted': posted,
  									'deadline': deadline,
  									'job_link': job_link,
  									'job_type': job_type,
  									'job_duration': job_duration,
  									'student': student,
  									'job_from': 'University of Toronto -- Ischool' })
  print 'It took', (time.time()-start)/60.0, 'minutes.'

with open('data_short.json', 'w') as outfile:
  json.dump(job_posts, outfile, sort_keys = True, indent=4)

print('--------------------------------------')
print 'Finish: It took', (time.time()-start)/60.0, 'minutes.'



#"Toronto, Chatham or Gatineau, ON or QC, Canada"