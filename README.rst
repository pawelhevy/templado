=====
Templado
=====

Templado is a simple Django app to upload your HTML report templates and generate those reports by filling the fields of form based on JSON template.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "templado" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'bootstrap3',
        'templado',
    )

2. Modify also settings with::
    
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

    from django.conf import settings
    REPORT_STATIC_DIR = os.path.join(os.path.join(settings.MEDIA_ROOT, 'media'), 'report-static')

3. Include the templado URLconf in your project urls.py like this::

    url(r'^templado/', include('templado.urls', namespace='templado')),

4. Run `python manage.py migrate` to create the templado models.

5. Start the development server.

6. Visit http://127.0.0.1:8000/templado/ to start using Templado app.
