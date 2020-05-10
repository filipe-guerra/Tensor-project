import docx
from tensor_analyse import *

def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return fullText

text = getText('demo.docx')

text_analyse = New_analyse(text)
print(text_analyse.tokens)

encoder = set_encoder(text_analyse.tokens)

text_analyse.encode_token(encoder)
text_analyse.encoded