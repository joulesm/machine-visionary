# ## Using Python 2.7
# # Module that takes input "visionary" text and
# # parses out the parts of speech for replacement

import httplib, urllib, base64, json, time
import traceback

class ParseVisionText:

  params = urllib.urlencode({})

  change_tags = ["JJ", "JJR", "JJS", "NN", "NNS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
  valid_tags = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "POS", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB"]
  allowed_punct = ["'", "!", ".", ",", "?"]

  # Available analyzerIds:
  POS_tags = "4fa79af1-f22c-408d-98bb-b7d7aeef7f04"
  Constituency_Tree = "22a6b758-420f-4745-8a3c-46835a67c0d2"
  Tokens = "08ea174b-bfdb-4e64-987e-602f85da7f72"
  body = {
    "language" : "en",
  }

  headers = {
    # Request headers
   "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": "31b69098875f40a0a8fef462f1731a94",
  }

  url = "/linguistics/v1.0/analyze?{}"

  def __init__(
      self,
      POS_tags_analyzer = True,
      c_tree_analyzer = False,
      tokens_analyzer = False):
    analyzers = []
    if POS_tags_analyzer:
      analyzers.append(self.POS_tags)
    if c_tree_analyzer:
      analyzers.append(self.Constituency_Tree)
    if tokens_analyzer:
      analyzers.append(self.Tokens)
    self.body["analyzerIds"] = analyzers
    self.tags_dict = {}
    self.quote_dict = {}
    self.quote = ""

  def demotivate(self, quote, tags):
    self.parseQuote(quote)
    self.parseTags(tags)
    return self.mergeQuotesAndTags()

  def parseQuote(self, quote):
    self.quote = quote
    self.body["text"] = quote
    desc = self.doConn()
    if desc:
      self.quote_tags = json.loads(desc)[0]["result"][0]
      for i in range(len(self.quote_tags)):
        if self.quote_tags[i] not in self.valid_tags:
          del self.quote_tags[i]
    return self.quote_tags

  def parseTags(self, tags):
    tags_dict = {}
    tags_sentence = " ".join(tags)
    self.body["text"] = tags_sentence
    desc = self.doConn()
    if desc:
      words = tags_sentence.split(" ")
      desc_json = json.loads(desc)
      for i in range(len(words)):
        tags_dict[words[i]] = desc_json[0]["result"][0][i]
    self.tags_dict = tags_dict
    return tags_dict

  def mergeQuotesAndTags(self):
    words = self.quote.split(" ")
    for i in range(len(words)):
      if self.quote_tags[i] in self.change_tags:
        new_tag = self.replaceTag(self.quote_tags[i])
        if new_tag:
          # checking for punctuation
          if words[i][-1] in self.allowed_punct:
            punct = words[i][-1]
            words[i] = new_tag + punct
            i += 1
          else:
            words[i] = new_tag
    return " ".join(words)

  def replaceTag(self, replace_tag):
    for word, tag in self.tags_dict.iteritems():
      if tag == replace_tag:
        del self.tags_dict[word]
        return word

  def doConn(self):
    try:
      conn = httplib.HTTPSConnection("api.projectoxford.ai")
      conn.request(
        "POST",
        url = self.url.format(self.params),
        body = json.dumps(self.body),
        headers = self.headers)
      response = conn.getresponse()
      data = response.read()
      conn.close()
      return data
    except Exception as e:
      traceback.print_exc()
      print str(e)

#####

if __name__ == "__main__":
  quote = "make America great!"
  print quote
  tags = ["outdoor", "cat", "red", "tree", "purple", "building", "$", "''", "()", ",", "--", "!", ";"]
  print tags
  print ParseVisionText().demotivate(quote, tags)
