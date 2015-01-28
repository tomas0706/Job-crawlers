import urllib
import urllib2
import re 


data = urllib2.urlopen('http://www.snagajob.com/job-search?ui=true')
page = data.read()
print page
url_list = re.findall('<li class="facet-item"><a rel="nofollow" title=".*?" href="(.*?)">(.*?)</a> <span class="count">\(18589\)</span></li>', page)
print url_list