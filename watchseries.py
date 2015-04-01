#!/bin/bash/python

import requests
import codecs
import os
import sys
from lxml import etree
import pickle



series_db = {}
names = []
master_url = "http://watchseriestv.to"


def save_data(data, name ):
    f = open('/tmp/'+ name + '.pkl', 'wb')
    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    f.close()

def load_data(name):
    f = open('/tmp/' + name + '.pkl', 'rb')
    ret = pickle.load(f)
    f.close()
    return ret

#Menu to be used throughout the program
def menu(title, body, options):
    '''
    Accepts a list of options to display
    Good idea to pass the keys of a dict as options
    '''

    
    os.system('clear')
    print title
    print '-'*(len(title)+5)
    print '\n' + body + '\n'    #add .wrap to body
    if len(options) > 0:
        total_opt = len(options)
        index = 1
        menuitem = {}
        for key in options:
            print str(index) + ". " + key
            menuitem[str(index)] = key
            index = index + 1
        #get option from user
        confirm = 'n'
        while confirm != 'y':
            choice = raw_input("\nEnter number corresponding to choice or q to quit : ")
            if choice in ['q', 'b']:
                return choice
            print "Your Choice - " + choice + " : " + menuitem[str(choice)]
            '''
            confirm = raw_input("Sure ?(y/n)")
            '''
            confirm = 'y'
        return menuitem[str(choice)]
    else:
        data = raw_input(">>> ")
        if data == 'q':
            quit()
        return data

def handle_cmd(cmd):
    if cmd == 'q':
        quit()
    elif cmd == 'b':
        return 'b'
    else:
        return 'ok'

#Populate the series_db dictionary with all episodes
def create_db(url, xpath_seasons, xpath_names, xpath_links, xpath_season_urls, listing):
    response = requests.post(url)
    data = response.text
    tree = etree.HTML(data)
    
    #Parse seasons, episodes and links    
    seasons = tree.xpath(xpath_seasons)
    season_urls = tree.xpath(xpath_season_urls)
    names = tree.xpath(xpath_names)
    links = tree.xpath(xpath_links)
    names.reverse()
    links.reverse()
    seasons.reverse()
    season_urls.reverse()

    
    
    #series_db = load_data('abc')
    episode_selected = -1
    #create record i.e. series_db

    while episode_selected != 1:
        if listing == "seasons":
            if episode_selected == -1:
                for season in seasons:
                    series_db[unicode(season)] = str(season_urls[seasons.index(season)])
                episode_selected = 0
            #provide menu
            body = "Seasons : " + str(len(seasons)) + "\nEpisodes : " + str(len(links)) + "\n"
            selected_key = menu("Your Series", body, seasons) #do not pass keys of series_db as they are sorted
            cmd = handle_cmd(selected_key)
            if cmd=='b':
                return cmd
            response = requests.post(series_db[unicode(selected_key)])
            data = response.text
            tree = etree.HTML(data)

            names = tree.xpath(xpath_names)
            links = tree.xpath(xpath_links)
            links.reverse()
            names.reverse()

        for name in names:
            if not((unicode(name)) in series_db.keys()):
                series_db[unicode(name)] = master_url + links[names.index(name)]

        
        #save data to file
        #save_data(series_db, 'abc')

        #provide menu
        selected_key = menu("Title", "Body", names) #do not pass keys of series_db as they are sorted; pass names
        cmd = handle_cmd(selected_key)
        
        if cmd == 'b' and listing=="seasons":
            episode_selected = 0
        elif cmd == 'b':
            return cmd
        else:
            episode_selected = 1


    return series_db[selected_key]
  
