from requests_html import HTMLSession
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import copy

import datetime
import sqlite3

import mysql
import mysql.connector
import sshtunnel


import random
import math
import time
import sys
import re

# from .import errors as e
import errors as e

SLEEP_TIME = 5




# SCRAPE ME WHAT YOU'VE GOT!!
# ____________  ________
#             \/
#         ___
#     . -^   `--,
#    /# =========`-_
#   /# (--====___====\
#  /#   .- --.  . --.|
# /##   |  * ) (   * ),
# |##   \    /\ \   / |
# |###   ---   \ ---  |
# |####      ___)    #|
# |######           ##|
#  \##### ---------- /
#   \####           (
#    `\###          |
#      \###         |
#       \##        |
#        \###.    .)
#         `======/

data = None

proxy = None
user_agent = None



#This Section For Creating Clients, Browsers, and using Proxies

def new_browser_selenium(browser, element):
  window_before = browser.window_handles[0]
  element.click()
  time.sleep(1)

  ActionChains(browser) \
  .key_down(Keys.CONTROL) \
  .click(add_to_cart) \
  .key_up(Keys.CONTROL) \
  .perform()

  print("There can only be one thing to click")
  time.sleep(2)
  window_after = browser.window_handles[1]
  browser.switch_to_window(window_after)
  print("Im on the second browser")



def selenium_and_soup(url,i="0"):
  print("Using selenium and soup")
  soup = None
  browser = get_selenium_browser()
  try:
    browser.get(url)
  except:
    print(i)
    i = i+1
    selenium_and_soup(url,i)
    if i ==100:
      print("It timed out 101 times")
      time.sleep(90000)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  browser.quit()
  return soup

def headless_selenium_and_soup(url):
  soup = None
  browser = get_headless_selenium_browser()
  browser.get(url)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  browser.quit()
  return soup



def selenium_and_soup_no_quit(url):
  soup = None
  browser = get_selenium_browser()
  browser.get(url)
  code = browser.page_source
  soup = BeautifulSoup(code, "html.parser")
  return soup


def get_selenium_browser():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address

  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)
  opts = Options()
  ua = load_user_agent()
  user_agent_arg = "user-agent="+ua
  print(user_agent_arg)
  # time.sleep(100)
  opts.add_argument(user_agent_arg)
  # time.sleep(11100)
  # capabilities =

  browser = webdriver.Chrome(chrome_options=opts, desired_capabilities = capabilities)

  return browser


# def get_selenium_browser():
#   prox = Proxy()
#   prox.proxy_type = ProxyType.MANUAL
#   proxy_address = get_proxy()
#   prox.http_proxy = proxy_address
#   prox.socks_proxy = proxy_address
#   prox.ssl_proxy = proxy_address

#   capabilities = webdriver.DesiredCapabilities.CHROME
#   prox.add_to_capabilities(capabilities)

#   # capabilities =
#   browser = webdriver.Chrome(desired_capabilities = capabilities)

#   return browser


def get_headless_selenium_browser():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address


  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)

  chrome_options = Options()
  ua = load_user_agent()
  user_agent_arg = "user-agent="+ua
  print(user_agent_arg)

  chrome_options.add_argument(user_agent_arg)
  prefs={"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096 }
  chrome_options.add_experimental_option('prefs', prefs)

  chrome_options.add_argument("headless")
  # capabilities =
  browser = webdriver.Chrome(chrome_options=chrome_options,desired_capabilities = capabilities)

  return browser



def get_selenium_browser_random_proxy():
  prox = Proxy()
  prox.proxy_type = ProxyType.MANUAL
  proxy_address = get_random_proxy()
  prox.http_proxy = proxy_address
  prox.socks_proxy = proxy_address
  prox.ssl_proxy = proxy_address

  capabilities = webdriver.DesiredCapabilities.CHROME
  prox.add_to_capabilities(capabilities)

  # capabilities =
  browser = webdriver.Chrome(desired_capabilities = capabilities)
  browser.set_page_load_timeout(1000)
  # driver.Manage().Timeouts().PageLoad = TimeSpan.FromSeconds(10);

  return browser



def get_secure_connection(url):

  code = None

  for i in range(10):

    session = HTMLSession()
    session.cookies.clear()

    proxy = get_proxy()
    user_agent = load_user_agent()

    session.proxies['https'] = 'https://astest:assembledtesting123@' + proxy
    session.proxies['http'] = 'http://astest:assembledtesting123@' + proxy

    headers = {
          'Connection' : 'close',
          'user-agent' : user_agent
        }

    try:
      code = session.get(url, headers=headers, timeout=15)
      if(code.status_code == 200):
        break

    except:
      proxy = None
      user_agent = None
      continue
  if(code is not None):
    code.html.render()
    code = code.html.html
  return code


def get_random_proxy():

  print("fetching a proxy ip . . . ")

  result_ip = None

  url = "https://www.us-proxy.org/"
  code = requests.get(url, timeout = 30)

  soup = BeautifulSoup(code.text, "html.parser")

  proxy_table = soup.findAll("tbody")

  if(proxy_table == None):
    print("ERROR: The proxy table is empty")
    return

  proxies = proxy_table[0].findAll("tr")

  while(result_ip == None):

    proxy = random.choice(proxies)

    td = proxy.findAll("td")
    type = str(td[4].string)
    https = str(td[6].string)

    if(type == "elite proxy" and https == "yes"):
      ip = str(td[0].string)
      port = str(td[1].string)

      result_ip = ip + ":" + port

  return result_ip




def get_proxy():

  result_ip = random.choice([
  '173.232.219.41:12345/',
  '23.108.233.113:12345/',
  '75.75.234.110:12345/',
  '173.232.219.198:12345/',
  '75.75.234.112:12345/'])

  return result_ip



def load_user_agent():

  lines = open("user_agents.txt").read().splitlines()
  ua = random.choice(lines)

  return ua


def sleep_counter(duration):
  for i in range(duration):
    time.sleep(1)

#
# class Client(QWebEnginePage):
#     def __init__(self,url):
#         global app
#         self.app = QApplication(sys.argv)
#         QWebEnginePage.__init__(self)
#         self.html = ""
#         self.loadFinished.connect(self.on_load_finished)
#         self.load(QUrl(url))
#         self.app.exec_()
#
#     def on_load_finished(self):
#         self.html = self.toHtml(self.Callable)
#         print("Load Finished")
#
#     def Callable(self,data):
#         self.html = data
#         self.app.quit()
