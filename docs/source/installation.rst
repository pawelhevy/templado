Installation
====================================

Templado package for Django allows you to create pdf reports based on html and json templates you upload.

Here are some steps to make templado app working.

#. After you created your Django app, you can just install Templado in your virtualenv from PyPi with command

	``pip install templado``

#. Put **bootstrap3** and **templado** in your *settings.py*::

	INSTALLED_APPS = (
	    ...
	    'bootstrap3',
	    'templado',
	)

#. Modify also *settings.py* with::

	FILE_UPLOAD_HANDLERS = (
	    ...
	    'django.core.files.uploadhandler.MemoryFileUploadHandler',
	    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
	)

	TEMPLATE_CONTEXT_PROCESSORS = (
	    ...
	    'django.contrib.auth.context_processors.auth',
	    'django.core.context_processors.request',
	)
	
	REPORT_STATIC_DIR = os.path.join(os.path.join(settings.MEDIA_ROOT, 'media'), 'report-static')

#. Include the templado URLconf in your project *urls.py* like this::

	url(r'^templado/', include('templado.urls', namespace='templado'))

#. Run ``python manage.py migrate`` to create the templado models.
#. Start development server
#. Visit http://127.0.0.1:8000/templado/ to start using Templado app.


