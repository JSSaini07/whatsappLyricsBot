from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from musixmatch import ws
import json
import time
import urllib

url='https://web.whatsapp.com/'
driver = webdriver.Firefox()
driver.get(url)
notFound=True
ready=True
#scan the qr code (wait cycle)
while(notFound):
	print('Trying to open')
	html=driver.page_source
	soup=BeautifulSoup(html)
	if(soup.find("div", {"id": "side"})!=None):
		notFound=False
	time.sleep(0.5)

print('Opened')

def getApiKey():
	src=urllib.urlopen('http://jssaini07.github.io/creds/creds.html').read()
	src=src.split('splitPoint')[1]
	src=src.split("'")
	apikey=''
	for i in range(0,len(src)):
		if(src[i]!="'"):
			apikey=apikey+src[i]
	apikey=apikey.split('</p>')[0]
	return apikey

apikey=getApiKey()

#get lyrics for trackName
def findLyrics(trackName):
	global apikey
	searchResult=ws.track.search(q_track=trackName,apikey=apikey)
	searchResult=str(searchResult)
	searchResult=json.loads(searchResult)
	lyricsId=searchResult["message"]["body"]["track_list"][0]["track"]["track_id"]
	searchResult=ws.track.lyrics.get(track_id=lyricsId,apikey=apikey)
	searchResult=str(searchResult)
	searchResult=json.loads(searchResult)
	lyrics=searchResult["message"]["body"]["lyrics"]["lyrics_body"]
	return lyrics

#sendLyrics to chat
def sendLyrics():
	global ready
	element=driver.find_elements_by_class_name('chat-secondary')
	for e in element: 
		if('song "' in e.text):
			try:
				song=e.text.split('song "')[1]
				song=song.split('"')[0]
				print(e.text)
				print('current e')
				print(e)
				e.click()
				chatInput=driver.find_element_by_xpath("//div[@class='input']")
				lyrics=findLyrics(song)
				chatInput.send_keys(lyrics)
				sendButton=driver.find_element_by_class_name('send-container')
				sendButton.click()
			except:
				chatInput=driver.find_element_by_xpath("//div[@class='input']")
				chatInput.send_keys('Error')
				sendButton=driver.find_element_by_class_name('send-container')
				sendButton.click()
				pass
	print('setting ready true')
	element=[]
	ready=True

#keep listening for requests
while(True):
	if(ready):
		print('setting ready false')
		ready=False
		sendLyrics()