import re
from tf.app import use
from .tfDataset import TfDataset
from ..env import mylog

class TfVulgate(TfDataset):
    
    booksDict = {
        597910: {"name": "Matthew", "abbrev": "MAT", "syn": ['MAT', 'mat', 'Matthew', 'matthew'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597911: {"name": "Mark", "abbrev": "MRK", "syn": ['MRK', 'mrk', 'Mark', 'mark'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597912: {"name": "Luke", "abbrev": "LUK", "syn": ['LUK', 'luk', 'Luke', 'luke'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597913: {"name": "John", "abbrev": "JHN", "syn": ['JHN', 'jhn', 'John', 'john'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597914: {"name": "Acts", "abbrev": "ACT", "syn": ['ACT', 'act', 'Acts', 'acts'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597915: {"name": "Romans", "abbrev": "ROM", "syn": ['ROM', 'rom', 'Romans', 'romans'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597916: {"name": "1 Corinthians", "abbrev": "1CO", "syn": ['1CO', '1co', '1 Corinthians', '1_Corinthians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597917: {"name": "2 Corinthians", "abbrev": "2CO", "syn": ['2CO', '2co', '2 Corinthians', '2_Corinthians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597918: {"name": "Galatians", "abbrev": "GAL", "syn": ['GAL', 'gal', 'Galatians', 'galatians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597919: {"name": "Ephesians", "abbrev": "EPH", "syn": ['EPH', 'eph', 'Ephesians', 'ephesians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597920: {"name": "Philippians", "abbrev": "PHP", "syn": ['PHP', 'php', 'Philippians', 'philippians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597921: {"name": "Colossians", "abbrev": "COL", "syn": ['COL', 'col', 'Colossians', 'colossians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597922: {"name": "1 Thessalonians", "abbrev": "1TH", "syn": ['1TH', '1th', '1 Thessalonians', '1_Thessalonians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597923: {"name": "2 Thessalonians", "abbrev": "2TH", "syn": ['2TH', '2th', '2 Thessalonians', '2_Thessalonians'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597924: {"name": "1 Timothy", "abbrev": "1TI", "syn": ['1TI', '1ti', '1 Timothy', '1_Timothy'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597925: {"name": "2 Timothy", "abbrev": "2TI", "syn": ['2TI', '2ti', '2 Timothy', '2_Timothy'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597926: {"name": "Titus", "abbrev": "TIT", "syn": ['TIT', 'tit', 'Titus', 'titus'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597927: {"name": "Philemon", "abbrev": "PHM", "syn": ['PHM', 'phm', 'Philemon', 'philemon'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597928: {"name": "Hebrews", "abbrev": "HEB", "syn": ['HEB', 'heb', 'Hebrews', 'hebrews'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597929: {"name": "James", "abbrev": "JAS", "syn": ['JAS', 'jas', 'James', 'james'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597930: {"name": "1 Peter", "abbrev": "1PE", "syn": ['1PE', '1pe', '1 Peter', '1_Peter'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597931: {"name": "2 Peter", "abbrev": "2PE", "syn": ['2PE', '2pe', '2 Peter', '2_Peter'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597932: {"name": "1 John", "abbrev": "1JN", "syn": ['1JN', '1jn', '1 John', '1_John'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597933: {"name": "2 John", "abbrev": "2JN", "syn": ['2JN', '2jn', '2 John', '2_John'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597934: {"name": "3 John", "abbrev": "3JN", "syn": ['3JN', '3jn', '3 John', '3_John'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597935: {"name": "Jude", "abbrev": "JUD", "syn": ['JUD', 'jud', 'Jude', 'jude'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597936: {"name": "Revelation", "abbrev": "REV", "syn": ['REV', 'rev', 'Revelation', 'revelation'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597937: {"name": "Genesis", "abbrev": "GEN", "syn": ['GEN', 'gen', 'Genesis', 'genesis'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597938: {"name": "Exodus", "abbrev": "EXO", "syn": ['EXO', 'exo', 'Exodus', 'exodus'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597939: {"name": "Leviticus", "abbrev": "LEV", "syn": ['LEV', 'lev', 'Leviticus', 'leviticus'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597940: {"name": "Numbers", "abbrev": "NUM", "syn": ['NUM', 'num', 'Numbers', 'numbers'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597941: {"name": "Deuteronomy", "abbrev": "DEU", "syn": ['DEU', 'deu', 'Deuteronomy', 'deuteronomy'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597942: {"name": "Joshua", "abbrev": "JOS", "syn": ['JOS', 'jos', 'Joshua', 'joshua'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597943: {"name": "Judges", "abbrev": "JDG", "syn": ['JDG', 'jdg', 'Judges', 'judges'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597944: {"name": "Ruth", "abbrev": "RUT", "syn": ['RUT', 'rut', 'Ruth', 'ruth'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597945: {"name": "1 Samuel", "abbrev": "1SA", "syn": ['1SA', '1sa', '1 Samuel', '1_Samuel'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597946: {"name": "2 Samuel", "abbrev": "2SA", "syn": ['2SA', '2sa', '2 Samuel', '2_Samuel'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597947: {"name": "1 Kings", "abbrev": "1KI", "syn": ['1KI', '1ki', '1 Kings', '1_Kings'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597948: {"name": "2 Kings", "abbrev": "2KI", "syn": ['2KI', '2ki', '2 Kings', '2_Kings'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597949: {"name": "1 Chronicles", "abbrev": "1CH", "syn": ['1CH', '1ch', '1 Chronicles', '1_ChronICLES'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597950: {"name": "2 Chronicles", "abbrev": "2CH", "syn": ['2CH', '2ch', '2 Chronicles', '2_ChronICLES'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597951: {"name": "1 Esdras", "abbrev": "EZR", "syn": ['EZR', 'ezr', '1 Esdras', '1_Esdras', 'Ezra', 'ezra'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597952: {"name": "Nehemiah", "abbrev": "NEH", "syn": ['NEH', 'neh', 'Nehemiah', 'nehemiah', '2 Esdras'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597953: {"name": "Esther", "abbrev": "EST", "syn": ['EST', 'est', 'Esther', 'esther'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597954: {"name": "Judith", "abbrev": "JDT", "syn": ['JDT', 'jdt', 'Judith', 'judith'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597955: {"name": "Tobit", "abbrev": "TOB", "syn": ['TOB', 'tob', 'Tobit', 'tobit'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597956: {"name": "1 Maccabees", "abbrev": "1MA", "syn": ['1MA', '1ma', '1 Maccabees', '1_Maccabees'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597957: {"name": "2 Maccabees", "abbrev": "2MA", "syn": ['2MA', '2ma', '2 Maccabees', '2_Maccabees'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597958: {"name": "Psalms", "abbrev": "PSA", "syn": ['PSA', 'psa', 'Psalms', 'psalms', 'Psalmi'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597959: {"name": "Prayer of Manasses", "abbrev": "MAN", "syn": ['MAN', 'man', 'Prayer of Manasses', 'prayer_of_manasses'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597960: {"name": "Proverbs", "abbrev": "PRO", "syn": ['PRO', 'pro', 'Proverbs', 'proverbs'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597961: {"name": "Ecclesiastes", "abbrev": "ECC", "syn": ['ECC', 'ecc', 'Ecclesiastes', 'ecclesiastes'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597962: {"name": "Job", "abbrev": "JOB", "syn": ['JOB', 'job', 'Job', 'job'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597963: {"name": "Wisdom", "abbrev": "WIS", "syn": ['WIS', 'wis', 'Wisdom', 'wisdom'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597964: {"name": "Ecclesiasticus", "abbrev": "SIR", "syn": ['SIR', 'sir', 'Ecclesiasticus', 'ecclesiasticus', 'Sirach', 'sirach'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597965: {"name": "Psalmi Salomonis", "abbrev": "PSS", "syn": ['PSS', 'pss', 'Psalmi Salomonis', 'psalmi_salomonis'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597966: {"name": "Hosea", "abbrev": "HOS", "syn": ['HOS', 'hos', 'Hosea', 'hosea'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597967: {"name": "Amos", "abbrev": "AMO", "syn": ['AMO', 'amo', 'Amos', 'amos'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597968: {"name": "Micah", "abbrev": "MIC", "syn": ['MIC', 'mic', 'Micah', 'micah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597969: {"name": "Joel", "abbrev": "JOL", "syn": ['JOL', 'jol', 'Joel', 'joel'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597970: {"name": "Obadiah", "abbrev": "OBA", "syn": ['OBA', 'oba', 'Obadiah', 'obadiah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597971: {"name": "Jonah", "abbrev": "JON", "syn": ['JON', 'jon', 'Jonah', 'jonah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597972: {"name": "Nahum", "abbrev": "NAM", "syn": ['NAM', 'nam', 'Nahum', 'nahum'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597973: {"name": "Habakkuk", "abbrev": "HAB", "syn": ['HAB', 'hab', 'Habakkuk', 'habakkuk'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597974: {"name": "Zephaniah", "abbrev": "ZEP", "syn": ['ZEP', 'zep', 'Zephaniah', 'zephaniah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597975: {"name": "Haggai", "abbrev": "HAG", "syn": ['HAG', 'hag', 'Haggai', 'haggai'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597976: {"name": "Zechariah", "abbrev": "ZEC", "syn": ['ZEC', 'zec', 'Zechariah', 'zechariah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597977: {"name": "Malachi", "abbrev": "MAL", "syn": ['MAL', 'mal', 'Malachi', 'malachi'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597978: {"name": "Isaiah", "abbrev": "ISA", "syn": ['ISA', 'isa', 'Isaiah', 'isaiah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597979: {"name": "Jeremiah", "abbrev": "JER", "syn": ['JER', 'jer', 'Jeremiah', 'jeremiah'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597980: {"name": "Lamentations", "abbrev": "LAM", "syn": ['LAM', 'lam', 'Lamentations', 'lamentations'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597981: {"name": "Ezekiel", "abbrev": "EZK", "syn": ['EZK', 'ezk', 'Ezekiel', 'ezekiel'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
        597982: {"name": "Daniel", "abbrev": "DAN", "syn": ['DAN', 'dan', 'Daniel', 'daniel'], "words": 1, "chapters": 1, "lemmas": 1, "morphs": 1},
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


    def pos(self,wordid):
        return self.api.F.pos.v(wordid)
        
    def apparatusNote(self,book,chapter,verse):
        return ''
    def getLemma(self,wordid):
        lemma = super().getLemma(wordid)
        filtered = re.sub('[\]0-9!%*,.:;=?$]','',lemma)
        return lemma if filtered else ''

