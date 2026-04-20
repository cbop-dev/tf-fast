import sys, os
from .env import mylog, debug
from pathlib import Path
from tf.app import use
#from tf.advanced import sections as Sections
from .tfData.tfLXX import TfLXX
from .tfData.tfDataset import TfDataset, POS, PosGroups
from .tfData.tfNT import TfN1904
from .tfData.tfBHS import TfBHS
from .tfData.tfSBLGNT import TfSBLGNT
from .tfData.tfVulgate import TfVulgate
#from contextlib import asynccontextmanager
from .tfData.tfWEB import TfWEB
#from .env import mylog, debug
from tffast.tfData.tfDataset import POS

#debugOn=debug
#debugOn=True
debug = True

DISABLED_DATASETS = os.getenv("DISABLED", '').split(',')

datasetMap = {
	'lxx': TfLXX,
	'nt': TfN1904,
	'bhs': TfBHS,
	'sblgnt': TfSBLGNT,
	'vul': TfVulgate,
	'web': TfWEB,
}

enabledDatasets=['lxx','nt','bhs','sblgnt','vul','web']
for ds in DISABLED_DATASETS:
	if ds in enabledDatasets:
		del enabledDatasets[ds]



# Removed threading import and lock as they are no longer needed for lazy loading
# import threading

dataSets={}
# _dataset_lock = threading.Lock() # Removed

def getDataset(dbname='lxx',theDatasets=dataSets):
	# Datasets are now eagerly loaded by lifespan, so no lazy loading logic is needed here.
	# We just return the pre-loaded dataset.
	
	db=theDatasets.get(dbname)
	
	if(not db):
		if(dbname in datasetMap.keys()):
			print(f"Loading dataset: {dbname}")
			db=datasetMap[dbname]()
			theDatasets[dbname]=db
		else:
			print(f"Dataset {dbname} not found and not loaded!")
			
	else:
		print(f"Dataset {dbname} already loaded!")
		pass
		
	return db


def loadDatasets(enabled=enabledDatasets,theDatasets=dataSets):
	for key in enabled:
		getDataset(dbname=key,theDatasets=theDatasets)
		"""
		if key not in theDatasets.keys():
			mylog(f"Eagerly loading: {key}")
			theDatasets[key]=datasetMap[key]()
		"""
