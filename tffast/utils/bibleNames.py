import json
filename="tffast/utils/bibleBookNames.json"

bookNamesObject=json.load(open(filename))
standardizedBookNames=bookNamesObject["standardBookNamesDict"]

versification_name_map=bookNamesObject['versification_name_map']


lxxBooks ={
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

nt1904books={
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

vulgateBookNames={
        596441: {"name": "Matthew", "abbrev": "MAT", "syn": ['MAT', 'mat', 'Matthew', 'matthew'], "words": 16435, "chapters": 28, "lemmas": 1715, "morphs": 1},
        596442: {"name": "Mark", "abbrev": "MRK", "syn": ['MRK', 'mrk', 'Mark', 'mark'], "words": 10284, "chapters": 16, "lemmas": 1430, "morphs": 1},
        596443: {"name": "Luke", "abbrev": "LUK", "syn": ['LUK', 'luk', 'Luke', 'luke'], "words": 18004, "chapters": 24, "lemmas": 1960, "morphs": 1},
        596444: {"name": "John", "abbrev": "JHN", "syn": ['JHN', 'jhn', 'John', 'john'], "words": 14026, "chapters": 21, "lemmas": 1076, "morphs": 1},
        596445: {"name": "Acts", "abbrev": "ACT", "syn": ['ACT', 'act', 'Acts', 'acts'], "words": 16563, "chapters": 28, "lemmas": 1982, "morphs": 1},
        596446: {"name": "Romans", "abbrev": "ROM", "syn": ['ROM', 'rom', 'Romans', 'romans'], "words": 6509, "chapters": 16, "lemmas": 1072, "morphs": 1},
        596447: {"name": "1 Corinthians", "abbrev": "1CO", "syn": ['1CO', '1co', '1 Corinthians', '1_Corinthians', '1 Cor', '1Cor', 'I Cor', 'I Corinthians'], "words": 6386, "chapters": 16, "lemmas": 1011, "morphs": 1},
        596448: {"name": "2 Corinthians", "abbrev": "2CO", "syn": ['2CO', '2co', '2 Corinthians', '2_Corinthians', '2 Cor', '2Cor', 'II Cor', 'II Corinthians'], "words": 4272, "chapters": 13, "lemmas": 838, "morphs": 1},
        596449: {"name": "Galatians", "abbrev": "GAL", "syn": ['GAL', 'gal', 'Galatians', 'galatians'], "words": 2110, "chapters": 6, "lemmas": 545, "morphs": 1},
        596450: {"name": "Ephesians", "abbrev": "EPH", "syn": ['EPH', 'eph', 'Ephesians', 'ephesians'], "words": 2136, "chapters": 6, "lemmas": 570, "morphs": 1},
        596451: {"name": "Philippians", "abbrev": "PHP", "syn": ['PHP', 'php', 'Philippians', 'philippians'], "words": 1556, "chapters": 4, "lemmas": 448, "morphs": 1},
        596452: {"name": "Colossians", "abbrev": "COL", "syn": ['COL', 'col', 'Colossians', 'colossians'], "words": 1442, "chapters": 4, "lemmas": 454, "morphs": 1},
        596453: {"name": "1 Thessalonians", "abbrev": "1TH", "syn": ['1TH', '1th', '1 Thessalonians', '1_Thessalonians', '1 Thess', '1Thess', '1 Thes', '1Thes'], "words": 1392, "chapters": 5, "lemmas": 374, "morphs": 1},
        596454: {"name": "2 Thessalonians", "abbrev": "2TH", "syn": ['2TH', '2th', '2 Thessalonians', '2_Thessalonians', '2 Thess', '2Thess', '2 Thes', '2Thes'], "words": 743, "chapters": 3, "lemmas": 264, "morphs": 1},
        596455: {"name": "1 Timothy", "abbrev": "1TI", "syn": ['1TI', '1ti', '1 Timothy', '1_Timothy', '1 Tim', '1Tim'], "words": 1575, "chapters": 6, "lemmas": 573, "morphs": 1},
        596456: {"name": "2 Timothy", "abbrev": "2TI", "syn": ['2TI', '2ti', '2 Timothy', '2_Timothy', '2 Tim', '2Tim'], "words": 1154, "chapters": 4, "lemmas": 468, "morphs": 1},
        596457: {"name": "Titus", "abbrev": "TIT", "syn": ['TIT', 'tit', 'Titus', 'titus'], "words": 652, "chapters": 3, "lemmas": 304, "morphs": 1},
        596458: {"name": "Philemon", "abbrev": "PHM", "syn": ['PHM', 'phm', 'Philemon', 'philemon'], "words": 317, "chapters": 1, "lemmas": 153, "morphs": 1},
        596459: {"name": "Hebrews", "abbrev": "HEB", "syn": ['HEB', 'heb', 'Hebrews', 'hebrews'], "words": 4580, "chapters": 13, "lemmas": 1121, "morphs": 1},
        596460: {"name": "James", "abbrev": "JAS", "syn": ['JAS', 'jas', 'James', 'james'], "words": 1632, "chapters": 5, "lemmas": 577, "morphs": 1},
        596461: {"name": "1 Peter", "abbrev": "1PE", "syn": ['1PE', '1pe', '1 Peter', '1_Peter', '1 Pet', '1Pet'], "words": 1624, "chapters": 5, "lemmas": 569, "morphs": 1},
        596462: {"name": "2 Peter", "abbrev": "2PE", "syn": ['2PE', '2pe', '2 Peter', '2_Peter', '2 Pet', '2Pet'], "words": 1033, "chapters": 3, "lemmas": 439, "morphs": 1},
        596463: {"name": "1 John", "abbrev": "1JN", "syn": ['1JN', '1jn', '1 John', '1_John', '1 Jn', '1Jn'], "words": 1854, "chapters": 5, "lemmas": 255, "morphs": 1},
        596464: {"name": "2 John", "abbrev": "2JN", "syn": ['2JN', '2jn', '2 John', '2_John', '2 Jn', '2Jn'], "words": 218, "chapters": 1, "lemmas": 104, "morphs": 1},
        596465: {"name": "3 John", "abbrev": "3JN", "syn": ['3JN', '3jn', '3 John', '3_John', '3 Jn', '3Jn'], "words": 212, "chapters": 1, "lemmas": 115, "morphs": 1},
        596466: {"name": "Jude", "abbrev": "JUD", "syn": ['JUD', 'jud', 'Jude', 'jude'], "words": 420, "chapters": 1, "lemmas": 231, "morphs": 1},
        596467: {"name": "Revelation", "abbrev": "REV", "syn": ['REV', 'rev', 'Revelation', 'revelation'], "words": 8348, "chapters": 22, "lemmas": 1043, "morphs": 1},
        596468: {"name": "Genesis", "abbrev": "GEN", "syn": ['GEN', 'gen', 'Genesis', 'genesis'], "words": 25217, "chapters": 50, "lemmas": 2671, "morphs": 1},
        596469: {"name": "Exodus", "abbrev": "EXO", "syn": ['EXO', 'exo', 'Exodus', 'exodus'], "words": 20060, "chapters": 40, "lemmas": 2167, "morphs": 1},
        596470: {"name": "Leviticus", "abbrev": "LEV", "syn": ['LEV', 'lev', 'Leviticus', 'leviticus'], "words": 13775, "chapters": 27, "lemmas": 1587, "morphs": 1},
        596471: {"name": "Numbers", "abbrev": "NUM", "syn": ['NUM', 'num', 'Numbers', 'numbers'], "words": 19316, "chapters": 36, "lemmas": 2200, "morphs": 1},
        596472: {"name": "Deuteronomy", "abbrev": "DEU", "syn": ['DEU', 'deu', 'Deuteronomy', 'deuteronomy'], "words": 18502, "chapters": 34, "lemmas": 2055, "morphs": 1},
        596473: {"name": "Joshua", "abbrev": "JOS", "syn": ['JOS', 'jos', 'Joshua', 'joshua'], "words": 12154, "chapters": 24, "lemmas": 1758, "morphs": 1},
        596474: {"name": "Judges", "abbrev": "JDG", "syn": ['JDG', 'jdg', 'Judges', 'judges'], "words": 12625, "chapters": 21, "lemmas": 1849, "morphs": 1},
        596475: {"name": "Ruth", "abbrev": "RUT", "syn": ['RUT', 'rut', 'Ruth', 'ruth'], "words": 1784, "chapters": 4, "lemmas": 534, "morphs": 1},
        596476: {"name": "1 Samuel", "abbrev": "1SA", "syn": ['1SA', '1sa', '1 Samuel', '1_Samuel', '1 Sam', '1Sam'], "words": 18097, "chapters": 31, "lemmas": 1897, "morphs": 1},
        596477: {"name": "2 Samuel", "abbrev": "2SA", "syn": ['2SA', '2sa', '2 Samuel', '2_Samuel', '2 Sam', '2Sam'], "words": 14512, "chapters": 24, "lemmas": 1925, "morphs": 1},
        596478: {"name": "1 Kings", "abbrev": "1KI", "syn": ['1KI', '1ki', '1 Kings', '1_Kings', '1 Kgs', '1Kgs'], "words": 17225, "chapters": 22, "lemmas": 1928, "morphs": 1},
        596479: {"name": "2 Kings", "abbrev": "2KI", "syn": ['2KI', '2ki', '2 Kings', '2_Kings', '2 Kgs', '2Kgs'], "words": 15965, "chapters": 25, "lemmas": 1754, "morphs": 1},
        596480: {"name": "1 Chronicles", "abbrev": "1CH", "syn": ['1CH', '1ch', '1 Chronicles', '1_ChronICLES', '1 Chr', '1 Chron', '1Chr'], "words": 14343, "chapters": 29, "lemmas": 2535, "morphs": 1},
        596481: {"name": "2 Chronicles", "abbrev": "2CH", "syn": ['2CH', '2ch', '2 Chronicles', '2_ChronICLES', '2 Chr', '2 Chron', '2Chr'], "words": 17939, "chapters": 36, "lemmas": 2139, "morphs": 1},
        596482: {"name": "1 Esdras", "abbrev": "EZR", "syn": ['EZR', 'ezr', '1 Esdras', '1_Esdras', 'Ezra', 'ezra'], "words": 8027, "chapters": 9, "lemmas": 1528, "morphs": 1},
        596483: {"name": "Nehemiah", "abbrev": "NEH", "syn": ['NEH', 'neh', 'Nehemiah', 'nehemiah', '2 Esdras'], "words": 7352, "chapters": 13, "lemmas": 1414, "morphs": 1},
        596484: {"name": "Esther", "abbrev": "EST", "syn": ['EST', 'est', 'Esther', 'esther'], "words": 3990, "chapters": 10, "lemmas": 939, "morphs": 1},
        596485: {"name": "Judith", "abbrev": "JDT", "syn": ['JDT', 'jdt', 'Judith', 'judith'], "words": 6587, "chapters": 16, "lemmas": 1339, "morphs": 1},
        596486: {"name": "Tobit", "abbrev": "TOB", "syn": ['TOB', 'tob', 'Tobit', 'tobit'], "words": 4961, "chapters": 14, "lemmas": 1028, "morphs": 1},
        596487: {"name": "1 Maccabees", "abbrev": "1MA", "syn": ['1MA', '1ma', '1 Maccabees', '1_Maccabees', '1 Mac', '1Mac'], "words": 16334, "chapters": 16, "lemmas": 1815, "morphs": 1},
        596488: {"name": "2 Maccabees", "abbrev": "2MA", "syn": ['2MA', '2ma', '2 Maccabees', '2_Maccabees', '2 Mac', '2Mac'], "words": 10363, "chapters": 15, "lemmas": 2112, "morphs": 1},
        596489: {"name": "Psalms", "abbrev": "PSA", "syn": ['PSA', 'psa', 'Psalms', 'psalms', 'Psalmi'], "words": 30255, "chapters": 150, "lemmas": 2333, "morphs": 1},
        596490: {"name": "Prayer of Manasses", "abbrev": "MAN", "syn": ['MAN', 'man', 'Prayer of Manasses', 'prayer_of_manasses'], "words": 208, "chapters": 1, "lemmas": 112, "morphs": 1},
        596491: {"name": "Proverbs", "abbrev": "PRO", "syn": ['PRO', 'pro', 'Proverbs', 'proverbs'], "words": 9904, "chapters": 31, "lemmas": 1778, "morphs": 1},
        596492: {"name": "Ecclesiastes", "abbrev": "ECC", "syn": ['ECC', 'ecc', 'Ecclesiastes', 'ecclesiastes'], "words": 3795, "chapters": 12, "lemmas": 917, "morphs": 1},
        596493: {"name": "Job", "abbrev": "JOB", "syn": ['JOB', 'job', 'Job', 'job'], "words": 12532, "chapters": 42, "lemmas": 2045, "morphs": 1},
        596494: {"name": "Wisdom", "abbrev": "WIS", "syn": ['WIS', 'wis', 'Wisdom', 'wisdom'], "words": 7173, "chapters": 19, "lemmas": 1515, "morphs": 1},
        596495: {"name": "Ecclesiasticus", "abbrev": "SIR", "syn": ['SIR', 'sir', 'Ecclesiasticus', 'ecclesiasticus', 'Sirach', 'sirach'], "words": 20580, "chapters": 52, "lemmas": 2636, "morphs": 1},
        596496: {"name": "Psalmi Salomonis", "abbrev": "PSS", "syn": ['PSS', 'pss', 'Psalmi Salomonis', 'psalmi_salomonis'], "words": 1782, "chapters": 8, "lemmas": 583, "morphs": 1},
        596497: {"name": "Hosea", "abbrev": "HOS", "syn": ['HOS', 'hos', 'Hosea', 'hosea'], "words": 3497, "chapters": 14, "lemmas": 840, "morphs": 1},
        596498: {"name": "Amos", "abbrev": "AMO", "syn": ['AMO', 'amo', 'Amos', 'amos'], "words": 2794, "chapters": 9, "lemmas": 732, "morphs": 1},
        596499: {"name": "Micah", "abbrev": "MIC", "syn": ['MIC', 'mic', 'Micah', 'micah'], "words": 2069, "chapters": 7, "lemmas": 636, "morphs": 1},
        596500: {"name": "Joel", "abbrev": "JOL", "syn": ['JOL', 'jol', 'Joel', 'joel'], "words": 1356, "chapters": 3, "lemmas": 465, "morphs": 1},
        596501: {"name": "Obadiah", "abbrev": "OBA", "syn": ['OBA', 'oba', 'Obadiah', 'obadiah'], "words": 425, "chapters": 1, "lemmas": 191, "morphs": 1},
        596502: {"name": "Jonah", "abbrev": "JON", "syn": ['JON', 'jon', 'Jonah', 'jonah'], "words": 962, "chapters": 4, "lemmas": 294, "morphs": 1},
        596503: {"name": "Nahum", "abbrev": "NAM", "syn": ['NAM', 'nam', 'Nahum', 'nahum'], "words": 849, "chapters": 3, "lemmas": 398, "morphs": 1},
        596504: {"name": "Habakkuk", "abbrev": "HAB", "syn": ['HAB', 'hab', 'Habakkuk', 'habakkuk'], "words": 1008, "chapters": 3, "lemmas": 420, "morphs": 1},
        596505: {"name": "Zephaniah", "abbrev": "ZEP", "syn": ['ZEP', 'zep', 'Zephaniah', 'zephaniah'], "words": 1064, "chapters": 3, "lemmas": 388, "morphs": 1},
        596506: {"name": "Haggai", "abbrev": "HAG", "syn": ['HAG', 'hag', 'Haggai', 'haggai'], "words": 793, "chapters": 2, "lemmas": 241, "morphs": 1},
        596507: {"name": "Zechariah", "abbrev": "ZEC", "syn": ['ZEC', 'zec', 'Zechariah', 'zechariah'], "words": 4366, "chapters": 14, "lemmas": 824, "morphs": 1},
        596508: {"name": "Malachi", "abbrev": "MAL", "syn": ['MAL', 'mal', 'Malachi', 'malachi'], "words": 1220, "chapters": 4, "lemmas": 370, "morphs": 1},
        596509: {"name": "Isaiah", "abbrev": "ISA", "syn": ['ISA', 'isa', 'Isaiah', 'isaiah'], "words": 24572, "chapters": 66, "lemmas": 2706, "morphs": 1},
        596510: {"name": "Jeremiah", "abbrev": "JER", "syn": ['JER', 'jer', 'Jeremiah', 'jeremiah'], "words": 29503, "chapters": 52, "lemmas": 2408, "morphs": 1},
        596511: {"name": "Lamentations", "abbrev": "LAM", "syn": ['LAM', 'lam', 'Lamentations', 'lamentations'], "words": 2386, "chapters": 5, "lemmas": 725, "morphs": 1},
        596512: {"name": "Ezekiel", "abbrev": "EZK", "syn": ['EZK', 'ezk', 'Ezekiel', 'ezekiel'], "words": 26801, "chapters": 48, "lemmas": 2274, "morphs": 1},
        596513: {"name": "Daniel", "abbrev": "DAN", "syn": ['DAN', 'dan', 'Daniel', 'daniel'], "words": 1941, "chapters": 3, "lemmas": 503, "morphs": 1},
}

webcBookNames={
        877670: {"name": "GEN", "abbrev": "GEN", "syn": ["GEN", "gen", "Genesis", "genesis"], "words": 1, "chapters": 1, "lemmas": 0},
        877671: {"name": "EXO", "abbrev": "EXO", "syn": ["EXO", "exo", "Exodus", "exodus"], "words": 1, "chapters": 1, "lemmas": 0},
        877672: {"name": "LEV", "abbrev": "LEV", "syn": ["LEV", "lev", "Leviticus", "leviticus"], "words": 1, "chapters": 1, "lemmas": 0},
        877673: {"name": "NUM", "abbrev": "NUM", "syn": ["NUM", "num", "Numbers", "numbers"], "words": 1, "chapters": 1, "lemmas": 0},
        877674: {"name": "DEU", "abbrev": "DEU", "syn": ["DEU", "deu", "Deuteronomy", "deuteronomy"], "words": 1, "chapters": 1, "lemmas": 0},
        877675: {"name": "JOS", "abbrev": "JOS", "syn": ["JOS", "jos", "Joshua", "joshua"], "words": 1, "chapters": 1, "lemmas": 0},
        877676: {"name": "JDG", "abbrev": "JDG", "syn": ["JDG", "jdg", "Judges", "judges"], "words": 1, "chapters": 1, "lemmas": 0},
        877677: {"name": "RUT", "abbrev": "RUT", "syn": ["RUT", "rut", "Ruth", "ruth"], "words": 1, "chapters": 1, "lemmas": 0},
        877678: {"name": "1SA", "abbrev": "1SA", "syn": ["1SA", "1sa", "1 Sam", "1 Samuel", "1Sam", "1_Samuel"], "words": 1, "chapters": 1, "lemmas": 0},
        877679: {"name": "2SA", "abbrev": "2SA", "syn": ["2SA", "2sa", "2 Sam", "2 Samuel", "2Sam", "2_Samuel"], "words": 1, "chapters": 1, "lemmas": 0},
        877680: {"name": "1KI", "abbrev": "1KI", "syn": ["1KI", "1ki", "1 Kgs", "1 Kings", "1Kgs", "1_Kings"], "words": 1, "chapters": 1, "lemmas": 0},
        877681: {"name": "2KI", "abbrev": "2KI", "syn": ["2KI", "2ki", "2 Kgs", "2 Kings", "2Kgs", "2_Kings"], "words": 1, "chapters": 1, "lemmas": 0},
        877682: {"name": "1CH", "abbrev": "1CH", "syn": ["1CH", "1ch", "1 Chr", "1 Chronicles", "1Chr", "1 Chron", "1_Chronicles", "I_Chronicles"], "words": 1, "chapters": 1, "lemmas": 0},
        877683: {"name": "2CH", "abbrev": "2CH", "syn": ["2CH", "2ch", "2 Chr", "2 Chronicles", "2Chr", "2 Chron", "2_Chronicles", "II_Chronicles"], "words": 1, "chapters": 1, "lemmas": 0},
        877684: {"name": "EZR", "abbrev": "EZR", "syn": ["EZR", "ezr", "1 Esdras", "1_Esdras", "Ezra", "ezra"], "words": 1, "chapters": 1, "lemmas": 0},
        877685: {"name": "NEH", "abbrev": "NEH", "syn": ["NEH", "neh", "Nehemiah", "nehemiah", "2 Esdras"], "words": 1, "chapters": 1, "lemmas": 0},
        877686: {"name": "JOB", "abbrev": "JOB", "syn": ["JOB", "job", "Job"], "words": 1, "chapters": 1, "lemmas": 0},
        877687: {"name": "PSA", "abbrev": "PSA", "syn": ["PSA", "psa", "Psalms", "psalms", "Psalmi"], "words": 1, "chapters": 1, "lemmas": 0},
        877688: {"name": "PRO", "abbrev": "PRO", "syn": ["PRO", "pro", "Proverbs", "proverbs"], "words": 1, "chapters": 1, "lemmas": 0},
        877689: {"name": "ECC", "abbrev": "ECC", "syn": ["ECC", "ecc", "Ecclesiastes", "ecclesiastes"], "words": 1, "chapters": 1, "lemmas": 0},
        877690: {"name": "SNG", "abbrev": "SNG", "syn": ["SNG", "sng"], "words": 1, "chapters": 1, "lemmas": 0},
        877691: {"name": "ISA", "abbrev": "ISA", "syn": ["ISA", "isa", "Isaiah", "isaiah"], "words": 1, "chapters": 1, "lemmas": 0},
        877692: {"name": "JER", "abbrev": "JER", "syn": ["JER", "jer", "Jeremiah", "jeremiah"], "words": 1, "chapters": 1, "lemmas": 0},
        877693: {"name": "LAM", "abbrev": "LAM", "syn": ["LAM", "lam", "Lamentations", "lamentations"], "words": 1, "chapters": 1, "lemmas": 0},
        877694: {"name": "EZK", "abbrev": "EZK", "syn": ["EZK", "ezk", "Ezekiel", "ezekiel"], "words": 1, "chapters": 1, "lemmas": 0},
        877695: {"name": "HOS", "abbrev": "HOS", "syn": ["HOS", "hos", "Hosea", "hosea"], "words": 1, "chapters": 1, "lemmas": 0},
        877696: {"name": "JOL", "abbrev": "JOL", "syn": ["JOL", "jol", "Joel", "joel"], "words": 1, "chapters": 1, "lemmas": 0},
        877697: {"name": "AMO", "abbrev": "AMO", "syn": ["AMO", "amo", "Amos", "amos"], "words": 1, "chapters": 1, "lemmas": 0},
        877698: {"name": "OBA", "abbrev": "OBA", "syn": ["OBA", "oba", "Obadiah", "obadiah"], "words": 1, "chapters": 1, "lemmas": 0},
        877699: {"name": "JON", "abbrev": "JON", "syn": ["JON", "jon", "Jonah", "jonah"], "words": 1, "chapters": 1, "lemmas": 0},
        877700: {"name": "MIC", "abbrev": "MIC", "syn": ["MIC", "mic", "Micah", "micah"], "words": 1, "chapters": 1, "lemmas": 0},
        877701: {"name": "NAM", "abbrev": "NAM", "syn": ["NAM", "nam", "Nahum", "nahum"], "words": 1, "chapters": 1, "lemmas": 0},
        877702: {"name": "HAB", "abbrev": "HAB", "syn": ["HAB", "hab", "Habakkuk", "habakkuk"], "words": 1, "chapters": 1, "lemmas": 0},
        877703: {"name": "ZEP", "abbrev": "ZEP", "syn": ["ZEP", "zep", "Zephaniah", "zephaniah"], "words": 1, "chapters": 1, "lemmas": 0},
        877704: {"name": "HAG", "abbrev": "HAG", "syn": ["HAG", "hag", "Haggai", "haggai"], "words": 1, "chapters": 1, "lemmas": 0},
        877705: {"name": "ZEC", "abbrev": "ZEC", "syn": ["ZEC", "zec", "Zechariah", "zechariah"], "words": 1, "chapters": 1, "lemmas": 0},
        877706: {"name": "MAL", "abbrev": "MAL", "syn": ["MAL", "mal", "Malachi", "malachi"], "words": 1, "chapters": 1, "lemmas": 0},
        877707: {"name": "TOB", "abbrev": "TOB", "syn": ["TOB", "tob", "Tobit", "tobit"], "words": 1, "chapters": 1, "lemmas": 0},
        877708: {"name": "JDT", "abbrev": "JDT", "syn": ["JDT", "jdt", "Judith", "judith"], "words": 1, "chapters": 1, "lemmas": 0},
        877709: {"name": "ESG", "abbrev": "ESG", "syn": ["ESG", "esg"], "words": 1, "chapters": 1, "lemmas": 0},
        877710: {"name": "WIS", "abbrev": "WIS", "syn": ["WIS", "wis", "Wisdom", "wisdom"], "words": 1, "chapters": 1, "lemmas": 0},
        877711: {"name": "SIR", "abbrev": "SIR", "syn": ["SIR", "sir", "Ecclesiasticus", "ecclesiasticus", "Sirach", "sirach"], "words": 1, "chapters": 1, "lemmas": 0},
        877712: {"name": "BAR", "abbrev": "BAR", "syn": ["BAR", "bar"], "words": 1, "chapters": 1, "lemmas": 0},
        877713: {"name": "1MA", "abbrev": "1MA", "syn": ["1MA", "1ma", "1 Maccabees", "1_Maccabees", "1 Mac", "1Mac"], "words": 1, "chapters": 1, "lemmas": 0},
        877714: {"name": "2MA", "abbrev": "2MA", "syn": ["2MA", "2ma", "2 Maccabees", "2_Maccabees", "2 Mac", "2Mac"], "words": 1, "chapters": 1, "lemmas": 0},
        877715: {"name": "DAG", "abbrev": "DAG", "syn": ["DAG", "dag"], "words": 1, "chapters": 1, "lemmas": 0},
        877716: {"name": "Matthew", "abbrev": "Matthew", "syn": ["Matthew", "matthew", "MAT", "mat"], "words": 1, "chapters": 1, "lemmas": 0},
        877717: {"name": "Mark", "abbrev": "Mark", "syn": ["Mark", "mark", "MRK", "mrk"], "words": 1, "chapters": 1, "lemmas": 0},
        877718: {"name": "Luke", "abbrev": "Luke", "syn": ["Luke", "luke", "LUK", "luk"], "words": 1, "chapters": 1, "lemmas": 0},
        877719: {"name": "John", "abbrev": "John", "syn": ["John", "john", "JHN", "jhn"], "words": 1, "chapters": 1, "lemmas": 0},
        877720: {"name": "Acts", "abbrev": "Acts", "syn": ["Acts", "acts", "ACT", "act"], "words": 1, "chapters": 1, "lemmas": 0},
        877721: {"name": "Romans", "abbrev": "Romans", "syn": ["Romans", "romans", "ROM", "rom"], "words": 1, "chapters": 1, "lemmas": 0},
        877722: {"name": "1_Corinthians", "abbrev": "1_Corinthians", "syn": ["1_Corinthians", "1_corinthians", "1 Corinthians", "1 Cor", "1Cor", "I Cor", "I Corinthians", "1CO", "1co"], "words": 1, "chapters": 1, "lemmas": 0},
        877723: {"name": "2_Corinthians", "abbrev": "2_Corinthians", "syn": ["2_Corinthians", "2_corinthians", "2 Corinthians", "2 Cor", "2Cor", "II Cor", "II Corinthians", "2CO", "2co"], "words": 1, "chapters": 1, "lemmas": 0},
        877724: {"name": "Galatians", "abbrev": "Galatians", "syn": ["Galatians", "galatians", "GAL", "gal"], "words": 1, "chapters": 1, "lemmas": 0},
        877725: {"name": "Ephesians", "abbrev": "Ephesians", "syn": ["Ephesians", "ephesians", "EPH", "eph"], "words": 1, "chapters": 1, "lemmas": 0},
        877726: {"name": "Philippians", "abbrev": "Philippians", "syn": ["Philippians", "philippians", "PHP", "php"], "words": 1, "chapters": 1, "lemmas": 0},
        877727: {"name": "Colossians", "abbrev": "Colossians", "syn": ["Colossians", "colossians", "COL", "col"], "words": 1, "chapters": 1, "lemmas": 0},
        877728: {"name": "1_Thessalonians", "abbrev": "1_Thessalonians", "syn": ["1_Thessalonians", "1_thessalonians", "1 Thessalonians", "1 Thess", "1Thess", "1 Thes", "1Thes", "1TH", "1th"], "words": 1, "chapters": 1, "lemmas": 0},
        877729: {"name": "2_Thessalonians", "abbrev": "2_Thessalonians", "syn": ["2_Thessalonians", "2_thessalonians", "2 Thessalonians", "2 Thess", "2Thess", "2 Thes", "2Thes", "2TH", "2th"], "words": 1, "chapters": 1, "lemmas": 0},
        877730: {"name": "1_Timothy", "abbrev": "1_Timothy", "syn": ["1_Timothy", "1_timothy", "1 Timothy", "1 Tim", "1Tim", "1TI", "1ti"], "words": 1, "chapters": 1, "lemmas": 0},
        877731: {"name": "2_Timothy", "abbrev": "2_Timothy", "syn": ["2_Timothy", "2_timothy", "2 Timothy", "2 Tim", "2Tim", "2TI", "2ti"], "words": 1, "chapters": 1, "lemmas": 0},
        877732: {"name": "Titus", "abbrev": "Titus", "syn": ["Titus", "titus", "TIT", "tit"], "words": 1, "chapters": 1, "lemmas": 0},
        877733: {"name": "Philemon", "abbrev": "Philemon", "syn": ["Philemon", "philemon", "PHM", "phm"], "words": 1, "chapters": 1, "lemmas": 0},
        877734: {"name": "Hebrews", "abbrev": "Hebrews", "syn": ["Hebrews", "hebrews", "HEB", "heb"], "words": 1, "chapters": 1, "lemmas": 0},
        877735: {"name": "James", "abbrev": "James", "syn": ["James", "james", "JAS", "jas"], "words": 1, "chapters": 1, "lemmas": 0},
        877736: {"name": "1_Peter", "abbrev": "1_Peter", "syn": ["1_Peter", "1_peter", "1 Peter", "1 Pet", "1Pet", "1PE", "1pe"], "words": 1, "chapters": 1, "lemmas": 0},
        877737: {"name": "2_Peter", "abbrev": "2_Peter", "syn": ["2_Peter", "2_peter", "2 Peter", "2 Pet", "2Pet", "2PE", "2pe"], "words": 1, "chapters": 1, "lemmas": 0},
        877738: {"name": "1_John", "abbrev": "1_John", "syn": ["1_John", "1_john", "1 John", "1 Jn", "1Jn", "1JN", "1jn"], "words": 1, "chapters": 1, "lemmas": 0},
        877739: {"name": "2_John", "abbrev": "2_John", "syn": ["2_John", "2_john", "2 John", "2 Jn", "2Jn", "2JN", "2jn"], "words": 1, "chapters": 1, "lemmas": 0},
        877740: {"name": "3_John", "abbrev": "3_John", "syn": ["3_John", "3_john", "3 John", "3 Jn", "3Jn", "3JN", "3jn"], "words": 1, "chapters": 1, "lemmas": 0},
        877741: {"name": "Jude", "abbrev": "Jude", "syn": ["Jude", "jude", "JUD", "jud"], "words": 1, "chapters": 1, "lemmas": 0},
        877742: {"name": "Revelation", "abbrev": "Revelation", "syn": ["Revelation", "revelation", "REV", "rev"], "words": 1, "chapters": 1, "lemmas": 0},
}

bibleBookMappingNames = bookNamesObject['bibleBookMappingNames']
"""
bhsMap={'GEN': 'Gen', 'EXO': 'Exod', 'LEV': 'Lev', 'NUM': 'Num', 'DEU': 'Deut', 'JOS': 'Josh', 'JDG': 'Judg', '1SA': 'Isa', '2SA': '2Sam', '1KI': '1Kgs', '2KI': '2Kgs', 'JER': 'Jer', 'EZK': 'Ezek', 'HOS': 'Hos', 'JOL': 'Joel', 'AMO': 'Amos', 'OBA': 'Obad', 'JON': 'Jonah', 'MIC': 'Mic', 'NAM': 'Nah', 'HAB': 'Hab', 'ZEP': 'Zeph', 'HAG': 'Hag', 'ZEC': 'Zech', 'MAL': 'Mal', 'PSA': 'Ps', 'JOB': 'Job', 'PRO': 'Prov', 'RUT': 'Ruth', 'SNG': 'Cant', 'ECC': 'Qoh', 'LAM': 'Lam', 'EST': 'Esth', 'DAN': 'Dan', 'EZR': 'Ezra', 'NEH': 'Neh', '1CH': '1Chr', '2CH': '2Chr'}
lxxMap={'GEN': 'Gen', 'EXO': 'Exod', 'LEV': 'Lev', 'NUM': 'Num', 'DEU': 'Deut', 'JOS': 'Josh', 'JDG': 'Judg', 'RUT': 'Ruth', '1SA': 'Isa', '2SA': '2Sam', '1KI': '1Kgs', '2KI': '2Kgs', '1CH': '1Chr', '2CH': '2Chr', '1ES': '1Esdr', '2ES': '2Esdr', 'EST': 'Esth', 'JDT': 'Jdt', 'TOB': 'TobBA', 'TBS': 'TobS', '1MA': '1Mac', '2MA': '2Mac', '3MA': '3Mac', '4MA': '4Mac', 'PSA': 'Ps', 'ODA': 'Od', 'PRO': 'Prov', 'ECC': 'Qoh', 'SNG': 'Cant', 'JOB': 'Job', 'WIS': 'Wis', 'SIR': 'Sir', 'PSS': 'PsSol', 'HOS': 'Hos', 'MIC': 'Mic', 'AMO': 'Amos', 'JOL': 'Joel', 'JON': 'Jonah', 'OBA': 'Obad', 'NAM': 'Nah', 'HAB': 'Hab', 'ZEP': 'Zeph', 'HAG': 'Hag', 'ZEC': 'Zech', 'MAL': 'Mal', 'JER': 'Jer', 'BAR': 'Bar', 'LJE': 'EpJer', 'LAM': 'Lam', 'EZK': 'Ezek', 'BEL': 'Bel', 'BLT': 'BelTh', 'DAN': 'DanTh', 'SUS': 'Sus', 'SST': 'SusTh'}
n1904Map={'MAT': 'Matt', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John', 'ACT': 'Acts', 'ROM': 'Rom', '1CO': '1 Cor', '2CO': '2 Cor', 'GAL': 'Gal', 'EPH': 'Eph', 'PHP': 'Phil', 'COL': 'Col', '1TH': '1 Thess', '2TH': '2 Thess', '1TI': '1 Tim', '2TI': '2 Tim', 'TIT': 'Titus', 'PHM': 'Phlm', 'HEB': 'Heb', 'JAS': 'Jas', '1PE': '1 Pet', '2PE': '2 Pet', '1JN': '1 John', '2JN': '2 John', '3JN': '3 John', 'JUD': 'Jude', 'REV': 'Rev'}
vulMap={'MAT': 'MAT', 'MRK': 'MRK', 'LUK': 'LUK', 'JHN': 'JHN', 'ACT': 'ACT', 'ROM': 'ROM', '1CO': '1CO', '2CO': '2CO', 'GAL': 'GAL', 'EPH': 'EPH', 'PHP': 'PHP', 'COL': 'COL', '1TH': '1TH', '2TH': '2TH', '1TI': '1TI', '2TI': '2TI', 'TIT': 'TIT', 'PHM': 'PHM', 'HEB': 'HEB', 'JAS': 'JAS', '1PE': '1PE', '2PE': '2PE', '1JN': '1JN', '2JN': '2JN', '3JN': '3JN', 'JUD': 'JUD', 'REV': 'REV', 'GEN': 'GEN', 'EXO': 'EXO', 'LEV': 'LEV', 'NUM': 'NUM', 'DEU': 'DEU', 'JOS': 'JOS', 'JDG': 'JDG', 'RUT': 'RUT', '1SA': 'ISA', '2SA': '2SA', '1KI': '1KI', '2KI': '2KI', '1CH': '1CH', '2CH': '2CH', 'EZR': 'EZR', 'NEH': 'NEH', 'EST': 'EST', 'JDT': 'JDT', 'TOB': 'TOB', '1MA': '1MA', '2MA': '2MA', 'PSA': 'PSA', 'MAN': 'MAN', 'PRO': 'PRO', 'ECC': 'ECC', 'JOB': 'JOB', 'WIS': 'WIS', 'SIR': 'SIR', 'PSS': 'PSS', 'HOS': 'HOS', 'AMO': 'AMO', 'MIC': 'MIC', 'JOL': 'JOL', 'OBA': 'OBA', 'JON': 'JON', 'NAM': 'NAM', 'HAB': 'HAB', 'ZEP': 'ZEP', 'HAG': 'HAG', 'ZEC': 'ZEC', 'MAL': 'MAL', 'JER': 'JER', 'LAM': 'LAM', 'EZK': 'EZK', 'DAN': 'DAN'}
webMap={'GEN': 'GEN', 'EXO': 'EXO', 'LEV': 'LEV', 'NUM': 'NUM', 'DEU': 'DEU', 'JOS': 'JOS', 'JDG': 'JDG', 'RUT': 'RUT', '1SA': 'ISA', '2SA': '2SA', '1KI': '1KI', '2KI': '2KI', '1CH': '1CH', '2CH': '2CH', 'EZR': 'EZR', 'NEH': 'NEH', 'JOB': 'JOB', 'PSA': 'PSA', 'PRO': 'PRO', 'ECC': 'ECC', 'SNG': 'SNG', 'JER': 'JER', 'LAM': 'LAM', 'EZK': 'EZK', 'HOS': 'HOS', 'JOL': 'JOL', 'AMO': 'AMO', 'OBA': 'OBA', 'JON': 'JON', 'MIC': 'MIC', 'NAM': 'NAM', 'HAB': 'HAB', 'ZEP': 'ZEP', 'HAG': 'HAG', 'ZEC': 'ZEC', 'MAL': 'MAL', 'TOB': 'TOB', 'JDT': 'JDT', 'ESG': 'ESG', 'WIS': 'WIS', 'SIR': 'SIR', 'BAR': 'BAR', '1MA': '1MA', '2MA': '2MA', None: 'DAG', 'MAT': 'Matthew', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John', 'ACT': 'Acts', 'ROM': 'Romans', '1CO': '1_Corinthians', '2CO': '2_Corinthians', 'GAL': 'Galatians', 'EPH': 'Ephesians', 'PHP': 'Philippians', 'COL': 'Colossians', '1TH': '1_Thessalonians', '2TH': '2_Thessalonians', '1TI': '1_Timothy', '2TI': '2_Timothy', 'TIT': 'Titus', 'PHM': 'Philemon', 'HEB': 'Hebrews', 'JAS': 'James', '1PE': '1_Peter', '2PE': '2_Peter', '1JN': '1_John', '2JN': '2_John', '3JN': '3_John', 'JUD': 'Jude', 'REV': 'Revelation'}
sblMap={'MAT': 'Matt', 'MRK': 'Mark', 'LUK': 'Luke', 'JHN': 'John', 'ACT': 'Acts', 'ROM': 'Rom', '1CO': '1 Cor', '2CO': '2 Cor', 'GAL': 'Gal', 'EPH': 'Eph', 'PHP': 'Phil', 'COL': 'Col', '1TH': '1 Thess', '2TH': '2 Thess', '1TI': '1 Tim', '2TI': '2 Tim', 'TIT': 'Titus', 'PHM': 'Phlm', 'HEB': 'Heb', 'JAS': 'Jas', '1PE': '1 Pet', '2PE': '2 Pet', '1JN': '1 John', '2JN': '2 John', '3JN': '3 John', 'JUD': 'Jude', 'REV': 'Rev'}
"""


versionMaps=bookNamesObject["versions"]

"""
{
  'bhs':bhsMap,
  'lxx':lxxMap,
  'nt':n1904Map,
  'web':webMap,
  'sblgnt':sblMap,
  'vulgate':vulMap
}
"""


def getBookMapAbbrev(name):
    for abbrev, names in bibleBookMappingNames.items():
        names=[n.lower() for n in names]
        if name.lower() in names:
            return abbrev
    return None

def getTfBookAbbrev(verseMapAbbrev,version):
  """
  getTfBookAbbrev: a reverse function to getBookMapAbbrev. Returns the bookname abbreviation used the given tf fabric dataset.
  verseMapAbbrev: the mapping abbreviation used in the verse_map module/function. (i.e., the value returned by getBookMapAbbrev)
  version: the version of the tf fabric dataset: e.g., one of: 'bhs', 'lxx', 'nt', 'web', 'sblgnt', 'vulgate'
  """

  ret = None
  if version in versionMaps:
      
      if verseMapAbbrev in versionMaps[version]:
        ret = versionMaps[version][verseMapAbbrev]
  return ret

def getStandarizedBookName(synonym):
  """
    Returns a book name for the book with the given synonymn or abbreviation. NB: this is a one way function, in that it will return a common value for some variations on the same book, e.g., "EstherG" and "Esther" both return "Esther" and likewise for versions of Daniel, etc.
    synonym: the synonym for the book name. 
    returns a string, the "standardized" book name if found, or an empty string if none found
  """
  ret = ''
  synonym = synonym.strip()
  for name, syns in standardizedBookNames.items():
    if synonym in syns:
      ret = name
      break
    elif synonym.lower() in map(lambda s: s.lower(), syns):
      ret = name
      break
  
  if (ret == ''):
    pass
    #print(f"Could not find synonym {synonym}")
  
  return ret
