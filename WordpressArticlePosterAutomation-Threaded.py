# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import unittest, time, re, os, threading, random
import urllib2, shutil
from os import listdir
import sys
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStore
from evernote.api.client import EvernoteClient
from docx import Document


url_l=[]

def make_first_note(url_l):
    dev_token = "x"
    client = EvernoteClient(token=dev_token, sandbox=False)
    note_store=client.get_note_store()

    message=''
    for i in url_l:
        message+='<br>'+i+'</br>'

    #message='<br>'+url+'</br>'

    note = Types.Note() 
    note.title = "Article Editing + Theme Editing Job (%s)" %(time.strftime("%d/%m/%Y"))
    note.content = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note><br>1. Please go to all URL's and check if the formatting of the articles are OK</br>
<br>2. Insert 1-2 relevant images for the articles, that don't have any images.</br>
<br>3. Publish ONE article now. Publish every other article +7 or +14 or +21 days</br>
<br>4. Change theme settings, create a logo and upload that logo to the blog</br>
<br>Here are the article urls:</br>
<br></br>
%s</en-note>
    """ %(message)

    try:
        createdNote = note_store.createNote(note)
    except Exception, e:
        print type(e)
        print e
        raise SystemExit

    print "First nNote created!"


def make_second_note(url_l):
    dev_token = "x"
    client = EvernoteClient(token=dev_token, sandbox=False)
    note_store=client.get_note_store()

    message=''
    for i in url_l:
        message+='<br>'+i+'</br>'

    #message='<br>'+url+'</br>'

    note = Types.Note() 
    note.title = "Backlinks(%s)" %(time.strftime("%d/%m/%Y"))
    note.content = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note><br>Insert Backlinks for the following articles:</br>
<br></br>
%s</en-note>
    """ %(message)

    now = int(round(time.time() * 1000)) 
    then = now + 864000000 # ten days after now

    # init NoteAttributes instance
    note.attributes = Types.NoteAttributes()
    note.attributes.reminderOrder = now
    note.attributes.reminderTime = then
    try:
        createdNote = note_store.createNote(note)
    except Exception, e:
        print type(e)
        print e
        raise SystemExit

    print "Second nNote created!"



class wordpressdriver(unittest.TestCase):
    def setUp(self):
        file_name = "postarticles.txt" # Input filename through RAW INPUT raw_input()
        if os.path.isfile(file_name):
            f = open(file_name, 'r')
            self.base_domain = (l.strip() for l in f.readlines())
            f.close()
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_python_web_driver_plugin_installieren(self):
        def do_all_work(domain_name):
            #Access folder with name same as domain_name
            file_list=listdir(os.getcwd()+'\\domains\\'+domain_name)

            #For Firefox
            # binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
            driver = webdriver.Chrome() #(firefox_binary=binary)


            #For PhantomJS
            #phantomjs_path = "C:\Program Files\Python27\misc\windows-x86_64-phantomjs.exe" #Ver 2.0.1
            #driver = webdriver.PhantomJS(executable_path=phantomjs_path, service_log_path=os.path.devnull)

            
            #Login
            url='http://www.'+domain_name+'/wp-login.php'
            #LOGIN TO Wordpress
            driver.maximize_window()
            driver.implicitly_wait(30) 
            driver.get(url)
            driver.find_element_by_id("user_login").click()
            driver.find_element_by_id("user_login").clear()
            time.sleep(3)
            driver.find_element_by_id("user_login").send_keys("xxxx") # USERNAME
            time.sleep(3)
            driver.find_element_by_id("user_pass").click()
            driver.find_element_by_id("user_pass").clear()
            time.sleep(3)
            driver.find_element_by_id("user_pass").send_keys("xxxx") # PASSWORD
            time.sleep(10)
            driver.find_element_by_id("wp-submit").click()
            driver.implicitly_wait(30)

            #LOGGED IN - SELF TEST
            try:
                self.assertEqual("Dashboard", driver.find_element_by_css_selector("h1").text)
                
            except:
                #NOT LOGGED IN - TRY AGAIN
                driver.maximize_window()
                driver.implicitly_wait(30) 
                driver.find_element_by_id("user_login").click()
                driver.find_element_by_id("user_login").clear()
                time.sleep(3)
                driver.find_element_by_id("user_login").send_keys("xxxx") # USERNAME
                time.sleep(2)
                driver.find_element_by_id("user_pass").click()
                driver.find_element_by_id("user_pass").clear()
                time.sleep(1)
                driver.find_element_by_id("user_pass").send_keys("xxx") # PASSWORD
                time.sleep(1)
                driver.find_element_by_id("wp-submit").click()

            
            for fl in file_list:
                    #If file is in .docx format
                    if '.docx' in fl:
                        document = Document(os.getcwd()+'\\domains\\'+domain_name+'\\'+fl)
                        #paragraphs = getdocumenttext(infil)
                        print 'Domain: %s, uploading file: %s' % (domain_name,fl)
                        new_paragraphs = []
                        for paragraph in document.paragraphs:
                            new_paragraphs.append(paragraph.text.encode('utf-8'))
                            #print paragraph.text.encode('utf-8')

                        
                        driver.get('http://www.'+domain_name+'/wp-admin/post-new.php')

                        #Insert title
                        driver.find_element_by_name('post_title').click()
                        driver.find_element_by_name('post_title').send_keys(unicode(new_paragraphs[0].decode("utf-8")))
                        print 'Title of article pasted.'

                        #Insert body of article
                        driver.find_element_by_id('content-tmce').click()
                        driver.find_element_by_id('content_ifr').click()
                        driver.find_element_by_id('content_ifr').send_keys('\n'.join(new_paragraphs[1:]))

                        #Save as draft
                        time.sleep(5)
                        driver.find_element_by_id('save-post').click()
                        time.sleep(5)
                        
                        driver.implicitly_wait(20)
                        #Get the current edit url of the document we uploaded
                        edit_url=driver.current_url+'\n'
                        print 'Edit url: ', edit_url.strip()
                        url_l.append(edit_url.strip())
                        #Create path to desktop
                        just_posted_path = os.sep.join((os.path.expanduser("~"),"Desktop"))

                        #Check if file exist and write edit_url_path
                        if os.path.isfile(just_posted_path+'\JustPosted-ArticlePoster2.txt'):
                            with open(just_posted_path+'\JustPosted-ArticlePoster2.txt','a') as f:
                                f.write(edit_url)
                        else:
                            with open(just_posted_path+'\JustPosted-ArticlePoster2.txt','w') as f:
                                f.write(edit_url)

                        print 'Uploading of file %s completed, moving to another.\n' % (fl)
                        shutil.move(sys.path[0]+'\\domains\\'+domain_name+'\\'+fl, sys.path[0]+'\\domains\\'+domain_name+'\\Posted\\'+fl)
                        



        #THREADING CODE
        for domain_name in self.base_domain:
            threading.Thread(target=do_all_work, args=[domain_name]).start()
            time.sleep(5)

        #Write to notes:
        make_first_note(url_l)
        make_second_note(url_l)
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
