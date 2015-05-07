import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='templado',
    version='0.2',
    packages=['templado'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Templado is a simple Django app to upload your HTML report templates and generate PDF reports by filling the fields of form based on JSON template.',
    long_description=README,
    url='https://github.com/nnkps/templado',
    author='Anna Kups',
    author_email='aniakups@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',  # dependencies are not compatible with python3 
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
	'Django',
        'CairoSVG',
        'Pyphen', 
        'WeasyPrint',
        'argparse',
        'cairocffi',
        'cffi',
        'cssselect',
        'django-bootstrap3',
        'html5lib',
        'lxml',
        'pycparser',
        'six',
        'tinycss',
        'wsgiref',
    ],
    keywords='template json html pdf report invoice',
)
