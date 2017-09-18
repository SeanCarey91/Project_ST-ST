import requests
import sys
from bs4 import BeautifulSoup

#
#
#Author: Sean Carey
#Date: 9/18/2017
#Version: 3.1 Beta
#Updated version with help from Alex Galea of Aiyma
#

def main():
    urls = raw_input("Please Enter URL:")
    if urls == None:
        sys.exit('please restart & enter a correct url')
    print "_____________________________\n"

    score = 0

    page = requests.get(urls)
    if not page.ok:
        sys.exit('4xx or 5xx status code returned')
    soup = BeautifulSoup(page.text, "lxml")

    #***Order of opertions executed does matter***
    server, status, score = clientside(soup, score)
    status_code = httpStatus(page)
    robots, score = noIndex(soup, score)
    finalScore(score)

    urlSyntax(urls)
    tags(soup)
    metaDesc(soup)
    metaTitle(soup)
    responsive(soup)

def clientside(soup, score):
    status = ''
    server = ''
    banner = soup.find(attrs={'id':'logo'})
    #Problem with below is unless the fast fonts url is exact it will not be found. need new way to find the script.
    jsScript = soup.find(attrs={'src':'//fast.fonts.net/'})
    if banner == None:
        status = 'Client Side Webpage'
        score -= 1
    else:
        server= banner['title']
        status = 'Server Side Webpage'
        score += 1
    if jsScript == None:
        status = 'Server Side Webpage'
        score +=1
    else:
        status = 'Client Side Webpage'
        score -= 1
    print status
    print "_____________________________\n"
    return server, status, score

def httpStatus(page):
    '''
    HTTP status code check
    '''
    httpStatus = page.status_code
    print "HTTP Status:"
    print httpStatus
    print "_____________________________\n"
    return httpStatus

def noIndex(soup, score):
    '''
    NoIndex/NoFollow test
    '''
    desc = soup.find(attrs={'name':'robots'})
    if desc == None:
        robots = "NONE"
        print "Page is ready to be Indexed!"
        print 'TEST: PASSED'
        print "_____________________________\n"
        score += 1
    else:
        robots = desc['content']
        print "Robots.txt:"
        print desc['content']
        print 'TEST: FAIL'
        print "_____________________________\n"
        score -= 1
    return robots, score

def finalScore(score):
    '''
    Pass/Fail score
    '''
    print "Final Score:"
    print score
    if score == 3:
       print "RESULT: PASSED"
       print "________________________\n"
    else:
       print "RESULT: FAILED"
       print "________________________\n"
       #quit()

def urlSyntax(urls):
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

def tags(soup):
    #Canonical Check
    canon = soup.find(attrs={'rel':'canonical'})
    if canon == None:
        print "No Canonical Tag was found!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Cononical Tag:"
        print canon['href']
        print "_____________________________\n"
    #Alternate Check
    alt = soup.find(attrs={'rel':'alternate'})
    if alt == None:
        print "No Alternate Tag was found!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Aternate Tag:"
        print alt['href']
        print "_____________________________\n"

def metaDesc(soup):
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

def metaTitle(soup):
    title = soup.title.get_text()
    print "Title Tag:"
    print title
    print "________________________\n"

def responsive(soup):
    respCode = soup.find(attrs={'name':'viewport'})
    if respCode == None:
        print "NOT RESPONSIVE!"
        print "TEST: FAIL"
        print "________________________\n"
    else:
        print "Viewport Responsive Code:"
        print respCode['content']
        print "_____________________________\n"

if __name__ == '__main__':
    main()
