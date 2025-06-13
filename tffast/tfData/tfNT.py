import sys, os
from tf.app import use
#from tf.advanced import sections
from pathlib import Path
from .tfDataset import TfDataset
from ..env import mylog

class TfN1904(TfDataset):
	bookDict={
		137780 : {"name": "Matthew", "abbrev": "Matt" , "syn": ["Matthew", "Mt" ,"Mtt", "Mat", "Matt"] , "words": 18299 , "lemmas": 1670 , "chapters": 28 },
		137781 : {"name": "Mark", "abbrev": "Mark" , "syn": ["Mark","Mar","Mk","Mc"] , "words": 11277 , "lemmas": 1336 , "chapters": 16 },
		137782 : {"name": "Luke", "abbrev": "Luke" , "syn": ["Luke", "Lk","Luk","Lu"] , "words": 19456 , "lemmas": 2031 , "chapters": 24 },
		137783 : {"name": "John", "abbrev": "John" , "syn": ["John", "Jn", "Jo","Giov", "Iohn"] , "words": 15643 , "lemmas": 1023 , "chapters": 21 },
		137784 : {"name": "Acts", "abbrev": "Acts" , "syn": ["Acts", "Act", "Ac"] , "words": 18393 , "lemmas": 2017 , "chapters": 28 },
		137785 : {"name": "Romans", "abbrev": "Rom" , "syn": ["Romans", "Ro", "Rom"] , "words": 7100 , "lemmas": 1056 , "chapters": 16 },
		137786 : {"name": "1 Corinthians", "abbrev": "1 Cor" , "syn": ["1 Corinthians","I Cor","1 Cor", "I Corinthians","I Co","1 Co","I_Cor","1_Cor","I_Corinthians","1_Corinthians","I_Co","1_Co"] , "words": 6820 , "lemmas": 950 , "chapters": 16 },
		137787 : {"name": "2 Corinthians", "abbrev": "2 Cor" , "syn": ["2 Corinthians","II Cor","2 Cor", "II Corinthians","II Co","2 Co","II_Cor","2_Cor","II_Corinthinans","2_Corinthians","II_Co","2_Co"] , "words": 4469 , "lemmas": 784 , "chapters": 13 },
		137788 : {"name": "Galatians", "abbrev": "Gal" , "syn": ["Galatians", "Gal","Ga"] , "words": 2228 , "lemmas": 516 , "chapters": 6 },
		137789 : {"name": "Ephesians", "abbrev": "Eph" , "syn": ["Ephesians", "Eph","Ephe", "Ep"] , "words": 2419 , "lemmas": 527 , "chapters": 6 },
		137790 : {"name": "Philippians", "abbrev": "Phil" , "syn": ["Philippians", "Phil", "Ph", "Philip", "Phili"] , "words": 1630 , "lemmas": 443 , "chapters": 4 },
		137791 : {"name": "Col", "abbrev": "Col" , "syn": ["Colossians", "Col", "Co"] , "words": 1575 , "lemmas": 429 , "chapters": 4 },
		137792 : {"name": "1 Thessalonians", "abbrev": "1 Thess" , "syn": ["1 Thessalonians", "I Thess","1 Thess", "I Thes","1 Thes","I The","1 The","I_Thess","1_Thess","I_Thes","1_Thes","I_The","1_The","I_Thessalonians"] , "words": 1473 , "lemmas": 361 , "chapters": 5 },
		137793 : {"name": "2 Thessalonians", "abbrev": "2 Thess" , "syn": ["2 Thessalonians","II Thess","2 Thess", "II Thes","2 Thes","II The","2 The","II_Thess","2_Thess","II_Thes","2_Thes", "II_The","2_The","II_Thessalonians" ] , "words": 822 , "lemmas": 249 , "chapters": 3 },
		137794 : {"name": "1 Timothy", "abbrev": "1 Tim" , "syn": ["1 Timothy", "I Tim","1 Tim","I Ti","1 Ti","I_Tim","1_Tim","I_Tim","1_Tim","I_Ti","1_Ti","I_Timothy"] , "words": 1588 , "lemmas": 536 , "chapters": 6 },
		137795 : {"name": "2 Timothy", "abbrev": "2 Tim" , "syn": ["2 Timothy","II Tim","2 Tim","II Ti","2 Ti","II_Tim","2_Tim","II_Tim","2_Tim", "II_Ti","2_Ti" , "II_Timothy" ] , "words": 1237 , "lemmas": 453 , "chapters": 4 },
		137796 : {"name": "Titus", "abbrev": "Titus" , "syn": ["Titus", "Tit", "Ti"] , "words": 658 , "lemmas": 299 , "chapters": 3 },
		137797 : {"name": "Philemon", "abbrev": "Phlm" , "syn": ["Philemon", "Phlmn", "Phlm","Phln","Phmn"] , "words": 335 , "lemmas": 140 , "chapters": 1 },
		137798 : {"name": "Hebrews", "abbrev": "Heb" , "syn": ["Hebrews", "Heb", "He", "Hebr"] , "words": 4955 , "lemmas": 1025 , "chapters": 13 },
		137799 : {"name": "James", "abbrev": "Jas" , "syn": ["James", "Ja", "Jam", "Jame"] , "words": 1739 , "lemmas": 553 , "chapters": 5 },
		137800 : {"name": "1 Peter", "abbrev": "1 Pet" , "syn": ["1 Peter", "I Pet","1 Pet","I Pe","1 Pe","I_Pet","1_Pet","I_Pet","1_Pet","I_Pe","1_Pe", "I Peter"] , "words": 1676 , "lemmas": 542 , "chapters": 5 },
		137801 : {"name": "2 Peter", "abbrev": "2 Pet" , "syn": ["2 Peter","II Pet","2 Pet","II Pe","2 Pe","II_Pet","2_Pet","II_Pet","2_Pet", "II_Pe","2_Pe" , "II Peter"] , "words": 1098 , "lemmas": 396 , "chapters": 3 },
		137802 : {"name": "1 John", "abbrev": "1 John" , "syn": ["1 John", "1 Jn", "I Jn", "I John"] , "words": 2136 , "lemmas": 233 , "chapters": 5 },
		137803 : {"name": "2 John", "abbrev": "2 John" , "syn": ["2 John","2 Jn", "II Jn", "II John"] , "words": 245 , "lemmas": 95 , "chapters": 1 },
		137804 : {"name": "3 John", "abbrev": "3 John" , "syn": ["3 John","3 Jn", "III Jn", "III John"] , "words": 219 , "lemmas": 108 , "chapters": 1 },
		137805 : {"name": "Jude", "abbrev": "Jude" , "syn": ["Jude", "Jud"] , "words": 457 , "lemmas": 225 , "chapters": 1 },
		137806 : {"name": "Revelation", "abbrev": "Rev" , "syn": ["Revelation", "Rev","Apocalypse", "Apoc", "Ap", "Re","Apo"] , "words": 9832 , "lemmas": 910 , "chapters": 22 }
	}
	def getBooks(self):
		return TfN1904.bookDict
	def __init__(self):
		datasetPathname = "CenterBLC/N1904"
		self.bookDict = TfN1904.bookDict
		#version="1935"
		mylog(f"TfN1904.init('{datasetPathname}'...")
		super().__init__(datasetPathname,dbname='nt')
		
	def getLemmaFeature(self):
		return self.api.F.lemma