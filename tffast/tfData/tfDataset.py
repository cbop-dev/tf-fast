import sys, os
from tf.app import use
from ..env import debug,mylog


class Lexeme:
	def __init__(self,id,lemma,gloss=None,plain=None,translit=None,beta=None,pos=None,lang=None,total=0):
		self.id = id if id else 0
		self.total = total 
		self.gloss = gloss
		self.beta = beta 
		self.translit = translit
		self.lemma = lemma
		self.plain = plain if plain else lemma
		self.pos = pos
		self.lang = lang


class TfDataset:
	def getBeta(self,wordid):
		return self.api.F.lex.v(wordid)
	def getGloss(self, wordid):
		return self.api.F.gloss.v(wordid)
	def getFreq(self,wordid):
		lem = self.getLemma(wordid)
		freqs = [e[1] for e in self.getLemmaFeature().freqList() if e[0] == lem]
		return freqs[0] if len(freqs) > 0 else 0
	
	def getLemma(self,wordid):
		return self.getLemmaFeature().v(wordid)
	
	def getLemmaFeature(self):
		return self.api.F.lemma
	def getAPI(self):
		return self.api
	def getBooksDict(self):
		return self.booksDict
	def __init__(self,datasetPathname,version=None,dbname='lxx'):
		mylog(f"TfDataset.init('{datasetPathname}','{version}')...")
		self.lexemes=set()
		theTfDataset = use(datasetPathname,version=version) #if version else use(datasetPathname)
		if (theTfDataset):
			mylog("TfDataset() got data: ")
			mylog(theTfDataset)
			self.dataset = theTfDataset
			mylog("Got self.dataset: ")
			mylog(self.dataset)
			self.api = self.dataset.api
		else:
			mylog("TfDataset() got no data!")
			self.api = None
		#self.datasets=["yes", "no"]
		self.posDict=None
		self.posGroups=None
		self.bookDict=None
		self.dbname=dbname
		self.buildLexData()

	def buildLexData(self):
		self.lexemes = dict()
		lemmaFreqDict={o[0]:o[1] for o in self.getLemmaFeature().freqList()}
		mylog("buildLexData(): gonna build self.lexemes...")
		self.words = list()
		for w in self.api.F.otype.s('word'):
			lem = self.getLemma(w)
			if lem not in self.lexemes.keys():
				self.lexemes[lem] = Lexeme(0,lem,gloss=self.getGloss(w),
						total=lemmaFreqDict[lem] if lemmaFreqDict[lem] else 0)
			self.words.append(self.getLemma(w))
		self.bookDict = self.getBooks()
		mylog("buildLexData(): done with first loop")
		
		for i, lemLex in enumerate(sorted(self.lexemes.items())):
			lemLex[1].id=i

	def numWords(self,node):
		return len([w for w in self.api.L.d(node) if self.api.F.otype.v(w)=='word'])
	
	def getBooks(self):
		if not self.bookDict:
			self.bookDict = {b: {'name': self.api.F.book.v(b), 'abbrev':self.api.F.book.v(b), 'words':self.numWords(b)} for b in self.api.F.otype.s('book')}
		return self.bookDict
	
	def getLexCount(self):
		count = 0
		if (self.lexemes):
			count = len(self.lexemes)
		return count
	
	def isProperNoun(self, wordid):
		return (self.api.F.sp.v(wordid) == 'noun') and self.api.F.lex_utf8.v(wordid)[0].isupper()
	def getLexObj(self,wordid):
		return None
	
	# getLex: returns Lexeme object with given ID. (NB: 'id' is assigned by buildLexData() function, using indexes of sorted lemmas. I.e., the first alphabetically listed lemma has an id of 0, the last one has 5395)
	def getLex(self,lexID):
		foundLexes = [l for l in self.lexemes.values() if l.id==lexID]
		if len(foundLexes) > 0:
			return foundLexes[0]
		else:
			return None

	
		# returns dict of lexemes and frequencies:
	def getLexemes(self,sections=[], restrict=[],exclude=[], min=1, gloss=False, totalCount=True,pos=False,checkProper=True, beta=True,type='all',common=False,plain=False):
		#mylog("Min: " + str(min))
		
		lexemes = {}
		sectionsLexemes = {}

		totalInstances = 0
		totalLexemes = 0
		totalWordsInSections = 0

		restrictStrings=[v['desc'] for (k,v) in self.posDict.items() if k in restrict]
		excludeStrings=[v['desc'] for (k,v) in self.posDict.items() if k in exclude]
		#print("restrictStrings: " + str(restrictStrings))
		restricted = True if len(restrictStrings) > 0 else False
		excluded  = True if len(excludeStrings) > 0 else False
		
		def includeWord(wordid):
			wordid=int(wordid)
			include = False
			nonlocal beta
			nonlocal checkProper
			nonlocal excludeStrings
			nonlocal excluded
			nonlocal gloss
			nonlocal pos
			nonlocal plain
			nonlocal restrictStrings
			nonlocal restricted
			nonlocal totalCount
			nonlocal totalInstances
			nonlocal totalLexemes
			nonlocal totalWordsInSections


			if (self.api.F.otype.v(wordid) == 'word'):
				#beta = F.lex.v(wordid)
				totalWordsInSections += 1
				#greek = F.lex_utf8.v(wordid)
				
				if (checkProper and self.isProperNoun(wordid)):
					# we have a name, and must account for that fact:
					if ((not excluded or 26 not in exclude) 
						and (not restricted or 26 in restrict)): #we should include it
						include = True
				else:# don't need to worry about names
					thePos = self.api.F.sp.v(wordid)
					if ( (not excluded or thePos not in excludeStrings)  
						and (not restricted or thePos in restrictStrings)):
						include = True
			
			return include
			

		def addLexes(nodeid,recursive=False):
			def addLex(wordid):
				nonlocal totalInstances
				nonlocal totalLexemes
				nonlocal totalWordsInSections
				nonlocal beta
				nonlocal plain
				nonlocal gloss
				nonlocal totalCount
				nonlocal pos

				if(includeWord(wordid)):	
					
					totalInstances += 1
					if (not self.getLemma(wordid) in lexemes.keys()):
						totalLexemes +=1
						lexemes[self.getLemma(wordid)] = {'count': 1, 'id': wordid}
						# track which of the give sections this word is in:
						if (common):
							sectionsLexemes[self.getLemma(wordid)]=set([int(s) for s in (set(L.u(wordid)) & set(sections))])

						if (totalCount):
							lexemes[self.getLemma(wordid)]['total'] = int(self.getLexCount(wordid));
						if (gloss):
							lexemes[self.getLemma(wordid)]['gloss'] = self.getGloss(wordid)
						if (beta):
							lexemes[self.getLemma(wordid)]['beta'] = self.getBeta(wordid)
						if (pos):
							lexemes[self.getLemma(wordid)]['pos'] = self.api.F.sp.v(wordid)
							#print("Got pos!")
							if (lexemes[self.getLemma(wordid)]['pos'] == 'noun' and self.getLemma(wordid)[0].isupper()):
								if (checkProper):
									lexemes[self.getLemma(wordid)]['pos'] = 'proper noun or name'
								else:
									lexemes[self.getLemma(wordid)]['proper'] = True
					else:
						lexemes[self.getLemma(wordid)]['count'] += 1
						if (common):
							sectionsLexemes[self.getLemma(wordid)].update([int(s) for s in (set(self.api.L.u(wordid)) & set(sections))])
			
			id=int(nodeid)
			if (self.api.L.d(id) and not recursive):
				for w in self.api.L.d(id):
					addLexes(w,recursive=True)
			elif(self.api.F.otype.v(id) == 'word'):
				addLex(id)
			
		#print("sections: " + str(sections))
		if(len(sections) > 0):
			for s in sections:
				s=int(s)
				foundSuper = False
				for supersect in self.api.L.u(s):
					if ((str(supersect) in sections) or (supersect in sections)):
						foundSuper = True
				if(not foundSuper):
					addLexes(s)
		else:
			for o in self.api.N.walk():
				addLexes(o)
		#print(lexemes)		
		# sort lexemes?
		# 
		# 	
		theResponseObj = {
			'totalInstances': totalInstances,#i.e., number of words in this section
			'totalLexemes': totalLexemes,
			'totalWords':totalWordsInSections,
			'lexemes': lexemes if min == 1 else {k:v for (k,v) in lexemes.items() if int(v['count']) >= int(min)}
		}
		
		if (common):
			commonLexes = [g for (g,ss) in sectionsLexemes.items() if set(sections) <= ss]
			#print("commonlexes length: " + str(len(commonLexes)))
		#	print("set repon.common to: "+str(len(theResponseObj['common'])))
			theResponseObj['common']=commonLexes
		return  theResponseObj
		
	def getChaptersDict(self,book):
		#mylog("getChapters(" + str(book) + "," + db +")")
		return dict([(self.api.F.chapter.v(c), c) for c in self.api.L.d(book) if self.api.F.otype.v(c)=='chapter'])
		
	#def getBooksDict(self):
	#	return dict([(b, self.api.F.book.v(b)) for b in self.api.N.walk() if self.api.F.otype.v(b) == 'book'])

