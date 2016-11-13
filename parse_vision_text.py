# ## Using Python 2.7
# # Module that takes input "visionary" text and
# # parses out the parts of speech for replacement

import httplib, urllib, base64, json
import traceback

class ParseVisionText:

  params = urllib.urlencode({})

  # Available analyzerIds:
  POS_tags = "4fa79af1-f22c-408d-98bb-b7d7aeef7f04"
  Constituency_Tree = "22a6b758-420f-4745-8a3c-46835a67c0d2"
  Tokens = "08ea174b-bfdb-4e64-987e-602f85da7f72"
  body = {
    "language" : "en",
    "analyzerIds" : [POS_tags]
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

  def parse(self, text):
    self.body["text"] = text
    try:
      conn = httplib.HTTPSConnection("api.projectoxford.ai")
      conn.request(
        "POST",
        url = self.url.format(self.params),
        body = json.dumps(self.body),
        headers = self.headers)
      response = conn.getresponse()
      data = response.read()
      #print(data)
      conn.close()
      return data
    except Exception as e:
      traceback.print_exc()
      print str(e)

#####

print ParseVisionText().parse("Julia you are super cute")
