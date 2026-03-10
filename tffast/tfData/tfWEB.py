import sys, os, re
from tf.app import use
from .tfDataset import TfDataset
from ..env import mylog

class DummyApp:
    def __init__(self, api):
        self.api = api

class TfWEB(TfDataset):
    posDict = {
        
    }
    booksDict = {
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


    def __init__(self, dataset=None):
        db="web"
        # Since it's now on GitHub, we can let Text-Fabric resolve it automatically
        lemmaEnabled =False

        betaEnabled = False
        plainEnabled = False
        datasetPathname = "cbop-dev/tf-web-c"
            
        self.booksDict = TfWEB.booksDict
        dbname=db
        version="1.2"
        mylog(f"TfWEB.init('{datasetPathname}')...")
        
        super().__init__(datasetPathname, version=version, dbname=db, dataset=dataset,
        lemmaEnabled=lemmaEnabled,betaEnabled=betaEnabled,plainEnabled=plainEnabled)
        self.lang="english"

    def getLemmaFeature(self):
        # We don't have lemmas, just words, so return text feature
        return self.api.F.text

    def getLemma(self, wordid):
        # Fallback to the 'text' feature for lemma
        return self.api.T.text(wordid)

    def getBeta(self,wordid):
        return self.api.T.text(wordid)

    def getPlain(self,wordid):
        return self.api.T.text(wordid)
        
    def getGloss(self,wordid):
        return ''

    def isProperNoun(self,wordid):
        text = self.api.T.text(wordid)
        if text and len(text) > 0:
            return text[0].isupper()
        return False

    def getText(self, nodeId):
        text = super().getText(nodeId)
        if self.api.F.otype.v(nodeId) != 'word':
            
            text = re.sub(r'\s+([.,!?;:])', r'\1', text)
            # handle quotes which might have spaces around them.
            text = text.replace(" ' ", "'").replace(" \u2019 ", "\u2019").replace(" \u201d ", "\u201d")
        return text

    def normalize(self,string):
        return string

    def getPos(self,wordid):
        return ''

    
        
    def apparatusNote(self,book,chapter,verse):
        return ''
