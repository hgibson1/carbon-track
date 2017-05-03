from wtforms import Form, SelectField, SubmitField 


class RegisterTripForm(Form):
	zipcode = SelectField("Zipcode")
	year = SelectField("Year")
	make = SelectField("Make", choices=[])
	model = SelectField("Model", choices=[])
	submit = SubmitField("Submit")

	def set_make_choices(self, Model):
		choices = [(result.make, result.make) for result in Model.select(Model.make).distinct().where(Model.year == self.year.data)]
		self.make.choices = choices

	def set_model_choices(self, Model):
		choices = [(result.model, result.model) for result in Model.select(Model.model).distinct().where(Model.year == self.year.data and Model.make == self.make.data)]
		self.model.choices = choices

