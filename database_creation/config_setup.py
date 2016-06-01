import configparser
config = configparser.ConfigParser()
config['DEFAULT'] = {}
config['DEFAULT']['api_key'] = 'apikey'
config['DEFAULT']['sql_password'] = 'password'
with open('config.ini', 'w') as configfile: 
	config.write(configfile)