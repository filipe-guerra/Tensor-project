import tensorflow as tf
import numpy as np
import tensorflow_text as text 
import tensorflow_datasets as tfds

class New_analyse:
  def __init__(self, all_text):
    tokenizer = text.UnicodeScriptTokenizer()
    (self.tokens, self.offset_starts, self.offset_limits) = tokenizer.tokenize_with_offsets(all_text) 
    self.bigrams = text.ngrams(self.tokens, 2, reduction_type=text.Reduction.STRING_JOIN)

  def encode_token(self, encoder):
    temp_encoded = []
    has_index = lambda x: encoder.tokens.index(x.decode('ascii'))+1 if encoder.tokens.index(x.decode('ascii')) > 0 else 0
    has_encoder = lambda x: encoder.encode(x)[0] if len(encoder.encode(x)) > 0 else has_index(x)
    for line in self.tokens.to_list():
        temp_encoded.append(list(map(has_encoder, line)))

    self.encoded = [np.array(line, dtype=np.uint32) for line in temp_encoded] 
 
def set_encoder(text_tokens):
  vocabulary_set = set()
  for words in text_tokens.to_list():
      vocabulary_set.update(words)

  encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)
  return encoder
