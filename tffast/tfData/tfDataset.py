import sys, os
from collections import Counter
from tf.app import use
from ..env import debug,mylog
from ..utils.greekUtils import GreekUtils
from ..utils.hebrewUtils import HebrewUtils



class Lexeme:
	def __init__(self,id,lemma,wordid=0,gloss=None,plain=None,translit=None,beta=None,pos=None,lang=None,strongs=None,total=0,isProper=False):
		self.id = id if id else 0
		self.wordid=wordid # a node id in which this lexeme is found as a word in DB (important if self.id does not correspond to node ids)
		self.total = total 
		self.gloss = gloss
		self.strongs=strongs
		self.translit = translit if translit else GreekUtils.greek_to_beta(GreekUtils.remove_diacritics(lemma))
		self.beta = beta if beta else translit
		self.lemma = lemma
		self.plain = plain if plain else self.getPlain(wordid)
		self.pos = pos
		self.lang = lang
		self.isProper = isProper


class TfDataset:
	def getBeta(self,wordid):
		return self.api.F.lex.v(wordid)#does not work for nt, must override.
	def getPlain(self,wordid):
		return self.getBeta(wordid) #treat same as beta; override in child class as necessary.
	def getGloss(self, wordid):
		return self.api.F.gloss.v(wordid) if 'gloss' in self.api.Fall() else ''
	def getLexiconEntry(self,wordNode):
		output = self.getLexiconEntryFeature().v(wordNode) if self.getLexiconEntryFeature() else None
		#if (not output):
			#mylog(f"Got no LexiconEntry(${wordNode})")

	def getFreq(self,wordid):
		lem = self.getLemma(wordid)
		freqs = [e[1] for e in self.getLemmaFeature().freqList('word') if HebrewUtils.normalize(e[0]) == lem]
		return freqs[0] if len(freqs) > 0 else 0
	

	def getLemma(self,wordid):
		return HebrewUtils.normalize(self.getLemmaFeature().v(wordid))
	
	def getLexiconEntryFeature(self):
		return None

	def getLemmaFeature(self):
		return self.api.F.lemma
	def getAPI(self):
		return self.api
	def getBooksDict(self):
		return self.booksDict
	def __init__(self,datasetPathname,version=None,dbname='lxx', dataset=None,buildLexData=True,modules=None,path=None,mod=None):
		mylog(f"TfDataset.init('{datasetPathname}','{version}')...")
		self.lexemes=dict() # lemma:str-->Lexeme class instance
		
		locations=[path] if path else ['']
		mydata=dataset
		if (not mydata):
			if (modules and len(modules) and len(locations)):
				#print(f"invoking use() with modules='${','.join(modules)}'")
				mydata = use(datasetPathname,version=version,locations=locations,modules=modules) if modules else use(datasetPathname,version=version)
			elif (mod):
				#print(f"invoking use() with mod='${mod}'")
				mydata = use(datasetPathname,version=version,mod=mod) 
			else:
				#print(f"invoking vanilla use()!")
				mydata=use(datasetPathname,version=version)
		else:
			print(f"Go some data: ${mydata}")
			
		if (mydata):
			mylog(f"TfDataset({dbname},{datasetPathname}) got data: ")
			mylog(mydata)
			self.dataset = mydata
			#mylog("Got self.dataset: ")
			#mylog(self.dataset)
			self.api = self.dataset.api
		else:
			mylog("TfDataset() got no data!")
			self.api = None
		
		self.posDict=None if not hasattr(self,'posDict') else self.posDict
		self.posGroups=None if not hasattr(self,'posGroups') else self.posGroups
		self.booksDict=None if not hasattr(self,'booksDict') else self.booksDict
		self.dbname=dbname
		if (buildLexData):
			self.buildLexData()

	def normalize(self,string):
		return string

	def buildLexData(self):
		self.lexemes = dict()#lemma:str->Lexeme
		lemmaFreqDict={HebrewUtils.normalize(o[0]):o[1] for o in self.getLemmaFeature().freqList('word')}
		#mylog("buildLexData(): gonna build self.lexemes...")
		self.words = list()
		for w in self.api.F.otype.s('word'):
			lem = self.getLemma(w)
			if lem not in self.lexemes.keys():
				self.lexemes[lem] = Lexeme(0,lem,gloss=self.getGloss(w),beta=self.getBeta(w),plain=self.getPlain(w),strongs=self.getStrongs(w),
						total=lemmaFreqDict[lem] if lemmaFreqDict[lem] else 0,isProper=self.isProperNoun(w),pos=self.pos(w))
			self.words.append(self.getLemma(w))
		self.booksDict = self.getBooks()
		#mylog("buildLexData(): done with first loop")
		
		for i, lemLex in enumerate(sorted(self.lexemes.items(),key=lambda l: l[1].plain.lower())):
			lemLex[1].id=i

	def numWords(self,node):
		return len([w for w in self.api.L.d(node) if self.api.F.otype.v(w)=='word'])

	def getBooks(self):
		if not self.booksDict:
			self.booksDict = {b: {'name': self.api.F.book.v(b), 'abbrev':self.api.F.book.v(b), 'words':self.numWords(b), 'chapters':len(self.api.L.d(b,'chapter')), 'lemmas':self.getLexemes2(sections=[b])['totalLexemes']} for b in self.api.F.otype.s('book')}
		return self.booksDict

	def getLexCount(self,wordid=0):

		count = 0
		if (wordid== 0 and self.lexemes):
			count = len(self.lexemes)
		else:
			foundLexCounts = [t[1] for t in self.getLemmaFeature().freqList('word') if t[0]==self.getLemma(wordid)]
			count = foundLexCounts[0] if len(foundLexCounts) > 0 else 0

		return count
	
	def isProperNoun(self, wordid):
		return (self.pos(wordid) == 'noun') and self.api.F.lex_utf8.v(wordid)[0].isupper()

	def getLexObj(self,wordid):
		return None
	
	# TODO: rethink/decide how to calculate lexID. Should this be the index of a sorted list of lexes? (thus only calculated after all lexemes have been processes/sorted)
	# TODO: test this with LXX and lxx-web...
	def getLexID(self,wordid):
		lemma=self.getLemma(wordid)
		return self.lexemes[lemma].id if lemma and self.lexemes[lemma] else 0
		
	def getStrongs(self,wordNodeId):
		output=''
		if 'strongs' in self.api.Fall():
			output=self.api.F.strongs.v(wordNodeId)
		return output

	# TODO: rethink "lexID" here, depending on implementation of getLexID().  and add "getLemmaByNodeID"?
	# getLex: returns Lexeme object with given ID. 
	# (NB: 'id' is assigned by buildLexData() function, using indexes of sorted lemmas. 
	# I.e., the first alphabetically listed lemma has an id of 0, the last one has 5395)
	def getLex(self,lexID):
		foundLexes = [l for l in self.lexemes.values() if l.id==lexID]
		if len(foundLexes) > 0:
			return foundLexes[0]
		else:
			return None

	def properNounKey(self):
		return -1
		# returns dict of lexemes and frequencies:

	def countLexInSection(self,lemma,section):
		count = 0
		lemma=HebrewUtils.normalize(lemma)
		if (self.api.F.otype.v(section) == 'word'):
			if (self.getLemma(section) == lemma):
				count = 1			
		else:
			count = len([self.getLemma(w) for w in self.api.L.d(section,'word') if self.getLemma(w) == lemma])
		return count


	def pos(self,wordid):
		return self.api.F.sp.v(wordid)
	
	# return object:{
	# 		totalInstances: number of relevant words found in this section according to query parameters. How to calculate efficiently?
	#		totalLexemes: totalLexemes,
	#		totalWords:totalWordsInSections,  total words, regardless of any query parameters
	#		lexemes: (todo)
	# }
	# params: min/max: how many total BHS instances of lex
	def getLexemes2(self,sections=[], restrict=[],exclude=[], min=0, gloss=False, max=0,
				totalCount=True,pos=False,checkProper=True, beta=True,type='all',common=False,plain=False):
		#mylog("Min: " + str(min))
		

		# lexemes{dict}: {lex:{'lexObj':{Lexeme}, 'count':{number}} where lex{string}=lemma string (key to self.lexemes)
		lexemes = {} 
		sectionsLexemes = {}# nodeid:{string:number, where string is dict entry / key value {string}

		#totalInstances = 0
		#totalLexemes = 0
		totalWordsInSections = 0

		
		restrictStrings=[v['desc'] for (k,v) in self.posDict.items() if k in restrict] if(self.posDict and len(self.posDict.items())) else []
		excludeStrings=[v['desc'] for (k,v) in self.posDict.items() if k in exclude] if(self.posDict and len(self.posDict.items())) else []
		#mylog("restrictStrings: " + str(restrictStrings))
		excludeProperNouns = self.properNounKey() in excludeStrings
		restrictProperNouns = self.properNounKey() in restrictStrings
		restricted = True if len(restrictStrings) > 0 else False
		excluded  = True if len(excludeStrings) > 0 else False
		#validLexes =[l for (l,lexObj) in self.lexemes.items() if 
		#	(not checkProper or (lexObj.isProper and excludeProperNouns and not restrictProperNouns)) 
		#	and (not excluded or (lexObj.pos not in excludeStrings)  
		#		and (not restricted or (lexObj.pos in restrictStrings)))]

		if(len(sections)==0):
		#get all word ids for each sections
			sections=self.booksDict.keys()

		for s in sections:

			words=[]
			if (self.api.F.otype.v(s) == 'word' or self.api.F.otype.v(s) == 'lex' or self.api.F.otype.v(s) == 'lemma'):
				
				sectionsLexemes[s]= self.getLemma(s)
				totalWordsInSections+=1
			#	totalInstances+=1
			else:
				words = self.api.L.d(s,'word')
				totalWordsInSections+= len(words)
				sectionsLexemes[s] = [self.getLemma(w) for w in words]

				
		
		sectionLexSets=[set(s) for s in sectionsLexemes.values()]
		tmpLexemes = []
		if (len(sectionLexSets)):
			tmpLexemes = list(set.union(*sectionLexSets))
		#if (common):
