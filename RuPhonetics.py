"""
Simple school-level phonetic analysis (transcription) in Russian language.
Usage:
    Phonetic(word, stressed syllable number)
Output:
    Phonetic: word -> [transcription]
"""


class Phonetic:
    replacements = {
        "вств": "ств",
        "дс": "ц",
        "дц": "цц",
        "дч": "чч",
        "его": "ево",
        "жч": "щщ",
        "здн": "зн",
        "здц": "сц",
        "здч": "щщ",
        "зж": "жж",
        "зч": "щщ",
        "зш": "шш",
        "лнц": "нц",
        "ндск": "нск",
        "ндц": "нц",
        "ндш": "нш",
        "нтг": "нг",
        "нтск": "нск",
        "рдц": "рц",
        "рдч": "рч",
        "сж": "жж",
        "стл": "сл",
        "стн": "сн",
        "стс": "сс",
        "стч": "щщ",
        "стьс": "сс",
        "сч": "щщ",
        "сш": "шш",
        "сщ": "щщ",
        "тс": "цц",
        "тц": "цц",
        "тч": "чч",
        "тщ": "чщ",
        "шч": "щщ"
    }

    ending_replacements = {
    "ого": "ово",
    "тся": "цца",
    "ться": "цца"
    }

    def __init__(self, word, stress=None):
        """
        :word: Word string.
        :stress: Stressed syllable number.
        """
        if not word:
            raise Exception("No word provided.")
        self.word = self.__word_in_proccess = word.lower().strip()

        syllables = self.syllable_count()

        self.stress = int(stress) if stress else None
        self.stress = 1 if syllables == 1 else self.stress
        if self.stress and not (0 < self.stress <= syllables):
            raise Exception("Number of a stressed syllable is out of bounds.")
        if not self.stress and syllables > 0:
            raise Exception("No stressed syllable number provided.")

        self.replace_endings()
        self.replace_all()

    def __repr__(self):
        return f"Phonetic: {self.word} -> [{self.to_phonetic(False)}]"

    def syllable_count(self):
        return sum([letter in Letter.vowels for letter in self.word])

    def replace_endings(self):
        """
        Replace pronunciation complications at the end of a word.
        """
        for old, new in sorted(
            self.ending_replacements.items(),
            key=lambda x: -len(x[0])
        ):
            if self.__word_in_proccess.endswith(old):
                self.__word_in_proccess = self.__word_in_proccess[: -len(old)] + new

    def replace_all(self):
        """
        Replace pronunciation complications in a word.
        """
        for old, new in sorted(
                self.replacements.items(),
                key=lambda x: -len(x[0])
        ):
            self.__word_in_proccess = self.__word_in_proccess.replace(old, new)

    def to_phonetic(self, return_letter_list=True):
        """
        :return_letter_list: If True, function returns a list of Letter objects,
                              if False - a string.
        """
        sounds = []
        last_letter = None
        vowel_counter = 0

        for l in self.__word_in_proccess:
            stressed = False
            if l in Letter.vowels:
                vowel_counter += 1
                if vowel_counter == self.stress:
                    stressed = True
            if l.isalpha():
                letter = Letter(letter=l, prev=last_letter, stressed=stressed)
                sounds.append(letter)
                last_letter = letter
            else:
                sounds.append(l)

        if not isinstance(sounds[-1], str):
            sounds[-1].set_last()

        if return_letter_list:
            return sounds

        return "".join(map(lambda x: x.get_sound() if not isinstance(x, str) else x, sounds))


