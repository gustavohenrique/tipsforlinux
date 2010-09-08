# -*- coding: utf-8 -*-
import urllib

def get_tiny_url(url):
    try:
        apiurl = "http://tinyurl.com/api-create.php?url="
        quoted = urllib.quote_plus(url)
        tinyurl = urllib.urlopen(apiurl + quoted).read()
        return tinyurl
    except:
        return ""
   
def content_tiny_url(content):
    regex_url = r'http:\/\/([\w.]+\/?)\S*'
    for match in re.finditer(regex_url, content):
        url = match.group(0)
        content = content.replace(url,tiny_url(url))
    return content

"""
import unittest
class TinyUrlTest(unittest.TestCase):
    def testGenerateTinyUrl(self):
        google = tiny_url("http://www.google.com")
        self.assertEquals("http://tinyurl.com/1c2", google)

if __name__ == '__main__':
  unittest.main()
"""