### pasted from init.py:
	def getVersesFromNodeRange(self,startNode,endNode,showVerses=False):
		text = ''
		print("getVersesFromNodeRange(" +str(startNode) + ","+str(endNode)+")")
		
		if (startNode == endNode):
			text += self.api.T.text(startNode)
			print("	got single node; text= " + text)
		elif (startNode > 0 and endNode >= startNode):
			for i in range(startNode,endNode+1,1):
				if(self.api.F.otype.v(i) =='verse'):
					if(showVerses):
						sec=api.T.sectionFromNode(i)
						if (sec[2]):
							text+= str(sec[2]) +'. '
					text += self.api.T.text(i)
				else:
					print("Node " + str(i) + " was not a verse, but is: " + self.api.F.otype.v(i) +", text = " + self.api.T.text(i))
			print("	got range. text = " + text)

		return text.strip()
	
	# returns refs as {'refs': <string array>, 'nodes': <int array of verses>, 'bookCounts': <dict of booksids->count>, 'total', <total instances in BHS>}
	def getLexRefs(self,id,sections=[],detail=''):
		
		# optionally limits to instances within any of the selected sections, exluding all others:
		id=int(id)
		sections = [int(s) for s in sections] if sections.length else []
		mylog("getrefs: sections = [" + ",".join([str(s) for s in sections])+"]")
		if(self.api.F.otype.v(id) == 'word'):
			lex=self.lex(id)
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
			for n in self.api.N.walk():
				if (self.api.F.otype.v(n) == 'word' and self.lex(n) == lex and (len(sections) == 0 or (len(set(self.api.L.u(n)) & set(sections)) > 0) )):
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
					bookid=api.L.u(n)[-1]
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
		
		try:
			return self.api.T.text(int(nodeId)).strip()
		except:
			return ''

	def getRef(self,nodeId):
		try:
			return " ".join(map(str, self.api.T.sectionFromNode(int(nodeId))))
		except:
			return ''


	def getNodeFromBcV(self,book,chapter,verse):
		node = 0
		
		print("calling nodeFromSection(" + book + "," + str(chapter) +"," + str(verse)+")")
		
		node=self.api.T.nodeFromSection((book,int(chapter),int(verse)))
		if (type(node) != int):
			node = 0
		print("...got node" + str(node))
		return node



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


