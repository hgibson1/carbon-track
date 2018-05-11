$(document).ready(function() {
	var dropdown = {
		year: document.getElementByID('#select_year'),
		make: document.getElementByID('#select_make'),
		model: document.getElementByID('#select_model')
	};

	function update_make() {
		var send = {
			year = dropdown.year.val()
		};
		
		dropdown.make.attr('disabled', 'disabled');
		dropdown.make.empty();
		dropdown.model.attr('disabled', 'disabled');
		dropdown.model.empty();
		
		$.getJSON("{{ url_for('_update_make_choices') }}"), send, function(data) {
			data.forEach(function(item) {
				dropdown.make.append(
					$('<option>', {
						value: item[0],
						text: item[1]
					})
				);
			});
			dropdown.make.removeAttr('disabled');
		});
	}

	function update_model() {
		var send = {
			year = dropdown.year.val(),
			make = dropdown.make.val()
		};
		
		dropdown.model.attr('disabled', 'disabled');
		dropdown.model.empty();

		$.getJSON("{{ url_for('_update_model_choices') }}"), send, function(data) {
			data.forEach(function(item) {
				dropdown.model.append(
					$('<option>', {
						value: item[0],
						text: item[1]
					})
				);
			});
			dropdown.model.removeAttr('disabled');
		});
	}

	dropdown.year.bind('click', function() {
		update_make();
	});

	dropdown.make.bind('click', function() {
		update_model();
	});

	update_make();
	update_model();
});

