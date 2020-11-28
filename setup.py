from setuptools import find_packages, setup 


setup(
	name='keywords_service',
	version='1.0.0',
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		"Werkzeug==1.0.1",
		"Flask_HTTPAuth==4.2.0",
		"Flask==1.1.2",
		"nltk==3.5",
		"itsdangerous==1.1.0",
		"psycopg2==2.8.6"
	],
)
