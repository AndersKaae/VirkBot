from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import pickle
from data import Company, Owner, Manager

def browser(url):
    options = Options()
	# Following two lines makes the chrome browser not show
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
    
    # Keeps browser open
    options.add_experimental_option("detach", True)

    options.add_argument("--user-data-dir=chrome-data")

    browser = webdriver.Chrome('./chromedriver', chrome_options=options)

    # Getting the first URL
    browser.get(url=url)

    while not "virksomhedsregistrering/betingelser" in browser.current_url:
        time.sleep(1)
    browser.find_element_by_id("acceptBetingelser").click()
    browser.find_element_by_id("fortsaetButton").click()
    
    # If we don't sleep for 2 sec the page does not load for some reason
    time.sleep(1)
    
    # ----- Page 1 -----
    browser.get("https://erst.virk.dk/start/type/aps")
    browser.find_element_by_id('navn').send_keys(c1.name)
    browser.find_element_by_id('hjemstedsadresse_adresse').send_keys(c1.adress)
    browser.find_element_by_id('obligatoriskEmail').send_keys(c1.email)
    browser.find_element_by_id("reklamebeskyttelse").click()
    browser.find_element_by_id('stiftelsesdato').send_keys(c1.signingDate)
    browser.find_element_by_id('virkningsdato').send_keys(c1.effectDate)
    browser.find_element_by_id("virknext").click()

    # ----- Page 2 -----
    
    # Owners
    browser.find_elements_by_class_name('btn-group')[0].click()
    browser.find_elements_by_class_name('linkCprPerson')[0].click()
    
    time.sleep(1)
    browser.find_element_by_id('stiftere_cprPerson_navn').send_keys(o1.name)
    browser.find_element_by_id('stiftere_cprPerson_cprNummer').send_keys(o1.cpr)
    browser.find_element_by_id("ejerTilfoejKnap").click()
    
    # Management
    time.sleep(1)
    browser.find_elements_by_class_name('btn-group')[1].click()
    browser.find_elements_by_class_name('linkCprPerson')[1].click()
    
    time.sleep(1)
    browser.find_element_by_id('ledelse_cprPerson_navn').send_keys(l1.name)
    browser.find_element_by_id('ledelse_cprPerson_cprNummer').send_keys(l1.cpr)

    browser.find_element_by_id("ledelse_medlemIDirektion").click()
    browser.find_element_by_id("ADM_DIREKTOER").click()
    browser.find_element_by_id("ejerTilfoejKnap").click()
    browser.find_element_by_id("virknext").click()

    # ----- Page 2 -----

    browser.find_element_by_id('formaal').send_keys(c1.purpose)
    browser.find_element_by_id('tegningsregelEdit').send_keys(c1.powertobind)
    browser.find_element_by_id("hovedbrancheknap").click()
    browser.find_element_by_id('er3branchekodevaelger').send_keys(c1.industrycode)
    time.sleep(1)
    browser.find_element_by_class_name("btn_vaelg").click()
    time.sleep(1)
    browser.find_element_by_id("virknext").click()

    # ----- Page 3 -----
    
    # Selskabskapital
    select = Select(browser.find_element_by_id("kapital_kapitalIndskud_kapitalPoster_0_indbetalingsMaade"))
    select.select_by_visible_text("Kontant klientkonto")
    browser.find_element_by_id('kapital_kapitalIndskud_kapitalPoster_0_nomineltBeloeb').send_keys(c1.capital)
    browser.find_element_by_id('kapital_kapitalIndskud_kapitalPoster_0_kurs').send_keys("100")

    # Aktieklasser
    browser.find_element_by_id("false").click()

    # Regnskabsår
    browser.find_element_by_id('regnskab_regnskabsaar_startDato-field').send_keys(c1.fiscalstart)
    browser.find_element_by_id('regnskab_regnskabsaar_slutDato-field').send_keys(c1.fiscalend)

    # Revisor
    browser.find_element_by_id("FRAVALGT").click()
    time.sleep(1)
    browser.find_element_by_id("revision_accepteretErklaeringFravalgRevision").click()
    
    browser.get(url="https://erst.virk.dk/start/X20-CW-13-GH/ejerforhold/index")

    # ----- Page 4 -----

    print('DONE')
    return browser.page_source

o1 = Owner("person_with_cpr", "Anders Lyager Kaae", "030382-1163")
l1 = Manager("person_with_cpr", "Anders Lyager Kaae", "030382-1163")
c1 = Company("Testselskabet ApS", "NULL", "Trommesalen 4, 5. th , 1614 København V", "info@legaldesk.dk", False, "01-07-2020", "10-07-2020", "Selskabets formål er at være awesome.", "Selskabet tegnes af en direktør.", "90.01.20", "40000", "01-01", "31-12", "2021")

browser("https://indberet.virk.dk/nemlogin/login?f=/integration/ERST/Start_virksomhed")