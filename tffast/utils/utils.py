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
				

"""
    function cleanString(str){
        if (str)
            return str.replaceAll(/\s+/g, ' ').trim();
        else 
            return ''
    }

    function cleanNumString(numString){
        return cleanString(numString);
    }
    const nums=[];
    numString = cleanNumString(numString);
    if (numString.length) {
        const sepGroups = numString.split(',');
    for (const group of sepGroups){
        const ranges = group.split("-");
        const min = parseInt(ranges[0]);
        const max = ranges.length > 1 ? parseInt(ranges[1]) : null;

        if (ranges.length > 2) //bad input!
            return [];
        else if (ranges.length == 2 && max){
            if (min < max){
                for (let i = min; i <= max; i++) {
                    if (!nums.includes(i))
                        nums.push(i);
                }
            }
            
        }
        else if (ranges.length == 1){ //no range, just a plain number!
            
            if (!nums.includes(min))
                nums.push(min);
        }
        else{
            //bad input?; don't add anything.
        }
    }
    }
    
    return nums.sort((a,b)=>a-b);
}
"""