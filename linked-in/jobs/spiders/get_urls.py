from selenium import webdriver
from selenium.webdriver.common.keys import Keys as k
import yaml
import os
import time
import pandas as pd

class linked_in:
  def __init__(self,browser,cfg):
    self.job_urls =[]
    self.cfg =cfg
    self.browser = browser
    self.login()
    self.jobs_data()
    # time.sleep(100)
  
  def login(self):
    self.browser.get(self.cfg['linkedin']['url'])
    user = self.browser.find_element_by_xpath('//*[@id="session_key"]')
    password = self.browser.find_element_by_xpath('//*[@id="session_password"]')
    user.send_keys(self.cfg['linkedin']['username'])
    password.send_keys(self.cfg['linkedin']['password'])
    button = self.browser.find_element_by_xpath('//*[@id="main-content"]/section[1]/div/div/form/button')
    button.click()
    
  def jobs_search(self):
    self.browser.set_window_size(700,800)
    data =pd.read_csv('data\lnpages.csv')
    urls = data['Urls'].to_list()
    for url in urls:
      self.browser.get(url)
      print(url)
      self.job_links()
    jb = pd.DataFrame(columns=['job urls'],data =self.job_urls)
    jb.to_csv('DL jobs.csv')
  
  def job_links(self):
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = self.browser.execute_script("return document.body.scrollHeight")
    i = 500
    while True:
      # Scroll down to bottom
      self.browser.execute_script("window.scrollTo(0, {});".format(i))
      # Wait to load page
      time.sleep(SCROLL_PAUSE_TIME)
      # Calculate new scroll height and compare with last scroll height
      new_height = self.browser.execute_script("return document.body.scrollHeight")
      print(last_height,new_height,i)
      if new_height == last_height:
        time.sleep(2)
        links = self.browser.find_elements_by_xpath('/html/body/div[5]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li/div/div/div[1]/div[2]/div[1]/a')
        if len(links) ==0:
          links = self.browser.find_elements_by_xpath('/html/body/div[6]/div[3]/div[3]/div[2]/div/section[1]/div/div/ul/li/div/div/div[1]/div[2]/div[1]/a')
        print(len(links))
        for link in links:
          self.job_urls.append(link.get_attribute('href'))
        break
      i=i+500
      last_height = new_height
        
    # sb = self.browser.find_elements_by_xpath('')
  
  def jobs_data(self):
    self.job_name=[]
    self.company_name=[]
    self.place=[]
    self.applicants=[]
    self.posted_at=[]
    self.job_type=[]
    self.num_emp=[]
    self.hiring_person=[]
    self.desc=[]
    self.pay=[]
    self.comp_type=[]
    data =pd.read_csv('DL jobs.csv')
    urls = data['job urls'].to_list()
    for url in urls:
      self.browser.get(url)
      self.data_extract()
    jb = pd.DataFrame(columns=['job name','company name','place','applicants','posted at','job type','num emp','hiring person','description','pay','sector'],data =list(zip(self.job_name,self.company_name,self.place,self.applicants,self.posted_at,self.job_type,self.num_emp,self.hiring_person,self.desc,self.pay,self.comp_type)))
    jb.to_csv('DL jobs.csv')
    
  def data_extract(self):
    SCROLL_PAUSE_TIME = 1
    # Get scroll height
    last_height = self.browser.execute_script("return document.body.scrollHeight")
    i = 700
    while True:
      # Scroll down to bottom
      self.browser.execute_script("window.scrollTo(0, {});".format(i))
      # Wait to load page
      time.sleep(SCROLL_PAUSE_TIME)
      # Calculate new scroll height and compare with last scroll height
      new_height = self.browser.execute_script("return document.body.scrollHeight")
      print(last_height,new_height,i)
      if new_height == last_height:
        try:
          page_state = self.browser.execute_script('return document.readyState;')
          if page_state == 'complete':
            print(page_state)
            try:
              more =self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button')
              # more.click()
              self.browser.execute_script("arguments[0].click();", more)
            except:
              more =self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/footer/button')
              # more.click()
              self.browser.execute_script("arguments[0].click();", more)
            time.sleep(1)
            try:
              self.job_name.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text)
            except:
              self.job_name.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/h1').text)
            try:
              self.company_name.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]/a').text)
            except:
              try:
                self.company_name.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]/a').text)
              except:
                try:
                  self.company_name.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]').text)
                except:
                  self.company_name.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[1]').text)
            try:
              self.place.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]').text)
            except:
              self.place.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[1]/span[2]').text)
            try:
              self.applicants.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[2]/span[2]/span').text)
            except:
              self.applicants.append(None)
            try:
              self.posted_at.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/span[2]/span[1]').text)
            except:
              self.posted_at.append(None)
            try:
              self.job_type.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/span').text)
            except:
              self.job_type.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/span').text)
            try:
              self.num_emp.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/span').text)
            except:
              self.num_emp.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[2]/span').text)
            try:
              self.hiring_person.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[3]/span').text)
            except:
              try:
                self.hiring_person.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div[3]/span').text)
              except:
                self.hiring_person.append(None)
            try:
              self.desc.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]').text)
            except:
              self.desc.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div/div[1]').text)
            try:
              self.pay.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[3]/div/h2').text.split()[:2])
            except:
              try:
                self.pay.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[3]/div/h2').text.split()[:2])
              except:
                self.pay.append(None)
            try:
              self.comp_type.append(self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[5]/section/section/div[1]/div[2]').text)
            except:
              try:
                self.comp_type.append(self.browser.find_element_by_xpath('/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[5]/section/section/div[1]/div[2]').text)
              except:
                self.comp_type.append(None)
            print(len(self.job_name),len(self.company_name),len(self.place),len(self.applicants),len(self.posted_at),len(self.job_type),len(self.num_emp),len(self.hiring_person),len(self.desc),len(self.pay))
                  # ,self.job_name,self.company_name,self.place,self.applicants,self.posted_at,self.job_type,self.num_emp,self.hiring_person,self.num_emp,self.desc,self.pay,self.comp_type,self.browser.find_element_by_xpath('/html/body/div[6]/div[3]/div/div[1]/div[1]/div/div[5]/section/section/div[1]/div[2]'))
            break
        except:
            break
      i=i+700
      last_height = new_height
    
class jobs_data:
  def __init__(self):
    config_path = os.path.join(os.getcwd(),'configuration/conf.yml')
    with open(config_path,'r') as f:
      self.cfg = yaml.full_load(f)
    driver_path = self.cfg["Driver"]['selenium driver path']
    # # browser_path = self.cfg['Driver']['brave path']
    option = webdriver.ChromeOptions()
    # option.binary_location = browser_path
    if self.cfg['Driver']['Headless']:
      option.add_argument("--headless")
    self.browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    self.load_browser()
  
  def load_browser(self):
    linked_in(self.browser,self.cfg)
    
jobs_data()