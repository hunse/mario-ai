import os
from agent_class import *
#from zipfile import ZipFile, is_zipfile


 
if __name__ == "__main__":

	options = {}
	
	for i in range(0, len(sys.argv[1:]) / 2):
		options[sys.argv[2 * i + 1]] = sys.argv[2 * (i + 1)]
	print options

	for zip in os.listdir(options['-ufrom']):
		os.chdir(options['-ufrom'])
		if is_zipfile(zip):
			agent = AgentZip(zip)
			if agent.is_valid()[0]:
				agent.unzip(options['-uto'])
				os.system('cd ' + options['-benchmark'] + '; java ch.idsia.scenarios.Main -ag ' +  options['-track'] + '.' + options['-event'] + '.' + agent.agent_package + '.' + agent.agent_class + ' > ' + options['-log'])
			else:
				print agent.is_valid[1]
		if options['-delete'] == 'yes':
			os.remove(options['-ufrom']+zip)
