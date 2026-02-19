import unicodedata

class HebrewUtils:
    def normalize(string):
        theMap={"שׁ":"\uFB2A",#two characters of shin with dot -> combined single unicode char
        "שׂ": "\uFB2B"
        }

        for old,new in theMap.items():
            string=string.replace(old,new)

        return string

