Changing look of application
=============================

#. Create file in your Django project::

	project/
	  ...
	  templates/
	    templado/
	    	templado_site.html

#. Sample html for *templado_site.html* can be like this::

	{% extends 'base.html' %}

	{% block title %}
	    {% block templado_title %}
	    {% endblock %}
	{% endblock %}

	{% block content %}
	    {% block templado_static %}
	    {% endblock %}

	    {% block templado_content %}
	    {% endblock %}
	{% endblock %}


Of course if you have declared blocks ``title`` and ``content`` in your *base.html*. But it's just a sample.
You can place blocks from templado wherever you want, those blocks are:

	- ``templado_title`` - contains title of application
	- ``templado_static`` - css and javascript files
	- ``templado_content`` - base skeleton of application

