from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def browser(url):
    options = Options()
	# Following two lines makes the chrome browser not show
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
    options.add_experimental_option("detach", True)
    browser = webdriver.Chrome('./chromedriver', chrome_options=options)
    browser.get(url=url)
    browser.sendkeys("TEST")


    return browser.page_source

browser("https://indberet.virk.dk/nemlogin/login?f=/integration/ERST/Start_virksomhed")