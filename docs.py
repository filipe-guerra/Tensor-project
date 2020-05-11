import docx
from tensor_analyse import *

class Compare_texts:
    def __init__(self, old_file, new_file):
        self.old_text = getText(old_file)
        self.old_analyse = New_analyse(self.old_text)
        self.encoder = set_encoder(self.old_analyse.tokens)
        self.old_analyse.encode_token(self.encoder)
        
        self.new_text = getText(new_file)
        self.new_analyse = New_analyse(self.new_text)
        self.new_analyse.encode_token(self.encoder)        

        self.compare_arrays = Compare_arrays(self.old_analyse, self.new_analyse)

    def old_unlinked_print(self):
        self.unlinked_print(self.compare_arrays.old_unlinked)

    def new_unlinked_print(self):
        self.unlinked_print(self.compare_arrays.new_unlinked)

    def unlinked_print(self, unlinked):
        for line in unlinked:
            print('---Paragraph ' + str(line))
            print(self.new_text[line])

class Compare_sequential:
    def __init__(self, old_file, new_file):
        self.old_text = getText(old_file)
        self.old_analyse = New_analyse(self.old_text)
        self.encoder = set_encoder(self.old_analyse.tokens)
        self.old_analyse.encode_token(self.encoder)
        
        self.new_text = getText(new_file)
        self.new_analyse = New_analyse(self.new_text)
        self.new_analyse.encode_token(self.encoder)     

    def compare(self):
        i1 = self.old_analyse.encoded
        i2 = self.new_analyse.encoded
        first_item_positions = [i for i,x in enumerate(i1) if x==i2[0]]
        true_sequence = []
        for position in first_item_positions:
            try:
                iteri1 = iter(i1[position:])
                for iteri2 in i2:
                    if iteri2 != next(iteri1):
                        true_sequence.append(False)
                        break
                else:
                    true_sequence.append(True)
                    break
            except:
                true_sequence.append(False)
        return True in true_sequence

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for paragraph in doc.paragraphs:
        fullText.append(paragraph.text)
    return fullText

# text = getText('demo.docx')

# text_analyse = New_analyse(text)
# print(text_analyse.tokens)

# encoder = set_encoder(text_analyse.tokens)

# text_analyse.encode_token(encoder)
# text_analyse.encoded

cs = Compare_sequential('seq1.docx', 'seq2.docx')
print(cs.compare())

# ct = Compare_texts('demo.docx', 'demo2.docx')
# ct.new_unlinked_print()