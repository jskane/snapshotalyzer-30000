from setuptools import setup

setup(
name='snapshotalyzer 30000',
version='0.1',
author='acloudguru via jskane',
author_email='jon.kane@solidstatescientific.com',
description='Snapshotalyzer is a tool that manages EC2 snapshots',
license='GPLv3+',
packages=['shotty'],
url='https://www.github.com/jskane/snapshotalyzer-30000',
install_requires=[
	'click',
	'boto3'
],
entry_points='''
	[console_scripts]
	shotty=shotty.shotty:cli
''',
)