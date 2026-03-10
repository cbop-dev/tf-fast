import re
from tf.app import use
from .tfDataset import TfDataset,POS
from ..env import mylog
from enum import Enum
class TfVulgate(TfDataset):
    posDict={
        "ADJadv.mul":[POS.ADJECTIVE.value],
        "ADJadv.ord":[POS.ADJECTIVE.value],
        "ADJcar":[POS.ADJECTIVE.value],
        "ADJdis":[POS.ADJECTIVE.value],
        "ADJmul":[POS.ADJECTIVE.value],
        "ADJord":[POS.ADJECTIVE.value],
        "ADJqua":[POS.ADJECTIVE.value],
        "ADV":[POS.ADVERB.value],
        "ADVint":[POS.ADVERB.value],
        "ADVint.neg":[POS.ADVERB.value],
        "ADVneg":[POS.ADVERB.value],
        "ADVrel":[POS.ADVERB.value],
        "CONcoo":[POS.CONJUNCTION.value],
        "CONsub":[POS.CONJUNCTION.value],
        "INJ":[POS.INTERJECTION.value],
        "NOMcom":[POS.NOUN.value],
        "NOMpro":[POS.NOUN.value],
        "PRE":[POS.PREPOSITION.value],
        "PROdem":[POS.PRONOUN.value],
        "PROind":[POS.PRONOUN.value],
        "PROint":[POS.PRONOUN.value],
        "PROper":[POS.PRONOUN.value],
        "PROpos":[POS.PRONOUN.value],
        "PROpos.ref":[POS.PRONOUN.value],
        "PROref":[POS.PRONOUN.value],
        "PROrel":[POS.PRONOUN.value],
        "VER":[POS.VERB.value]
    }
    booksDict = {
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

    def __init__(self, dataset=None):
        import os
        db="vulgate"
        self.lemmaEnabled = True
        self.betaEnabled = False
        self.plainEnabled = False
        # We assume the user/deployment has copied the text-fabric binary data to the expected folder
        # e.g., ~/text-fabric-data/github/cbop-dev/tf-vulgate/tf/1.0
        # Text-Fabric crashes if we use 'cbop-dev/tf-vulgate' without a github repo existing. 
        # Using 'data:' bypasses the github check. TF will automatically append version '1.0' to this path.
        # Note: TF 13.0 strips the first slash. So we use a double slash `//` and expand `~` explicitly.
        #base_path = os.path.expanduser('~')
        #datasetPathname = f"data:/{base_path}/text-fabric-data/github/cbop-dev/tf-vulgate/tf"
        datasetPathname="cbop-dev/tf-vulgate"
        self.booksDict = TfVulgate.booksDict
        self.dbname=db
        version="0.1"
        mylog(f"TfVulgate.init('{datasetPathname}')...")
        
        super().__init__(datasetPathname, version=version, dbname=db, dataset=dataset)
        self.lang="latin"
    



    def getBeta(self,wordid):
        return self.api.T.text(wordid).strip()

    def getPlain(self,wordid):
        return self.api.T.text(wordid).strip()
        
    def getGloss(self,wordid):
        return ''

    def isProperNoun(self,wordid):
        # In Vulgate, POS for proper noun might be encoded in msd or pos.
        # Check if the word is capitalized as a fallback.
        text = self.api.T.text(wordid)
        if text and len(text) > 0:
            return text[0].isupper()
        return False

    def getText(self, nodeId):
        text = super().getText(nodeId)
        if self.api.F.otype.v(nodeId) != 'word':
            # Clean up spacing around punctuation since the TF builder separated punc
            text = text.replace(" ,", ",").replace(" .", ".").replace(" :", ":").replace(" ;", ";").replace(" ?", "?").replace(" !", "!")
        return text

        
    def apparatusNote(self,book,chapter,verse):
        return ''
    def getLemma(self,wordid):
        lemma = super().getLemma(wordid)
        filtered = re.sub(r'[\]0-9!%*,.:;=?$]','',lemma)
        return lemma if filtered else ''

    def getPos(self,wordid):
        return self.api.F.pos.v(wordid)

    
    
