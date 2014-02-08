#!/usr/bin/env python

from __future__ import print_function
import os, sys



def findPackages(root):
	packages = []
	for (dir, dirs, filenames) in os.walk(root):
		for filename in filenames:
			if filename == 'top_level.txt':
				path = os.path.join(dir, filename)
				with open(path) as f:
					new = map(lambda L: L.strip(), f.readlines())
					print('Found {} in {}.'.format(', '.join(new), path))
					packages += new

	return packages


def link(sourceDir, targetDir, name):
	source = os.path.join(sourceDir, name)
	target = os.path.join(targetDir, name)
	if not os.path.exists(source):
		print('[!] Skipping {} (source does not exist).'.format(target))
	elif os.path.exists(target):
		print('[!] Skipping {} (link already exists).'.format(target))
	else:
		relSource = os.path.relpath(source, targetDir)
		print('{} -> {}'.format(target, relSource))
		os.symlink(relSource, target)



if __name__ == '__main__':
	sitePackages = sys.argv[1]
	target = sys.argv[2]

	packages = findPackages(sitePackages)
	print('Linking packages:', ', '.join(packages))

	for package in packages:
		link(sitePackages, target, package)

	statement = \
		'import os, sys\n' + \
		'sys.path.insert(0, os.path.join(os.path.dirname(__file__), \'{}\'))'.format(target)

	print('Add the following to your appengine_config.py:\n')
	print(statement, '\n\n')
