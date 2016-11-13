# ## Using Python 2.7
# # Module that takes input "visionary" text and
# # parses out the parts of speech for replacement

import httplib, urllib, base64, json, time
import traceback

class ParseVisionText:

  params = urllib.urlencode({})

  change_tags = ["NN", "JJ"]

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
    return self.quote_tags

  def parseTags(self, tags):
    tags_dict = {}
    for tag in tags:
      self.body["text"] = tag
      desc = self.doConn()
      if desc:
        words = tag.split(" ")
        for i in range(len(words)):
          tags_dict[words[i]] = json.loads(desc)[0]["result"][0][i]
      time.sleep(1)
    self.tags_dict = tags_dict
    return tags_dict

  def mergeQuotesAndTags(self):
    words = self.quote.split(" ")
    for i in range(len(words)):
      if self.quote_tags[i] in self.change_tags:
        words[i] = self.replaceTag(self.quote_tags[i])
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
  quote = "make America great again"
  print quote
  tags = ["outdoor", "cat", "red", "tree", "purple building"]
  print tags
  print ParseVisionText().demotivate(quote, tags)