from flask import Flask, request, render_template, jsonify, url_for

from datetime import datetime

from models import sqldb, influxdb, INFLUX_DATABASE, FuelEconomy, Zipcode
from forms import RegisterTripForm


BASE_LAT = 42.35
BASE_LONG = -71.11


app = Flask(__name__)


@app.before_first_request
def before_first_request():
	sqldb.connect()
	sqldb.create_tables([Zipcode, FuelEconomy], safe=True)


@app.before_request
def before_request():
	sqldb.connect()


@app.after_request
def after_request(response):
	sqldb.close()
	return response


@app.route("/", methods=["GET", "POST"])
def index():
	form = RegisterTripForm()
	form.zipcode.choices = [(result.zipcode, result.zipcode) for result in Zipcode.select()]
	form.year.choices = [(result.year, result.year) for result in FuelEconomy.select(FuelEconomy.year).distinct(FuelEconomy.year)]
	form.make.choices = [(result.make, result.make) for result in FuelEconomy.select(FuelEconomy.make).distinct(FuelEconomy.make)]
	form.model.choices = [(result.model, result.model) for result in FuelEconomy.select(FuelEconomy.model).distinct(FuelEconomy.model)]
	
	if request.method == "POST":	
		zipcode = request.form.zipcode.data
		lat = Zipcode.get(Zipcode.zipcode == zipcode).latitude
		lon = Zipcode.get(Zipcode.zipcode == zipcode).longitude
		distance = ((69 * abs(BASE_LAT - lat)) ** 2 + (51 * abs(BASE_LONG - lon)) ** 2) ** 0.5

		year = request.form.year.data
		make = request.form.make.data
		model = request.form.model.data

		city_fe = FuelEconomy.get(FuelEconomy.year == year and FuelEconomy.make == make and FuelEconomy.model == model).city_fe
		highway_fe = FuelEconomy.get(FuelEconomy.year == year and FuelEconomy.make == make and FuelEconomy.model == model).highway_fe
		co2_low = 20 * float(distance)/float(highway_fe)
		co2_high = 20 * float(distance)/float(city_fe)
		
		trip = {
			"measurement": "test",
			"time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
			"tags": {
				"zipcode": zipcode,
				"make": make,
				"model": model,
				"year": year
			},
			"fields": {
				"distance": distance,
				"co2_low": co2_low,
				"co2_high": co2_high
			}
		}

		influxdb.write_points([trip], database=INFLUX_DATABASE)

	return render_template("index.html", form=form, model=FuelEconomy)


@app.route("/_update_make_choices", methods=["GET", "POST"])
def update_make_choices():
	year = request.args.get('year', '01', type=int)
	make = [(result.make, result.make) for result in FuelEconomy.select(FuelEconomy.make).where(FuelEconomy.year == year).distinct(FuelEconomy.make)]
	print "redirect to update make"
	print year
	return jsonify(make)


@app.route("/_update_model_choices", methods=["GET", "POST"])
def update_model_choices():
	year = request.args.get('year', '01', type=int)
	make = request.args.get('make', '01', type=str)
	model = [(result.model, result.model) for result in FuelEconomy.select(FuelEconomy.model).where(FuelEconomy.year == year and FuelEconomy.make == make).distinct(FuelEconomy.model)]
	print "redirect to update model"
	print "{} {}".format(year, make)
	return jsonify(model)


if __name__ == "__main__":
	app.run(debug=True)

