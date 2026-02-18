def sortDict(d):
	return dict(sorted(d.items(),key=lambda o:o[1],reverse=True))