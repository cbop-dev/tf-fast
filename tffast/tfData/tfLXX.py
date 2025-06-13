import sys, os
from tf.app import use
from tf.advanced import sections
from pathlib import Path
from .tfDataset import TfDataset
from ..env import mylog
class TfLXX(TfDataset):
	posDict={
		0:  {'abbrev': 'n', 'desc':  'noun',},
		1:  {'abbrev': 'v', 'desc':  'verb',},
		2:  {'abbrev': 'adj', 'desc':  'adjective',},
		3:  {'abbrev': 'adj1', 'desc':  'adjective, 1st declension, -??/-?/-?? pattern endings',},
		4:  {'abbrev': 'adj3', 'desc': 'adjective, 3rd declension pattern endings',},
		5:  {'abbrev': 'adv', 'desc': 'adverb',},
		6:  {'abbrev': 'pers', 'desc': 'pronoun, personal/possessive',},
		7:  {'abbrev': 'rel', 'desc':  'pronoun, relative',},
		8:  {'abbrev': 'ar', 'desc':  'pronoun, article',},
		9:  {'abbrev': 'demon', 'desc':  'pronoun, demonstrative',},
		10:  {'abbrev': 'rel2', 'desc': 'pronoun, relative, ?????',},
		11:  {'abbrev': 'c', 'desc': 'conjunction',},
		12:  {'abbrev': 'prep', 'desc':  'preposition',},
		13:  {'abbrev': 'part', 'desc': 'particle',},
		14:  {'abbrev': 'num', 'desc':  'indeclinable number',},
		15:  {'abbrev': 'intero', 'desc':  'pronoun, interrogative/indefinite',},
		16:  {'abbrev': 'interj', 'desc':  'interjection',},
		17:  {'abbrev': 'c+demon', 'desc':  'conjunction + pronoun, demonstrative',},
		18:  {'abbrev': 'c+rel', 'desc': 'conjunction + pronoun, relative',},
		19:  {'abbrev': 'c+part', 'desc': 'conjunction + particle',},
		20:  {'abbrev': 'c+adv', 'desc': 'conjunction + adverb',},
		21:  {'abbrev': 'ar+adj', 'desc': 'pronoun, article + adjective',},
		22:  {'abbrev': 'pers+part', 'desc': 'pronoun, personal/possessive + particle',},
		23:  {'abbrev': 'prep+adj', 'desc': 'preposition + adjective',},
		24:  {'abbrev': 'prep+part', 'desc': 'preposition + particle',},
		25:  {'abbrev': 'demon+n', 'desc':  'pronoun, demonstrative + noun'},
		26:  {'abbrev': 'name', 'desc':  'proper noun or name'},
	}

	posGroups={
		"CONT":[0,1,2,3,4,5],
		"CONTENT":[0,1,2,3,4,5],
		"SYNT":list(range(17,26)),#NB: excludes last item
		"SYNTAX":list(range(17,26)),
		"PREP":[16,23,24],
		"PREPOSITIONS":[16,23,24],
		"PREPOSITION":[16,23,24],
		"PART":[19,25],#I'm not counting 13 (pers+part) or 24 (prep+part)
		"PARTICLES":[19,25],
		"PARTICLE":[19,25],
		"PRON":list(range(6,14)),
		"PRONOUNS":list(range(6,14)),
		"PRONOUN":list(range(6,14)),
			
	}
	bookDict={#indexed by the tf node ids, with various synonyms for searching/looking-up.
		623694: {'abbrev': "Gen", 'syn': ['Gen', 'Genesis', 'Ge']},
		623695: {'abbrev': "Exod", 'syn': ['Exod', 'Exodus']},
		623696: {'abbrev': "Lev", 'syn': ['Lev', 'Leviticus']},
		623697: {'abbrev': "Num", 'syn': ['Num', 'Numbers']},
		623698: {'abbrev': "Deut", 'syn': ['Deut', 'Deuteronomy', 'Dt', 'Deu']},
		623699: {'abbrev': "Josh", 'syn': ['Josh', 'Joshua']},
		623700: {'abbrev': "Judg", 'syn': ['Judg', 'Judges', 'Jdg', 'Jdgs', "Judgs"]},
		623701: {'abbrev': "Ruth", 'syn': ['Ruth', 'Ruth']},
		623702: {'abbrev': "1Sam", 'syn': ['1 Sam', '1 Samuel', 'I Samuel','1 Sa', '1 Sam','I Sa', 'I Sam','1 Kgdms', '1 Kingdoms','I Kingdoms','I Kgdms',]},
		623703: {'abbrev': "2Sam", 'syn': ['2 Sam', '2 Samuel', 'II Samuel','2 Sa', '2 Sam','II Sa', 'II Sam','2 Kgdms', '2 Kingdoms','II Kingdoms','II Kgdms', '2 Kgdms', '2 Kingdoms','II Kingdoms','II Kgdms']},
		623704: {'abbrev': "1Kgs", 'syn': ['1 Kgs', '1 Kings', 'I Kings','1 Kg', 'I Kg', '3 Kgdms', '3 Kingdoms','III Kingdoms','III Kgdms']},
		623705: {'abbrev': "2Kgs", 'syn': ['2 Kgs', '2 Kings', 'II Kings','2 Kg', 'II Kg', '4 Kgdms', '4 Kingdoms','IV Kingdoms','IV Kgdms']},
		623706: {'abbrev': "1Chr", 'syn': ['1 Chr', '1 Chronicles', '1 Chron', '1 Ch','I Chronicles', 'I Chron', 'I Ch','I Chr']},
		623707: {'abbrev': "2Chr", 'syn': ['2 Chr', '2 Chronicles', '2 Chron', '2 Ch', 'II Chronicles', 'II Chron', 'II Ch','II Chr']},
		623708: {'abbrev': "1Esdr", 'syn': ['Ezra', 'Ezra', '1 Esdras', 'I Esdras', '1 Esdr', 'I Esdr']},
		623709: {'abbrev': "2Esdr", 'syn': ['Neh', 'Nehemiah',  '2 Esdras', 'II Esdras', '2 Esdr', 'II Esdr']},
		623710: {'abbrev': "Esth", 'syn': ['Esth', 'Esther', 'Est']},
		623711: {'abbrev': "Jdt", 'syn': ['Jdt', 'Judith']},
		623712: {'abbrev': "TobBA", 'syn': ['Tob', 'Tobit', 'Tob BA', 'Tobit BA']},
		623713: {'abbrev': "TobS", 'syn': ['Tob', 'Tobit','Tob S', 'Tobit S']},
		623714: {'abbrev': "1Mac", 'syn': ['1 Macc', '1 Maccabees', '1 Macc', '1 Mac', '1 Maccab', 'I Macc', 'I Mac', 'I Maccab' ]},
		623715: {'abbrev': "2Mac", 'syn': ['2 Macc', '2 Maccabees', '2 Macc', '2 Mac', '2 Maccab', 'II Macc', 'II Mac', 'II Maccab']},
		623716: {'abbrev': "3Mac", 'syn': ['3 Macc', '3 Maccabees', '3 Macc', '3 Mac', '3 Maccab', 'III Macc', 'III Mac', 'III Maccab']},
		623717: {'abbrev': "4Mac", 'syn': ['4 Macc', '4 Maccabees', '4 Macc', '4 Mac', '4 Maccab', 'IV Macc', 'IV Mac', 'IV Maccab']},
		623718: {'abbrev': "Ps", 'syn': ['Ps(s)', 'Psalms', 'Psa']},
		623719: {'abbrev': "Od", 'syn': ['Odes', 'Odes of Solomon','OdesSol','OdSol']},
		623720: {'abbrev': "Prov", 'syn': ['Prov', 'Proverbs', 'Pr']},
		623721: {'abbrev': "Qoh", 'syn': ['Eccl', 'Ecclesiastes', 'Qoheleth', 'Qoh']},
		623722: {'abbrev': "Cant", 'syn': ['Song', 'Song of Songs', 'Song of Solomon', 'Canticles', 'Cant']},
		623723: {'abbrev': "Job", 'syn': ['Job', 'Jb']},
		623724: {'abbrev': "Wis", 'syn': ['Wis', 'Wisdom of Solomon', 'Wisdom', 'Wisd']},
		623725: {'abbrev': "Sir", 'syn': ['Sir', 'Sirach', 'Ecclesiasticus', 'Ben Sira']},
		623726: {'abbrev': "PsSol", 'syn': ['Psalms of Solomon', 'Ps Sol', 'PsaSol', 'Psa Sol']},
		623727: {'abbrev': "Hos", 'syn': ['Hos', 'Hosea']},
		623728: {'abbrev': "Mic", 'syn': ['Mic', 'Micah']},
		623729: {'abbrev': "Amos", 'syn': ['Amos', 'Amos']},
		623730: {'abbrev': "Joel", 'syn': ['Joel', 'Joel']},
		623731: {'abbrev': "Jonah", 'syn': ['Jonah', 'Jon', 'JonLXX', 'Jon LXX','JonahLXX', 'Jonah LXX']},
		623732: {'abbrev': "Obad", 'syn': ['Obad', 'Obadiah', 'Ob']},
		623733: {'abbrev': "Nah", 'syn': ['Nah', 'Nahum']},
		623734: {'abbrev': "Hab", 'syn': ['Hab', 'Habakkuk']},
		623735: {'abbrev': "Zeph", 'syn': ['Zeph', 'Zephaniah']},
		623736: {'abbrev': "Hag", 'syn': ['Hag', 'Haggai']},
		623737: {'abbrev': "Zech", 'syn': ['Zech', 'Zechariah']},
		623738: {'abbrev': "Mal", 'syn': ['Mal', 'Malachi']},
		623739: {'abbrev': "Isa", 'syn': ['Isa', 'Isaiah', 'Is']},
		623740: {'abbrev': "Jer", 'syn': ['Jer', 'Jeremiah']},
		623741: {'abbrev': "Bar", 'syn': ['Bar', 'Baruch']},
		623742: {'abbrev': "EpJer", 'syn': ['Ep Jer','Epistle of Jeremiah']},
		623743: {'abbrev': "Lam", 'syn': ['Lam', 'Lamentations']},
		623744: {'abbrev': "Ezek", 'syn': ['Ezek', 'Ezekiel']},
		623745: {'abbrev': "Bel", 'syn': ['Bel and the Dragon','BelDrag']},
		623746: {'abbrev': "BelTh", 'syn': ['Bel and the Dragon Th','BelDragTh']},
		623747: {'abbrev': "Dan", 'syn': ['Dan', 'Daniel','DanLXX', 'DanielLXX','Dan LXX', 'Daniel LXX','DanOG', 'DanielOG','Dan OG', 'Daniel OG']},
		623748: {'abbrev': "DanTh", 'syn': ['Dan', 'Daniel','DanTh', 'DanielTh','Dan Th', 'Daniel Th']},
		623749: {'abbrev': "Sus", 'syn': ['Susanna', 'SusOG', 'Sus OG', 'SusannaOG','Susanna OG']},
		623750: {'abbrev': "SusTh", 'syn': ['Susanna Th','SusannaTh']},
	}
	def getLemmaFeature(self):
		return self.api.F.lex_utf8
	
	def __init__(self):
		
		#mylog("TfLXX constructor()...")
		datasetPathname = "CenterBLC/LXX"
		version="1935"
		mylog(f"TfLXX.init('{datasetPathname}','{version}')...")
		super().__init__(datasetPathname, version=version)
		mylog("TfLXX() done calling super().init(). self.dataset =")
		mylog(self.dataset)

		self.posDict=TfLXX.posDict
	
		
		#theTfDataset = use(datasetPathname,version) #if version else use(datasetPathname)
		'''
		if (self.dataset):
			mylog("TfLxx.dataset= ")
			mylog(self.dataset)
			#self.dataset = theTfDataset
			mylog("Got self.dataset: ")
			mylog(self.dataset)
			self.theAPI = self.dataset.api
		else:
			mylog("TfDataset() got no data!")
			self.theAPI = None
		self.datasets=["yes", "no"]
		'''
		self.posDict=None
		self.posGroups=None
		self.bookDict=None
		self.dbname='lxx'
		