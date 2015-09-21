#!/usr/bin/env python3
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
# -*- coding: utf-8 -*-

import json
import requests
import urllib2
from bs4 import BeautifulSoup


soup = BeautifulSoup(open('index.html'), "xml")
soup = soup.find_all('table')[1]
soup = soup.find_all('tr')[1::]

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
    return {'city': city.strip(), 'province':province.strip(), 'country':code_country(country.strip())}
  elif size > 3:
  	location = location.split(',')
  	return {'city': location[0].strip(), 'province': '', 'country': code_country(location[3].strip())}
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


job_posts = []
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