#			tmpLexemes = list(set.intersection(*sectionLexSets))
#		else:
#			tmpLexemes = list(set.union(*sectionLexSets))

		
		#lexemes ={l:{'lexObj': self.lexemes[l]} for l in tmpLexemes if self.lexemes[l] and (
		#	(not checkProper or (self.lexemes[l].isProper and excludeProperNouns and not restrictProperNouns)) 
		#	and (not excluded or (self.lexemes[l].pos not in excludeStrings)  
		#		and (not restricted or (self.lexemes[l].pos in restrictStrings))))}

		for l in tmpLexemes:
			lexObj = self.lexemes[l] if l in self.lexemes.keys() else None
			if (lexObj and
				(
					(not checkProper or not excludeProperNouns or (lexObj.isProper or not restrictProperNouns)) 
					and (not excluded or (lexObj.pos not in excludeStrings))  
					and (not restricted or (lexObj.pos in restrictStrings))
				)
			):#include!
				#mylog(f"including Lex '{lexObj.lemma}' with pos '{lexObj.pos}'")
				lexemes[l]={
					'id':lexObj.id,
					'beta':lexObj.beta,
					 'gloss': lexObj.gloss,
					 'pos': lexObj.pos,
					 'total':lexObj.total,
					 
					 
				}
				if (lexObj.strongs):
					lexemes[l]['strongs']=lexObj.strongs

		keys=lexemes.keys()
		lexCounts = Counter([l for s in sectionsLexemes.values() for l in s if l in keys])

		for (l,obj) in lexemes.items():
			obj['count']=lexCounts[l]




		
		#mylog(lexemes)		
		# sort lexemes?
		# 
		# 	
		theResponseObj = {
			#'totalInstances': 0,#,sum([len(s) in sectionsLexemes,#i.e., number of relevant words found in this section according to query parameters. How to calculate efficiently?
			'totalLexemes': len(lexemes.keys()),
			'totalWords':totalWordsInSections, # total words, regardless of any query parameters
			'lexemes': lexemes if min <= 1 and max == 0 else {k:v for (k,v) in lexemes.items() if (int(v['total']) >= int(min) and int(v['total']) <= int(max))}
		}
		
		if (common):
			commonLexes = list(set.intersection(*sectionLexSets))
			#=[g for (g,ss) in sectionsLexemes.items() if set(sections) <= set(ss)]
			#mylog("commonlexes length: " + str(len(commonLexes)))
		#	mylog("set repon.common to: "+str(len(theResponseObj['common'])))
			theResponseObj['common']=commonLexes
		#print(f"getLexemes2() reponse obj.totalWords={theResponseObj['totalWords']}")
		return  theResponseObj
	
	def lookupChapters(self,name):
		## name: name or abbreviation  of book to lookup
		## returns: dictionary of {chapterNum : node ID} for given book.
		ret = {}
		bNode = self.lookupBook(name)
		if (bNode):
			ret = self.getChaptersDict(bNode)

		return ret

	def lookupChapter(self,bookname,chapNum) -> int:
		
		bNode = self.lookupBook(bookname)
		return self.getChapter(bNode,chapNum) if bNode else None



		
	def getChaptersDict(self,book):
		#mylog("getChapters(" + str(book) + "," + db +")")
		return dict([(self.api.F.chapter.v(c), c) for c in self.api.L.d(book) if self.api.F.otype.v(c)=='chapter'])
		
	def getChapter(self,bookID,chapNum):
		chapDict = self.getChaptersDict(bookID)
		chapNode = None
		if (chapNum in chapDict.keys()):
			chapNode = chapDict[chapNum]

		return chapNode
	#def getBooksDict(self):
	#	return dict([(b, self.api.F.book.v(b)) for b in self.api.N.walk() if self.api.F.otype.v(b) == 'book'])