def gorillavid(url, str_or_dwn):

    '''
    This function will work in 4 stages
        1. Open Page with list of links
        2. Open gorillavid link
        3. Click the Blue continue button
        4. Extract video URL
    '''

    
    #stage 1
    response = requests.post(url)
    gorilla_data = response.text
    tree = etree.HTML(gorilla_data)

    xpath_gorilla = "//div[@id='linktable']/table/tbody/tr/td/a[@title='gorillavid.in']/@href"
    gorilla_nr = 1
    gorillas = tree.xpath(xpath_gorilla)
    
    for i in range(0,len(gorillas)):
        gorillas[i] = master_url + gorillas[i]
        print str(i+1) + ". Link " + str(i+1)
    
    #print gorillas
    
    #stage 2
    print str(len(gorillas)) + " gorillavid links found"
    if len(gorillas) == 0:
        quit()
    gorilla_nr = raw_input("Which Link do you want to run ? ")
    response = requests.post(gorillas[int(gorilla_nr) - 1])
    '''
    for i in range(0,len(gorillas)):
        response = requests.post(gorillas[int(gorilla_nr) - 1])
        if response == '200':
            break
    '''
    str(response.status_code)
    emb_data = response.text
    tree = etree.HTML(emb_data)

    xpath_simple_click = "//div/a[@class='push_button blue']/@href"
    simple_click = tree.xpath(xpath_simple_click)
    #print simple_click
    
    #stage 3
    id = simple_click[0].split('/')[-1]
    #id = id1[-1]
    print id
    continue_data = {'id' : str(id),
         'method_free' : 'Free Download',
         'op' : 'download1'}
    print "trying " + simple_click[0]
    response = requests.post(simple_click[0], data=continue_data)
    vid = response.text

    #stage 4
    vid = vid.encode('utf-8')
    words = vid.split(" ")
    video = []
    for word in words:
        if "video." in word:
            #print word
            video.append(word)
    link = str(video[1])[1:-2]
    print "Woo Hoo !! Got the video link - " + link
    if str_or_dwn == 'download':
        download_video(link)
    else:
        stream_video(link)

def download_video(lnk):
    cmd = "wget " + (lnk)
    os.system(cmd)

def stream_video(lnk):
#    cmd = "cvlc -v " + (lnk)
    cmd = "vlc " + (lnk)
    os.system(cmd)


def welcome():
    '''
    Searches for the name on watchseriestv.to and returns results
    '''
    os.system('clear')
    print "Welcome to this watchseriestv.to unofficial client\nCurrently only gorillavid is supported\n\nSearch your Series"
    key = raw_input("Press any key to continue ...")

def search():
    os.system('clear')
    name = menu("Search", "What's your poison ? ",[])
    cmd = handle_cmd(name)

    os.system('clear')
    #search_string = name.replace(" ","%20")
    search_string = unicode(name)
    print "Searching for " + name
    print "Please wait ..."
    search_url = master_url + "/search/" + search_string

    response = requests.post(search_url)
    results_data = response.text
    tree = etree.HTML(results_data)
    
    xpath_results = "//div/a/strong/text()"
    xpath_result_links = "//div/div/div/div/a[@target='_blank']/strong/parent::a/@href"
    results = tree.xpath(xpath_results)
    result_links = tree.xpath(xpath_result_links)

    #menu
    title = "Search Results"
    body = str(len(results)) + " matches for your search"
    series = {}
    i=0
    for result in results:
        
        series[result] = master_url + result_links[i]
        print series[result]
        i += 1

    selected_key = menu(title, body, series.keys())
    cmd = handle_cmd(selected_key)
    if cmd == 'b':
        return cmd
    return series[selected_key]

    
def main():    

    pages = { '1' : welcome,
              '2' : search,
              '3' : create_db,
              '4' : gorillavid
              }
    listing = "episodes"
    str_or_dw = "stream"
    if len(sys.argv)>1:
        if "-s" in sys.argv:
            listing = "seasons"
        
        if "-d" in sys.argv:
            str_or_dw = "download"

    
    xpath_season_nrs = "//div[@itemprop='season']/h2/a/span/text()"
    xpath_season_urls = "//div[@itemprop='season']/h2/a/@href"
    xpath_episodes = "//div[@itemprop='season']/ul/li/a/@href"
    xpath_ep_name = "//div[@itemprop='season']/ul/li/a/span[@itemprop='name']/text()"

    url='b'
    episode = 'b'
    while 1:
        while episode == 'b':
            while url=='b':
                url = search()
            episode = create_db(url,xpath_season_nrs, xpath_ep_name, xpath_episodes, xpath_season_urls, listing)
            if episode == 'b':
                url = 'b'
            else:
                gorillavid(episode, str_or_dw)
                episode = 'b'


if __name__ == '__main__':
    main()
