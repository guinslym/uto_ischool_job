#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
# -*- coding: utf-8 -*-

import json
import requests
import urllib2
from bs4 import BeautifulSoup

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
  last_page = int(last_page_url)
  return last_page

total_pages = find_number_of_pages()

#for page in range(0,total_pages + 1):
job_posts = []
for page in range(0,total_pages + 1):
  print(page)
  soup = get_url_content(URL+str(page))
  soup = soup.find_all('table')[1]
  soup = soup.find_all('tr')[1::]

  for rows in soup:
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
    #find_job_type_and_duration(url)
    #job_type
    #job_duration
    job_posts.append({'job_title': job_title, 
  									'organization': organization,
  									'location': location,
  									'category': category,
  									'posted': posted,
  									'deadline': deadline,
  									'job_link': job_link})

with open('data.json', 'w') as outfile:
  json.dump(job_posts, outfile, sort_keys = True, indent=4)





#"Toronto, Chatham or Gatineau, ON or QC, Canada"