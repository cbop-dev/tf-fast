class GreekUtils:
    # Class-level attributes (equivalent to static properties in JavaScript)
    greek_letters = list("αβγδεζηιθκλμνξοπρσςτυφχψωϝΑΒΓΔΕΖΗΙΘΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩϜ")
    greek_diac = '\u0314\u0313\u0342\u0301\u0345\u0308\u0300\''
    greek = greek_letters + list(greek_diac)
    latin_beta_code_letters = list("abgdezhiqklmncoprsstufxywvABGDEZHIQKLMNCOPRSTUFXYWV")
    greek_beta_diac = '()=/|+\\#'
    beta = latin_beta_code_letters + list(greek_beta_diac)
    latin_greek_map = {}
    greek_latin_map = {}

    # Static initialization block equivalent
    @classmethod
    def _initialize_maps(cls):
        for i in range(len(cls.greek_letters)):
            cls.latin_greek_map[cls.latin_beta_code_letters[i]] = cls.greek_letters[i]
            cls.greek_latin_map[cls.greek_letters[i]] = cls.latin_beta_code_letters[i]

    # Call initialization at class definition time
    

    @staticmethod
    def greek_to_beta(greek_string, case_sensitive=True):
        """
        Convert a Greek string to Beta Code.

        Args:
            greek_string (str): The Greek text to convert.
            case_sensitive (bool): Whether to preserve case (default: True).

        Returns:
            str: The Beta Code representation of the input.
        """
        beta_chars = []
        greek_string = GreekUtils.remove_diacritics(greek_string if case_sensitive else greek_string.lower())
        greek_chars = list(greek_string)
        for char in greek_chars:
            lookup_index = GreekUtils.greek_letters.index(char) if char in GreekUtils.greek_letters else -1
            if lookup_index >= 0:
                beta_chars.append(GreekUtils.latin_beta_code_letters[lookup_index])
            else:
                beta_chars.append(char)
        return ''.join(beta_chars)

    @staticmethod
    def beta_to_greek(beta_string):
        """
        Convert a Beta Code string to Greek.

        Args:
            beta_string (str): The Beta Code text to convert.

        Returns:
            str: The Greek representation of the input.
        """
        greek_chars = []
        latin_chars = list(beta_string)
        for char in latin_chars:
            lookup_index = GreekUtils.beta.index(char) if char in GreekUtils.beta else -1
            if lookup_index >= 0:
                greek_chars.append(GreekUtils.greek[lookup_index])
            else:
                greek_chars.append(char)
        result = ''.join(greek_chars)
        return result.replace('ς', 'σ').replace(r'σ$', 'ς', 1)

    @staticmethod
    def fuzzy_search_array(search_string, string_array, limit=-1):
        """
        Search an array of strings for matches containing the search string, with optional regex support.

        Args:
            search_string (str): The string to search for.
            string_array (list): List of strings to search in.
            limit (int): Maximum number of matches to return (default: -1 for no limit).

        Returns:
            list: Filtered list of matching strings.
        """
        import re

        s_string = search_string.replace('ς', 'σ')
        to_check = ['*', '?', '.', '+']

        class Counter:
            def __init__(self):
                self.count = 0

        counter = Counter()

        if any(c in s_string for c in to_check):
            s_string = s_string.replace('*', '.*').replace('?', '.?').replace('+', '.+')
            regex = re.compile(f'^{s_string}')

            def partial_match(string_obj):
                s_obj = string_obj.replace('ς', 'σ')
                if limit < 1 or counter.count < limit:
                    if regex.search(s_obj):
                        counter.count += 1
                        return True
                return False
        else:
            def partial_match(string_obj):
                s_obj = string_obj.replace('ς', 'σ')
                if limit < 1 or counter.count < limit:
                    if s_string in s_obj:
                        counter.count += 1
                        return True
                return False

        return [s for s in string_array if partial_match(s)]

    @staticmethod
    def remove_diacritics(greek):
        """
        Remove diacritics from a Greek string.

        Args:
            greek (str): The Greek text to process.

        Returns:
            str: The input string with diacritics removed.
        """
        remove_diacritics_map = {
            "A": "Α", "E": "Ε", "O": "Ο", "ΐ": "ι", "ά": "α", "έ": "ε", "ή": "η", "ί": "ι",
            "ΰ": "υ", "ϊ": "ι", "ϋ": "υ", "ό": "ο", "ύ": "υ", "ώ": "ω", "ἀ": "α", "ἁ": "α",
            "ἄ": "α", "ἅ": "α", "ἆ": "α", "Ἀ": "Α", "Ἁ": "Α", "Ἄ": "Α", "Ἅ": "Α", "Ἆ": "Α",
            "ἐ": "ε", "ἑ": "ε", "ἔ": "ε", "ἕ": "ε", "Ἐ": "Ε", "Ἑ": "Ε", "Ἔ": "Ε", "Ἕ": "Ε",
            "ἠ": "η", "ἡ": "η", "ἤ": "η", "ἥ": "η", "ἦ": "η", "ἧ": "η", "Ἠ": "Η", "Ἡ": "Η",
            "Ἤ": "Η", "ἰ": "ι", "ἱ": "ι", "ἴ": "ι", "ἵ": "ι", "ἶ": "ι", "ἷ": "ι", "Ἰ": "Ι",
            "Ἱ": "Ι", "ὀ": "ο", "ὁ": "ο", "ὄ": "ο", "ὅ": "ο", "Ὀ": "Ο", "ὐ": "υ", "ὑ": "υ",
            "ὔ": "υ", "ὕ": "υ", "ὖ": "υ", "ὗ": "υ", "Ὑ": "Υ", "ὠ": "ω", "ὡ": "ω", "ὥ": "ω",
            "ὦ": "ω", "ὧ": "ω", "Ὡ": "Ω", "ά": "α", "έ": "ε", "ή": "η", "ὶ": "ι", "ί": "ι",
            "ό": "ο", "ύ": "υ", "ώ": "ω", "ᾂ": "α", "ᾄ": "α", "ᾅ": "α", "ᾠ": "ω", "ᾳ": "α",
            "ᾴ": "α", "ᾶ": "α", "ῃ": "η", "ῄ": "η", "ῆ": "η", "ῇ": "η", "ΐ": "ι", "ῖ": "ι",
            "ῥ": "ρ", "ῦ": "υ", "Ῥ": "Ρ", "ῳ": "ω", "ῴ": "ω", "ῶ": "ω", "ῷ": "ω", "͑Ρ": "Ρ",
            "ᾤ": "ω"
        }
        return ''.join(remove_diacritics_map.get(c, c) for c in greek)

    @staticmethod
    def plain_greek(greek):
        """
        Return Greek text without diacritics for sorting/searching.

        Args:
            greek (str): The Greek text to process.

        Returns:
            str: The input string with diacritics removed.
        """
        return GreekUtils.remove_diacritics(greek)
    
GreekUtils._initialize_maps()