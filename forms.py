from wtforms import Form, SelectField, SubmitField 


class RegisterTripForm(Form):
	zipcode = SelectField(id="select_zipcode")
	year = SelectField(id="select_year")
	make = SelectField(id="selec_make", choices=[])
	model = SelectField(id="select_model", choices=[])
	submit = SubmitField(id="submit")

