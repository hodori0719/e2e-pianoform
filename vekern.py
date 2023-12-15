import os

# CONSTANT MAPS

mididict = {'c': -6, 'd': -5, 'e': -4, 'f': -3, 'g': -2, 'a': -1, 'b': 0}
evaluate_accidental = {'--': -2, '-': -1, 'n': 0, '#': 1, '#': 2}
keydict = {'c': 5, 'd': 3, 'e': 1, 'f': 6, 'g': 4, 'a': 2, 'b': 0}

class Staff:
    '''
    class defining a single staff containing one or more voices.
    The principle idea is that certain semantic changes propagate throughout a
    staff. For instance, accidentals, key signatures, and clefs are applied
    per-staff, rather than per-voice.
    '''
    def __init__(self):
        self.key = [0, 0, 0, 0, 0, 0, 0]
        self.bar_key = {}
        self.clef = 0
        self.voices = 1

    def set_clef(self, staff_token):
        if staff_token[5] == 'G':
            self.clef = -2
        elif staff_token[5] == 'F':
            self.clef = 6
        self.clef += 2 * (int(staff_token[6]) - 1)

    def add_voice(self):
        self.voices += 1

    def remove_voice(self):
        self.voices -= 1

    def barline(self):
        return self.voices * '='

    def getVoices(self):
        return self.voices

    def reset_barline(self):
        self.bar_key = {}

    def see_accidental(self, note, accidental_token):
        accidental = evaluate_accidental[accidental_token]
        if note in self.bar_key:
            if self.bar_key[note] == accidental:
                return False
            self.bar_key[note] = accidental
            return True
        else:
            if self.key[keydict[note[0].lower()]] == accidental:
                return False
            self.bar_key[note] = accidental
            return True

    def change_key(self, key_token):
        self.key = [0, 0, 0, 0, 0, 0, 0]
        key_token = key_token[3:-1]
        key_index = 0
        for c in key_token:
            if c in keydict:
                key_index = keydict[c]
            else:
                self.key[key_index] += evaluate_accidental[c]

    def notetolocation(self, note, accidental=None):
        '''
        Given a note in the bekrn notation, and an accidental in the bekrn
        notation, converts it to midi pitch class.
        '''
        # middle line is 0
        midi = mididict[note[0].lower()]
        octave = 7;
        if note.isupper():
            octave *= -1
            midi += octave

        if len(note) > 1:
            midi += (len(note) - 1) * octave

        return midi + self.clef

def bekrn_to_vekrn(b_file, v_file):
    '''
    Given path to a file in .bekrn format, generates a corresponding .vekrn
    encoding and saves it into the same parent directory.
    '''
    # sample file
    # filename = '/Users/hodori/Desktop/grandstaff/beethoven/piano-sonatas/sonata01-1/original_m-70-75.bekrn'

    krnlines = []
    Y = []

    with open(b_file) as krnfile:
        krn = krnfile.read()
        krn = krn.replace(" ", " <s> ")
        krn = krn.replace("·", " ")
        lines = krn.split("\n")
        for line in lines:
            line = line.replace("\t", " <t> ")
            line = line.split(" ")
            if len(line) > 1:
                line.append("<b>")
                krnlines.append(line)
        Y.append(sum(krnlines, []))

    outfile = ''
    staves = [Staff(), Staff()]
    for krnline in krnlines:
        voice = 0
        staff = 0
        lastSeenAccidental = None
        lastSeenNote = None
        justSawNote = False

        for token in krnline:
            newline = ''
            separator = False
            afk = False

            if justSawNote:
                if token in evaluate_accidental:
                    lastSeenAccidental = token
                    afk = True
                else:
                    lastSeenAccidental = 'n'
                if staves[staff].see_accidental(lastSeenNote, lastSeenAccidental):
                    outfile += lastSeenAccidental + '·'
                else: # the accidental is implied, not visually evident.
                    if token in evaluate_accidental:
                        afk = True
                justSawNote = False

            if token == '<t>':
                voice += 1
                staff = 0
                totvoices = staves[staff].getVoices()
                while voice >= totvoices:
                    staff += 1
                    if staff < len(staves):
                        totvoices += staves[staff].getVoices()
                    else:
                        staff -= 1
                        break
                newline += '\t'
                separator = True
            elif token == '<b>':
                voice = 0
                staff = 0
                newline += '\n'
                separator = True
            elif token == '<s>':
                newline += ' '
                separator = True
            elif token[0].lower() in mididict:
                # A NOTE IS FOUND
                lastSeenNote = token
                newline += 'N' + str(staves[staff].notetolocation(token))
                justSawNote = True
            elif token == 'X':
                # this symbol displays the accidental of the current note no matter what
                if lastSeenAccidental:
                    newline += lastSeenAccidental
                else:
                    newline += 'n'
            elif 'staff' in token: # relic of kern that encodes no visual information
                newline += '*'

            else:
                # NON-ALTERABLE TOKENS
                if '*k' in token:
                    staves[staff].change_key(token)
                if 'clef' in token:
                    staves[staff].set_clef(token)
                elif token == '*^':
                    staves[staff].add_voice()
                elif token == '*v':
                    staves[staff].remove_voice()
                elif '=' in token:
                    staves[staff].reset_barline()


                newline += token

            if not separator and not afk:
                newline += '·'
                outfile += newline
            elif not afk:
                outfile = outfile[:-1] + newline

    with open(v_file, 'w') as outf:
        outf.write(outfile)

# ////////////////////////////////////////////////////

data_dir = 'Data/grandstaff'

for subdir, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.bekrn'):
            b_file = os.path.join(subdir, file)
            v_file = os.path.splitext(b_file)[0] + '.vekrn'
            bekrn_to_vekrn(b_file, v_file)
