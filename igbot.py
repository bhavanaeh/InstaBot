from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common import exceptions
import getpass
from datetime import datetime
from selenium.webdriver.common.by import By
from random import randint
import os

newlist=[]

class InstagramBot:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.base_url = 'https://www.instagram.com/'
        self.driver.execute_script("alert('Please check your console window')")
        try:
            alert= self.driver.switch_to.alert
            time.sleep(2)
            alert.accept()
        except Exception:
            pass
        self.login()
    
    def open_chrome(self):
        self.driver= webdriver.Chrome('./chromedriver.exe')
        self.base_url = 'https://www.instagram.com/'

    def login(self):
        self.username = str(input("\nEnter your username: "))   
        self.password = getpass.getpass(prompt='Password (Hidden Entry): ')
        print("\nPlease check your browser again")
        self.driver.get(self.base_url)
        time.sleep(2)
        self.driver.find_element_by_xpath('//input[@name= \"username\"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//input[@name= \"password\"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//button[@type= "submit"]').click()
        time.sleep(2)

        try:
            self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]').click()
        except Exception:
            self.go_to_my_profile()
            self.driver.execute_script('alert("Please keep an eye on your console window for the options/functionalities available,Thank You!")')
            try:
                alert= self.driver.switch_to.alert
                time.sleep(5)
                alert.accept()
            except Exception:
                pass
    
    def go_to_my_profile(self):
        self.driver.get(self.base_url + self.username)
        time.sleep(2)
    
    def get_followers_list(self):
        self.go_to_my_profile()
        #Getting Followers list below
        print('\nList of your followers:')
        time.sleep(2)
        self.driver.find_element_by_xpath("//a[@href= '/{}/followers/']".format(self.username)).click()
        time.sleep(2)
        scrollbox= self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height, curr_height= 0, 1
        while last_height!= curr_height:
            last_height= curr_height
            time.sleep(1)
            curr_height= self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollbox
            )
            time.sleep(1)
        follower_links= scrollbox.find_elements_by_tag_name('a')
        followers_names= [name.text for name in follower_links]
        [followers_names.remove(x) for x in followers_names if x=='']
        try:
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div/div[2]/button').click() #Click the [x] button for followers
        except Exception:
            self.driver.refresh()
            time.sleep(2)
        return followers_names

    def get_following_list(self):
        self.go_to_my_profile()
        #Getting Following list below
        print('List of people, you follow:')
        self.driver.find_element_by_xpath("//a[@href= '/{}/following/']".format(self.username)).click()
        time.sleep(1)
        scrollbox= self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_height, curr_height= 0, 1
        while last_height!= curr_height:
            last_height= curr_height
            time.sleep(1)
            curr_height= self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);
            return arguments[0].scrollHeight;
            """, scrollbox
            )
            time.sleep(1)
        following_links= scrollbox.find_elements_by_tag_name('a')
        following_names= [name.text for name in following_links]
        [following_names.remove(x) for x in following_names if x=='']
        return following_names

    def get_unfollowers(self):
        followers_names= self.get_followers_list()  #Getting Followers list 
        following_names= self.get_following_list()  #Getting Following list 
  
        #Getting Non-followers
        for x in following_names:
            if not x in followers_names:
                newlist.append(x)                
                print(x)
        
        print('\nFollowers: ' + str(len(followers_names)), end='')
        print('\nFollowing: ' + str(len(following_names)))
        print('\nNumber of Non-followers: ' + str(len(newlist)) + '\n')

    
    def logout(self):
        self.driver.get(self.base_url + self.username)
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/div[1]/div/button').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//button[contains(text(), "Log Out")]').click()


    def close_browser(self):
        self.driver.close()





try:
    obj = InstagramBot()
    while(True):
        choice= input("Please select a functionality for the bot to perform:\n\n1. Navigate to Your Profile\n2. Check who is not following you back\n3. Log Out\nPlease press ctrl+c for the bot to stop the process,Thank You!")
        if choice=='1':
            print('Loading')
            obj.go_to_my_profile()
        if choice=='2': 
            print('Loading')
            obj.get_unfollowers()
        if choice=='3':
            print('Thank You for visiting!')
            try:
                obj.close_browser()
            except Exception:
                break
except KeyboardInterrupt:
    print('\nProcess Interrupted. Thanks for visiting!\n')