class Letter:
    # Vowel types
    vowels = "аеёиоуыэюя"

    prev_hard_vowels = "аоуыэ"  # Make previous consonant hard
    prev_soft_vowels = "еёиюя"  # Make previous consonant soft

    ioted_vowels = {  # Ioted vowels (consonant [й'] + vowel)
        'е': 'э',
        'ё': 'о',
        'ю': 'у',
        'я': 'а'
    }

    # Consonant types
    consonants = "бвгджзйклмнпрстфхцчшщ"

    const_hard = "жшц"  # Always hard
    const_soft = "йчщ"  # Always soft

    const_voiced = "йлмнр"  # Always voiced
    const_unvoiced = "xцчщ"  # Always unvoiced

    voiced_unvoiced = (  # Voiced - unvoiced pairs
        ('б', 'п'),
        ('в', 'ф'),
        ('г', 'к'),
        ('д', 'т'),
        ('ж', 'ш'),
        ('з', 'с')
    )

    signs = "ъь"  # Signs of hardness/softness

    def __init__(self, letter, prev=None, stressed=False):
        """
        :letter: Letter string.
        :prev: Previous letter in the word (Letter object), if exists.
        :stressed: If the letter is a stressed vowel - True, else - False.
        """
        if prev and not isinstance(prev, self.__class__):
            raise Exception(f"Previous letter should be a {self.__class__} object "
                            f"or None.\n A {prev.__class__} object is provided.")
        self.prev = prev

        self.letter = letter.lower().strip()
        if len(self.letter) != 1:
            raise Exception(f"Letter should be a 1 character long string.")

        if not self.is_ru_letter():
            raise Exception(f"Not a Russian letter provided.")

        self.stressed = self.is_vowel() if stressed else False

        self.voiced = (self.letter in self.const_voiced or
                       self.letter in map(lambda x: x[0], self.voiced_unvoiced))
        self.set_prev_voiceness()

        self.soft = self.letter in self.const_soft
        self.set_prev_softness()

        self.display = True
        self.double = False
        self.set_double()

        self.last = False

    def __repr__(self):
        return f"Letter: {self.letter} -> [{self.get_sound()}]"

    def is_vowel(self):
        return self.letter in self.vowels

    def is_consonant(self):
        return self.letter in self.consonants

    def is_sign(self):
        return self.letter in self.signs

    def is_ru_letter(self):
        return (self.is_vowel() or
                self.is_consonant() or
                self.is_sign())

    def is_paired(self):
        return (True if
                list(filter(lambda x: self.letter in x, self.voiced_unvoiced))
                else False)

    def set_prev_voiceness(self):
        """
        Set the voiceness attribute of a previous letter.
        """
        prev = self.prev
        if (not prev or not
        (self.is_consonant()
         and prev.is_consonant())):
            return

        if (self.voiced and
                self.is_paired() and
                self.letter != 'в'):
            prev.voiced = True
            prev.set_prev_voiceness()

        if not self.voiced:
            prev.voiced = False
            prev.set_prev_voiceness()

    def set_prev_softness(self):
        """
        Set the softness attribute of a previous letter.
        """
        prev = self.prev
        if not (prev and prev.is_consonant()):
            return

        if ((self.letter in self.prev_soft_vowels or
             self.letter == 'ь') and
                self.prev.letter not in self.const_hard):
            prev.soft = True
            prev.set_prev_softness()

        elif ((self.letter in self.prev_hard_vowels or
               self.letter == 'ъ') and
              self.prev.letter not in self.const_soft):
            prev.soft = False
            prev.set_prev_softness()

    def set_double(self):
        """
        Set attributes of double consonants.
        """
        prev = self.prev
        if not prev:
            return

        if (self.is_consonant() and
                prev.is_consonant() and
                self.get_sound() == prev.get_sound()):
            prev.display = False
            self.display = True
            prev.double = True
            self.double = True

    def get_vowel_sound(self):
        """
        :return: Sound corresponding to a vowel.
        """
        prev = self.prev
        let = self.letter

        if let in self.ioted_vowels.keys():
            pure = self.ioted_vowels[let]
            if (not prev or prev.is_vowel() or prev.is_sign()):
                let = f"й'{pure}"
            elif not self.stressed:
                let = 'и'
            else:
                let = pure

        if let == 'о' and not self.stressed:
            let = 'а'

        if (let == 'и') and prev:
            if prev.is_sign():
                let = "й'и"
            elif prev.letter in prev.const_hard:
                let = 'ы'

        return let

    def get_variant(self):
        """
        :return: Sound from voiced - unvoiced pairs.
        """
        if not self.is_paired():
            return self.letter

        pair = list(filter(lambda x: self.letter in x, self.voiced_unvoiced))[0]

        return pair[0] if self.voiced else pair[1]

    def get_sound(self):
        """
        :return: Sound corresponding to a letter.
        """
        if self.is_sign() or not self.display:
            return ""

        if self.is_vowel():
            return self.get_vowel_sound()

        sound = self.get_variant()

        if self.soft:
            sound += "'"

        if self.double:
            sound += ":"

        return sound

    def set_last(self):
        """
        Set last consonant unvoiced.
        """
        self.last = True

        if (self.is_consonant() and
                self.voiced and
                self.letter not in self.const_voiced):
            self.voiced = False
            self.set_prev_voiceness()