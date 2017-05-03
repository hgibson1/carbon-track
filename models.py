from peewee import *
from influxdb import InfluxDBClient


INFLUX_SERVER = "localhost"
INFLUX_DATABASE = "test"

influxdb = InfluxDBClient(INFLUX_SERVER, 8086, INFLUX_DATABASE)
sqldb = SqliteDatabase("transportation-data.db")


class FuelEconomy(Model):
	year = IntegerField()
	make = CharField()
	model = CharField()
	city_fe = FloatField()
	highway_fe = FloatField()
	combined_fe = FloatField()

	class Meta:
		database = sqldb


class Zipcode(Model):
	zipcode = CharField(unique=True)
	latitude = FloatField()
	longiture = FloatField()

	class Meta:
		database = sqldb

	

