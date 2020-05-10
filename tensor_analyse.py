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

class Compare_arrays:
    def __init__(self, old_text, new_text):
        self.old = old_text
        self.new = new_text
        self.linked = {}
        self.run_analyse()

    def run_analyse(self):
      for old_item_num, item in enumerate(self.old.encoded):
          for new_item_num, new_item in enumerate(self.new.encoded):
              if np.array_equiv(item, new_item):
                  self.linked[old_item_num] = new_item_num

      self.fill_old_unlinked()
      self.fill_new_unlinked()

    def fill_old_unlinked(self):
      num_old_items = list(range(len(self.old.encoded)))
      linked_keys = list(self.linked.keys())
      self.old_unlinked = [item for item in num_old_items if item not in linked_keys]
      
    def fill_new_unlinked(self):
      num_old_items = list(range(len(self.new.encoded)))
      linked_values = list(self.linked.values())
      self.new_unlinked = [item for item in num_old_items if item not in linked_values]
      
    def old_changed_paragraphs(self):
      for i in self.old_unlinked:
        print("----- old paragraph changed -----")
        print(self.old.paragraphs[i][0])

    def new_changed_paragraphs(self):
      for i in self.new_unlinked:
        print("----- new paragraph changed -----")
        print(self.new.paragraphs[i][0])

def set_encoder(text_tokens):
  vocabulary_set = set()
  for words in text_tokens.to_list():
      vocabulary_set.update(words)

  encoder = tfds.features.text.TokenTextEncoder(vocabulary_set)
  return encoder
