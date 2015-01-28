import re
import urllib

data = urllib.urlopen('http://www.dice.com/job/results/communication?o=390&x=all&p=k')
page = data.read()
print page