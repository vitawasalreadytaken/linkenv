from setuptools import setup

setup(
	name = 'linkenv',
	version = '0.1.0',
	author = 'Vita Smid',
	author_email = 'me@ze.phyr.us',
	packages = ['linkenv',],
	url = 'https://github.com/ze-phyr-us/linkenv',
	license = 'LICENSE.txt',
	description = 'Symlink packages from your virtualenv so that GAE can find and deploy them.',
	entry_points = {
		'console_scripts': [
			'linkenv = linkenv.linkenv:main',
		]
	}
)
