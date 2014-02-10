#!/usr/bin/env python

from __future__ import print_function
import os, sys



def findPackages(root):
	packages = []
	for (dir, dirs, filenames) in os.walk(root):
		for filename in filter(lambda x: x == 'top_level.txt', filenames):
			path = os.path.join(dir, filename)
			with open(path) as f:
				for package in f:
					package = package.strip()
					for name in (package, package + '.py'):
						if os.path.exists(os.path.join(root, name)):
							print('Found {} in {}.'.format(name, path))
							packages.append(name)

	return packages


def link(sourceDir, targetDir, name):
	source = os.path.join(sourceDir, name)
	target = os.path.join(targetDir, name)
	# Redefine targetDir to include any subdir paths that may have been present in target.
	targetDir = os.path.dirname(target)

	if os.path.exists(target):
		print('[!] Skipping {} (link already exists).'.format(target))
	else:
		if not os.path.exists(targetDir):
			print('[!] Creating parent directory {}'.format(targetDir))
			os.makedirs(targetDir)

		relSource = os.path.relpath(source, targetDir)
		print('{} -> {}'.format(target, relSource))
		os.symlink(relSource, target)



def main():
	if len(sys.argv) != 3:
		print('Usage: {} path/to/site-packages/ path/to/target/dir/'.format(sys.argv[0]))
		print('\nWill look for packages in your `site-packages\' directory and symlink them to the target directory.')
		return

	sitePackages = sys.argv[1]
	target = sys.argv[2]

	packages = findPackages(sitePackages)
	print('Linking packages:', ', '.join(packages))

	for package in packages:
		link(sitePackages, target, package)

	statement = \
		'import os, sys\n' + \
		'sys.path.insert(0, os.path.join(os.path.dirname(__file__), \'{}\'))'.format(target.strip('/\\'))
	print('\nAdd the following to your appengine_config.py:\n')
	print(statement, '\n\n')


if __name__ == '__main__':
	main()
