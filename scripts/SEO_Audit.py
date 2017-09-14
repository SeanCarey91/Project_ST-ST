from lxml import html
import requests
import csv
from bs4 import BeautifulSoup
#
#
#Author: Sean Carey
#Date: 9/11/2017
#Version: 2.1 Beta
#Errors so far:
# 1. Score is not adding correctly
# 2. Title extract is not working correctly, need to strip html snippets
# 3. Client side vs. Server side has no single element. so need to figure out
#    what elements can be used.
#
#Variables
global urls
global page
global tree
global hs
hs =''
global httpStatus
httpStatus = ''
global robots
robots = ''
urls = raw_input("Please Enter URL:")
if urls == None:
    print "please restart & enter a correct url"
print "_____________________________\n"
global score
score = 0
global server
page = requests.get(urls)
tree = html.fromstring(page.content)
#Sign In button scrape for serverside code
def clientside():
    global urls
    global page
    global score
    global server
    status = ' '
    webpage= page
    soup= BeautifulSoup(webpage.text,"lxml")
    banner = soup.find(attrs={'id':'logo'})
    #Problem with below is unless the fast fonts url is exact it will not be found. need new way to find the script.
    jsScript = soup.find(attrs={'src':'//fast.fonts.net/'})
    if banner == None:
        status = 'Client Side Webpage'
        score ==0
    else:
        server= banner['title']
        status = 'Server Side Webpage'
        score == 1
    if jsScript == None:
        status = 'Server Side Webpage'
        score ==1
    else:
        status = 'Client Side Webpage'
        score ==0
    print status
    print "_____________________________\n"
    return score
#HTTP status code check
def httpStatus():
   global score
   global httpStatus
   try:
       status = requests.head(urls)
       code = status.status_code
       httpStatus = code
       print "HTTP Status:"
       print httpStatus
       print "_____________________________\n"
       return httpStatus
   except requests.ConnectionError:
       code = 'n/a'
       httpStatus = 'N/A'
       print "HTTP Status:"
       print httpStatus
       print "_____________________________\n"
       return httpStatus

#NoIndex/NoFollow test
def noIndex():
   global urls
   global page
   global score
   webpage= page
   soup= BeautifulSoup(webpage.text,"lxml")
   desc= soup.find(attrs={'name':'robots'})
   if desc == None:
       robots = "NONE"
       print "Page is ready to be Indexed!"
       print 'TEST: PASSED'
       print "_____________________________\n"
       score +=1
   else:
       robots = desc['content']
       print "Robots.txt:"
       print desc['content']
       print 'TEST: FAIL'
       print "_____________________________\n"
       score -=1
   return score

#Pass/Fail score
def finalScore():
    global score
    print "Final Score:"
    print score
    if score == 3:
       print "RESULT: PASSED"
       print "________________________\n"
    else:
       print "RESULT: FAILED"
       print "________________________\n"
       #quit()

def urlSyntax():
    global urls
    ssl = 'https://'
    w =  'www.'
    macys = 'macys.com'
    soc = '/social/'
    ce = '/ce'
    if ssl in urls:
        print "SSL: Pass"
        print "________________________\n"
    else:
        print "SSL: Fail"
        print "________________________\n"

    if w in urls and macys in urls:
        print "Macys Domain: Pass"
        print "________________________\n"
    else:
        print "Macys Domain: Fail"
        print "________________________\n"
    if soc in urls:
        print "This is an IMP site."
        print "________________________\n"
    if ce in urls:
        print "This is a CE site."
        print "________________________\n"

def tags():
    global urls
    global page
    webpage= page
    soup= BeautifulSoup(webpage.text,"lxml")
    canon= soup.find(attrs={'rel':'canonical'})
    alt= soup.find(attrs={'rel':'alternate'})
    #Canonical Check
    if canon == None:
        print "No Canonical Tag was found!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Cononical Tag:"
        print canon['href']
        print "_____________________________\n"
    #Alternate Check
    if alt == None:
        print "No Alternate Tag was found!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Aternate Tag:"
        print alt['href']
        print "_____________________________\n"

def metaDesc():
    global urls
    global page
    webpage= page
    soup= BeautifulSoup(webpage.text,"lxml")
    #title = soup.find(attrs={'name':''})
    desc = soup.find(attrs={'name':'description'})
    if desc == None:
        print "No Meta Description was found!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Meta Description:"
        print desc['content']
        print "________________________\n"
        charCount = desc['content']
        print "Description Character Count:"
        print len(charCount)
        print "_____________________________\n"

def metaTitle():
    global urls
    global page
    webpage= page
    soup= BeautifulSoup(webpage.text,"lxml")
    title = soup.findAll('title')
    #Need to find a way to convert this object to a string so I can remove the [<title> & </title>]
    #title.replace('[<title>', '')
    #title.replace('</title>]', '')
    print "Title Tag:"
    print title
    print "________________________\n"

def responsive():
    global urls
    global page
    webpage= page
    soup= BeautifulSoup(webpage.text,"lxml")
    respCode = soup.find(attrs={'name':'viewport'})
    if respCode == None:
        print "NOT RESPONSIVE!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Viewport Responsive Code:"
        print respCode['content']
        print "_____________________________\n"

#Output
#***Order of opertions executed does matter***
clientside()
httpStatus()
noIndex()
finalScore()
urlSyntax()
tags()
metaDesc()
metaTitle()
responsive()