### pasted from init.py:
	def getVersesFromNodeRange(self,startNode,endNode,showVerses=False):
		text = ''
		mylog("getVersesFromNodeRange(" +str(startNode) + ","+str(endNode)+")")
		
		if (startNode == endNode):
			text += self.api.T.text(startNode)
			mylog("	got single node; text= " + text)
		elif (startNode > 0 and endNode >= startNode):
			for i in range(startNode,endNode+1,1):
				if(self.api.F.otype.v(i) =='verse'):
					if(showVerses):
						sec=api.T.sectionFromNode(i)
						if (sec[2]):
							text+= str(sec[2]) +'. '
					text += self.api.T.text(i)
				else:
					mylog("Node " + str(i) + " was not a verse, but is: " + self.api.F.otype.v(i) +", text = " + self.api.T.text(i))
			mylog("	got range. text = " + text)

		return text.strip()
	
	# returns refs as {'refs': <string array>, 'nodes': <int array of verses>, 'bookCounts': <dict of booksids->count>, 'total', <total instances in BHS>}
	def getLexRefs(self,id,sections=[],detail=''):
		
		# optionally limits to instances within any of the selected sections, exluding all others:
		id=int(id)
		sections = [int(s) for s in sections] if len(sections) else []
		mylog("getrefs: sections = [" + ",".join([str(s) for s in sections])+"]")
		if(self.api.F.otype.v(id) == 'word'):
			lex=self.getLex(id)
			
			rNodes = {}
			bookCounts = {}
			queryDetail = 'verse'
			verseCounts={}
			if (detail):
				if (detail == "book"):
					queryDetail = 'book'
				elif (detail == "chapter"):
					queryDetail = 'chapter'

			#refs = {}
			for n in self.api.F.otype.s('word'):
				if (self.getLexID(n) == lex.id and (len(sections) == 0 or (len(set(self.api.L.u(n)) & set(sections)) > 0) )):
					sectionTuple= self.api.T.sectionTuple(n)
					if (queryDetail == 'book'):
						sectionNode = sectionTuple[0]
					elif (queryDetail == 'chapter'):
						sectionNode = sectionTuple[1]
					else:
						sectionNode = sectionTuple[2]

					#rNodes.add(sectionNode) # gets node of containing verse
					refTuple = self.api.T.sectionFromNode(n) # gets tuple of containing verse
					if (queryDetail == 'book'):
						refString = refTuple[0]
					elif (queryDetail == 'chapter'):
						refString = refTuple[0] + " " + str(refTuple[1])
					else:
						refString = refTuple[0] + " " + ":".join(map(str,refTuple[1:]))
					#refs.add(refString)
					bookid=self.api.L.u(n,'book')[0]
					if bookid not in bookCounts:
						bookCounts[bookid]=1
					else:
						bookCounts[bookid] +=1
					if sectionNode not in rNodes:
						rNodes[sectionNode]=refString
						verseCounts[sectionNode]=1
					else:
						verseCounts[sectionNode] +=1
						#rNodes[sectionNode]=refString+"(" + str(verseCounts[sectionNode]) + ")"

			return {'refs': list(rNodes.values()), 'nodes': list(rNodes.keys()), 'bookcounts': dict(bookCounts), 'total': sum(bookCounts.values())}
		else:
			return ''

	def getText(self,nodeId):
		if (nodeId > 0):
			try:
				return self.api.T.text(int(nodeId)).strip()
			except:
				return ''
		else:
			return ''

	def getRef(self,nodeId):
		try:
			return " ".join(map(str, self.api.T.sectionFromNode(int(nodeId))))
		except:
			return ''

	
	
	def apparatusNote(self,book,chapter,verse):
		return ""

	def apparatusNotesForNode(self,node):
		notes=[]
		node=int(node)
		if (type(node)== int):
			if (self.api.F.otype.v(node)=='verse'):
				ref=self.api.T.sectionFromNode(node)
				notes.append(self.apparatusNote(ref[0],ref[1],ref[2]))
			else:
				for v in self.api.L.d(node,'verse'):
					ref=self.api.T.sectionFromNode(v)
					notes.append(self.apparatusNote(ref[0],ref[1],ref[2]))
		
		return notes

	def getNodeFromBcV(self,book,chapter,verse):
		node = 0
		
		node=self.api.T.nodeFromSection((book,int(chapter),int(verse)))
		mylog(f"calling nodeFromSection(('{book}', {str(chapter)},{str(verse)}))=>{node}")
		if (type(node) != int):
			node = 0
		#mylog(" " + str(node))
		return node


	def getVerseNumberFromNode(self,node):
		return self.api.T.sectionFromNode(int(node))[-1] if len(self.api.T.sectionFromNode(int(node))) >= 3 else None
	
	def sectionFromNode(self,node):
		
		section= self.api.T.sectionFromNode(node)
		string = ''
		if (len(section) == 3):
			string = str(section[0]) + " " + str(section[1]) + ":" + str(section[2])
		elif (len(section) == 2):
			string = str(section[0]) + " " + str(section[1])
		else:#book only:
			string = str(section[0])
		return string
	
	## static class function!
	def consolidateBibleRefs(strings):
		outString = ''
		if(len(strings) > 1):
			bookHash = {}
			for s in strings:
				if (" " in s):
					(book,chapV) = s.split(" ")
					if (book not in bookHash.keys()):
						bookHash[book] = {}#indexed by chaps
					if (":" in chapV):
						(chap, verse) = chapV.split(":")
						if (chap not in bookHash[book].keys()):
							bookHash[book][chap] = [verse]
						else:
							bookHash[book][chap].append(verse)
					else: # no verse given
						if (chapV not in bookHash[book].keys()):
							bookHash[book][chapV] = []
						#else: #chap exists, but no need to add since we don't have a verse
				else: #book only
					if (s not in bookHash.keys()):
						bookHash[s]={}

			#mylog(bookHash)
			
			for (b,cvs) in bookHash.items():
				outString = b + " " if not outString else outString + "; " + b
				cvss = ''
				for (c, vs) in cvs.items():
					if (cvss):
						cvss += "; " + c 
					else:
						cvss += " " + c

					vss = ",".join(vs)
					if (vss):
						cvss += ":" + vss
					
				outString += cvss
				
		else:
			outString = strings[0]
		
		return outString
	def lookupBook(self,string):
		matches=[n for (n,o) in self.booksDict.items() if string in o['syn']]
		match=None
		if (len(matches)):
			match=matches[0]
		return match
	
	def getHandyDictionary(self,bookname,chapter=None,verses=[],min=0,max=0):
		bookNode=self.lookupBook(bookname)
		
		nodes=[]
		if (bookNode):
			if (chapter):
				if (len(verses)): #book, chap, and vv!
					nodes=[self.getNodeFromBcV(self.booksDict[bookNode]['name'],chapter,v) for v in verses]
					print(f"Got book,chap,v:[{','.join(map(str,nodes))}]")
				else:#chap only
					nodes.append(self.lookupChapter(bookname,chapter))
					print("Got book + chap only!")
			else: #bookonly
				nodes.append(bookNode)
				print("Got book only!")
		else:
			print("Got no book node! Uh oh!")
		
		return {k:{'gloss':l['gloss'],'strongs':l['strongs']} for k,l in self.getLexemes2(sections=nodes,min=min,max=max)['lexemes'].items()} if len(nodes) else {}

	def getBookWordsSorted(self):
		return dict(sorted({self.booksDict[b]['abbrev']:len(self.api.L.d(b,'word')) for b in self.getBooks().keys()}.items(),key=lambda o:o[1],reverse=True))