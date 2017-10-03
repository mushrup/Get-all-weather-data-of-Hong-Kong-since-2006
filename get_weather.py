import urllib2
import html2text
import re
import os
import pandas as pd
import time

def get_weather(year,month,date):
  days = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
  months = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
  url = 'http://www.hko.gov.hk/cgi-bin/hko/yes.pl?year='+str(year)+'&month='+months[month]+'&day='+days[date]+'&language=english&B1=Confirm'
  page = urllib2.urlopen(url) 
  html_content = page.read()
  rendered_content = html2text.html2text(html_content)
  file = open('weather.txt', 'w')
  file.write(rendered_content)
  file.close()
  time.sleep(0)

def get_numbers(file_name):
  with open(file_name) as input_data:
    started = False
    just_start = False
    order = 0
    numbers = []
      # Skips text before the beginning of the interesting block:
    for line in input_data:
                       #('     Maximum air temperature')
      if line.startswith('    Maximum Air Temperature') or line.startswith('    MAXIMUM AIR TEMPERATURE') or line.startswith('    Maximum air temperature') :
        words = re.split(r'\s{2,}', line)
        temp_list = re.findall(r'\b\d+\b',line)
        temp = float(temp_list[0])+0.1*float(temp_list[1])
        numbers.append(temp)
        order = order + 1
        started = True
        just_start = True

      if started is True and just_start is False:
        words = re.split(r'\s{2,}', line)
        temp_list = re.findall(r'\b\d+\b',line)
        if len(temp_list) is 2:
          temp = float(temp_list[0])+0.1*float(temp_list[1])
          numbers.append(temp)
        else:
          if len(temp_list) is 1:
            temp = float(temp_list[0])
            numbers.append(temp)
          else:
            temp = 0
            numbers.append(temp)
        order = order + 1
        if order is 7:
          started = False
          return numbers
      else:
        just_start = False

def fill_data(df,numbers):
  tags = df.columns.values
  for i in range(7):
    df.set_value(index, tags[i], numbers[i])

df = pd.DataFrame.from_csv('Plain_Template.csv')

for index, row in df.iterrows():
  year = index.year
  month = index.month
  day = index.day
  get_weather(year,month,day)
  print (year,month,day)
  numbers = get_numbers("weather.txt")
  fill_data(df,numbers)

df.to_csv('Weather_Dataset.csv', encoding='utf-8')
os.system("rm weather.txt")

