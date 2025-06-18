import datetime
debug = False
def mylog(msg, debugOn=debug,showTime=False):
	if(debugOn):
		msg = (msg + "[TIME: " + str(datetime.datetime.now())) if showTime else msg
		print(msg)
