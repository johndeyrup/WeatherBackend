import requests
import configparser
import pymysql
from datetime import datetime
#Get's API key from config.ini
def get_key(file, name):
	config = configparser.ConfigParser()
	config.read('config.ini')
	api_key = config['DEFAULT'][name]
	return api_key

#Get's 5 day forecast from weather api
def get_weather_forecast(city, api_key):
	api = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + 'us&mode=json&appid=' + api_key
	r = requests.get(api)
	request_json = r.json()
	return request_json

#Get everything from table
def get_table(cursor, table):
	cursor.execute("SELECT * FROM {}".format(table))
	for row in cursor:
		print(row)

#Insert Value into table
def insert_data(cursor, table, dic):
	cursor.execute("INSERT INTO {} (Temperature, MinTemp, MaxTemp, Pressure, Humidity, CloudCoverage, WindSpeed, WindDirection, Description, Date) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, '{}', {})".format\
		(table, dic['temp'], dic['temp_min'], dic['temp_max'], dic['pressure'], dic['humidity'], dic['cloud_coverage'], dic['wind_speed'], dic['deg'], dic['description'], dic['date']))

#Delete everything from table
def delete_data(cursor, table):
	cursor.execute("DELETE FROM {}".format(table))

def insert_json_data(json, table, cursor):
	for item in json:
		item_json = {}
		item_json['date'] = item['dt']
		main = item['main']
		item_json['temp'] = main['temp']
		item_json['temp_min'] = main['temp_min']
		item_json['temp_max'] = main['temp_max']
		item_json['pressure'] = main['pressure']
		item_json['humidity'] = main['humidity']
		item_json['cloud_coverage'] = item['clouds']['all']
		item_json['wind_speed'] = item['wind']['speed']
		item_json['deg'] = item['wind']['deg']
		item_json['description'] = item['weather'][0]['description']
		insert_data(cursor, table, item_json)

api_key = get_key('config.ini', 'api_key')
city = "Boston"
weather_json = get_weather_forecast(city, api_key)['list']
table_name = "Boston"
sql_password = get_key('config.ini', 'sql_password')
conn = pymysql.connect(host='localhost', port=3306, user='root', password=sql_password, db='weatherdb')
cur = conn.cursor()
insert_json_data(weather_json, table_name, cur)
# delete_data(cur, table_name)
get_table(cur, 'Boston')
conn.commit()
cur.close()
conn.close()
