Using in your browser
====================================

Here's sample walktrough how to create templates of reports and use them.

#. Go to url with *Templado* app, there is almost no content, because you haven't created your templates yet. Let's do this! Click on ``Create Template`` on the sidebar.

#. Now I will explain you the meaning of fields of form:
	* ``Title of template`` - you can name it how you want, e.g. "Pro forma invoice"
	* ``JSON template file`` - here you upload json pattern of form for creating new report. I will show you sample file::

		{
		    "id": {
	        	"caption": "Report ID",
		        "hint": "some number e.g. 21",
		        "type": "text",
		        "order": 1,
		        "check": "^[0-9]+$"
		    },
		    "year": {
		        "caption": "Year",
		        "hint": "YYYY",
		        "type": "text",
		        "order": 2,
		        "check": "^[0-9][0-9][0-9][0-9]$"
			},   
		    "items": {
		        "caption": "Bought products",
		        "order": 3,
		        "type": [
		            {
		                "price": {
		                    "caption": "Price",
		                    "hint": "e.g. 21.00",
		                    "type": "text",
		                    "order": 2,
		                    "check": "^[0-9]+\\.[0-9][0-9]$"
		                },
		                "name": {
		                    "caption": "Name of product",
		                    "hint": "e.g. printer ink",
		                    "type": "text",
		                    "order": 1,
		                    "check": ".+"
		                }
		            }
		        ]
		    }
		}


	As you can see, we declare what fields we want to show: **"id"**, **"year"** and **"items"**. Let's look on it! 
	It has:

		**"caption"**
			represents what will show as label
		**"hint"**
			placeholder for input
		**"type"**
			based on the type of value we declare type of input, for string - text input, for list with dict - nested formset which can have several text inputs, only root form can have those
		**"order"**
			number for ordering fields, because form pattern is represented as dict
		**"check"**
			regular expression for validating input from user

	* ``HTML template file`` - the file can be like this::

		<html>
		<head>
			<title></title>
		</head>
		<body>
			<h1>Invoice no. {{ id }}</h1>
			<table>
				{% for element in items %}
					<tr>
						<td>{{ element.name }}</td>
						<td>{{ element.price }}</td>
					</tr>
				{% endfor %}
			</table>
		</body>
		</html>


	Here we specify how our pdf with report should look like. It will be filled with data user gives to the input in form. We're using names from json file: ``id`` and ``items``, and because ``items`` is formset it can have several entries. Each of them has ``name`` and ``price``, so we can iterate over it.

	* ``Tags`` - some keywords separated with comma
	* ``Pattern for title`` - it will show as title of report based on data from form, also uses Django template language e.g.::

		PFI/{{ id }}/{{ year }}


	* ``Pattern for tags`` - your keywords, so it will be easier to find some specific report, e.g.::

		year: {{ year }}


#. Make sure you filled all fields and click ``Create!`` It will redirect you to view ``Templates`` and create new report template from which you can generate new reports. 

#. Now you can create new report from template. To do this click ``Generate``. 

#. There you have form, it has labels, captions, validations as we declared earlier in json pattern. Fill it as you like (in formset you can add new elements) and click ``Generate PDF``.

#. Finish! New report is created, click ``Download`` to see PDF based on html pattern we uploaded a few steps back and data we entered into form.