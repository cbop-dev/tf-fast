import numpy as np

def flatten(thelist):
	return  np.array(thelist).flatten().tolist()

def sortDict(d):
	return dict(sorted(d.items(),key=lambda o:o[1],reverse=True))

def cleanString(str,removeSpaces=True):
	
	if (str and removeSpaces):
		str= str.replace(" ", "")
	return str.strip()


def cleanNumString(numString):
	return cleanString(numString)

def createNumArrayFromStringListRange(numString):
	
	nums=[]
	numString=cleanNumString(numString)
	if (len(numString)):
		sepGroups = numString.split(',')
		for group in sepGroups:
			if(group):
				ranges=group.split('-')
				min=int(ranges[0]) if len(ranges)>0 else None
				max=int(ranges[-1]) if len(ranges)>1 else None
				if(len(ranges)>2):
					pass #bad input
				elif(len(ranges)==2 and min > 0 and max > min):
					for i in range(min,max+1):
						if i not in nums:
							nums.append(i)
				elif(len(ranges)==1 and min > 0): ## just a number
					if min not in nums:
						nums.append(min)
	return sorted(nums)	
