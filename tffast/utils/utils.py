import numpy as np

def flatten(thelist):
	return  np.array(thelist).flatten().tolist()

def sortDict(d):
	return dict(sorted(d.items(),key=lambda o:o[1],reverse=True))