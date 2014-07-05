__author__ = "Vrubel Dmitrii"
__date__ = "$${date} ${time}$"

import sys
import os

from datetime import datetime 
from zipfile import ZipFile, is_zipfile
from shutil import move

class AgentZip(ZipFile):
	'''Class for zip file with agent for MarioAi: two new methods and some new attributes. Required zipfile and os modules.'''

#	extlist = ['.xml', '.jar']

	agent_class = ''
	agent_package = ''
	agent_xml = ''
	agent_jar = ''
	agent_presentation = ''
	agent_other = []

	def __init__(self, archive):
		ZipFile.__init__(self, archive)
		for name in self.namelist():
			if os.path.splitext(name)[1] == '.class':
				self.agent_class = os.path.splitext(os.path.split(name)[1])[0]
				self.agent_package = os.path.split(name)[0]
			elif os.path.splitext(name)[1] == '.xml':
				self.agent_xml = os.path.splitext(name)[0]
			elif os.path.splitext(name)[1] == '.jar':
				self.agent_jar = os.path.splitext(name)[0]
			elif name.lower() == 'presentation/':
				self.agent_presentation = name[:-1]
			else:
				self.agent_other.append(name)

	def is_valid(self, case_sensitivity=False):
		'''Returns list: [bool, cause], where 'bool' is True or False and cause is the reason of invalid if there is'''

		firstnamelastname = ''		
		if not self.agent_presentation:
			return [False, 'No presentation']
		if self.agent_package:
			firstnamelastname = self.agent_package
		elif self.agent_jar:
			firstnamelastname = self.agent_jar
		elif self.agent_xml:
			firstnamelastname = self.agent_xml
		else:
			return [False, 'No agent files']

		if case_sensitivity:
			if self.agent_package:
				if firstnamelastname != self.agent_package:
					return [False, 'Package name is invalid']
			if self.agent_jar:
				if firstnamelastname != self.agent_jar:
					return [False, '.jar file name is invalid']
			if self.agent_xml:
				if firstnamelastname != self.agent_xml:
					return [False, '.xml file name is invalid']
		else:
			if self.agent_package:
				if firstnamelastname.lower() != self.agent_package.lower():
					return [False, 'Package name is invalid']
			if self.agent_jar:
				if firstnamelastname.lower() != self.agent_jar.lower():
					return [False, '.jar file name is invalid']
			if self.agent_xml:
				if firstnamelastname.lower() != self.agent_xml.lower():
					return [False, '.xml file name is invalid']
		return [True, 'Everything is ok']
		

	def unzip(self, destination, delete=False):
		'''Unzip archive in "destantion" folder. 
		   Attention! Current working directory will be changed!'''
		os.chdir(destination)	
		for file in self.namelist():
			try:
				if os.path.split(file)[0] and os.path.split(file)[1]: 
					os.makedirs(os.path.normpath(os.path.dirname(file)))
				f = open(file,'w')		
				f.write(self.read(file))
				f.close()
			except IOError:
				print 'IOError when ' + file 

if __name__ == "__main__":
	path = '/home/otranto/projects/marioai/downloads/archives/'
	unzipto = '/home/otranto/projects/marioai/downloads/unpacked/'
	done = path + 'done'

	for zip in os.listdir(path):
		os.chdir(path)
		if is_zipfile(zip):
			zipfile = AgentZip(zip)
			print zipfile.is_valid()
			print zipfile.namelist()
			print [zipfile.agent_class, zipfile.agent_package, zipfile.agent_xml, zipfile.agent_jar, zipfile.agent_presentation]
#			destination_folder = unzipto + zip + str(datetime.today()) + '/'
#			try: os.mkdir(destination_folder)
#			except OSError:
#				print '"unzipto" folder already exists'
#			zipfile.unzip(destination_folder)
#			move(path + zip, done)
