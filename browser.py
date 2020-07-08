from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import os
import time
import pickle
import sys
from data import *

def LaunchSelenium():
    options = Options()
	# Following two lines makes the chrome browser not show
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
    
    # Keeps browser open
    #options.add_experimental_option("detach", True)
    options.add_argument("user-data-dir=selenium")
    browser = webdriver.Chrome('./chromedriver', chrome_options=options)
    return browser

def Login(browser):
    # Getting the first URL
    browser.get("https://indberet.virk.dk/nemlogin/login?f=/integration/ERST/Start_virksomhed")

    # Trying to login automatically
    time.sleep(1)
    #LoginWithKeyfile(browser)
    #LoginWithNemID(browser, nemid, password)
    
    # Letting the user login manually with NemID or key
    while not "virksomhedsregistrering/betingelser" in browser.current_url:
        time.sleep(1)
    
    browser.find_element_by_id("acceptBetingelser").click()
    browser.find_element_by_id("fortsaetButton").click()

    # If we don't sleep for 1 sec the page does not load for some reason
    time.sleep(1)

def LoginWithKeyfile(browser):
    browser.find_element_by_xpath("/html/body/form/div[3]/div[1]/div/div/ul/li[2]/a/span[2]").click()
    time.sleep(2)
    action = ActionChains(browser)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.RETURN)
    time.sleep(2)
    action.send_keys('miro12sd')
    action.move_by_offset(100, 100)
    action.send_keys('miro12sd')
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.RETURN)
    action.perform()

def LoginWithNemID(browser):
    action = ActionChains(browser) 
    action.send_keys(nemid)
    action.send_keys(Keys.TAB)
    action.send_keys(password)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.ENTER)
    time.sleep(1)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    action.send_keys(Keys.TAB)
    time.sleep(1)
    action.move_by_offset(100, 100)
    action.send_keys(Keys.RETURN)
    action.perform()

def MainSubsequentReg(browser, company):
    Login(browser)
    
    # Starting the timer
    start_time = time.time()

    browser.get("https://erst.virk.dk/virksomhedsregistrering/aendring/")
    
    # Searching for company name
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/fieldset/div/input[1]").send_keys(company.name + " " + company.companytype)
    browser.find_element_by_id('submitSearch').click()
    time.sleep(2)
    browser.find_element_by_id('filter').click()
    time.sleep(1)

    # Figuring out where our company figures on the list and click the link
    n = FindCompanyOnList(browser.page_source, company.name + " " + company.companytype)
    browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div/div[" + str(n) + "]/div[7]/div/a").click()
    
    # Getting the CVR number from the URL
    company.cvr = browser.current_url[-8:]
    browser.get(url="https://erst.virk.dk/virksomhedsregistrering/aendring/vis?handling=aendre&vrNummer=" + company.cvr)
    
    # Click on the VAT link
    browser.find_element_by_id('pligter-link').click()
    
    # Getting the case ID from the URL
    ID = browser.current_url[32:44]

    # VAT
    if company.vat == True:
        browser.find_element_by_id('moms_erValgt').click()
        time.sleep(1)
        browser.find_element_by_id('OMSAETNING_UNDER_55_MIO').click()
        time.sleep(2)
        try:
            browser.find_element_by_id('moms_nyStartdato').send_keys(company.effectDate)
        except:
            browser.refresh()
            browser.find_element_by_id('moms_nyStartdato').send_keys(company.effectDate)

    # Import
    if company.imports == True:
        browser.find_element_by_id('importpligt_erValgt').click()
        time.sleep(1)
        browser.find_element_by_id('importpligt_nyStartdato').send_keys(company.effectDate)

    # Eksport
    if company.exports == True:
        browser.find_element_by_id('eksport_eksportValgt').click()
        time.sleep(1)
        browser.find_element_by_id('eksport_nyStartdato').send_keys(company.effectDate)

    # Lønsumsafgift (missing information)
    if company.lonsum == True:
        browser.find_element_by_id('loensumspligtig_erValgt').click()
        time.sleep(1)
        browser.find_element_by_id('loensumspligtigValgt_true').click()
        browser.find_element_by_id('loensumsmetode_nyStartdato').send_keys(company.effectDate)
        while not "overblik/index" in browser.current_url:
            time.sleep(1)
    
    if company.lonsum == True or company.exports == True or company.imports == True or company.vat == True:
        try:
            browser.find_element_by_xpath("/html/body/form/div/div[2]/div[2]/div[4]/div/div/div/input[2]").click()
        except:
            browser.find_element_by_xpath("/html/body/form/div/div[2]/div[2]/div[5]/div/div/div/input[2]").click()

    # Employer
    if int(company.numberemployees) > 0:
        browser.get(url="https://erst.virk.dk/aendringer/" + ID + "/ansaettelsesforhold/index")
        browser.find_element_by_id('loen_erValgt').click()
        time.sleep(1)
        browser.find_element_by_id('ALMINDELIG_LOENUDBETALING').click()
        time.sleep(1)
        browser.find_element_by_id('askat_askatValgt').click()
        time.sleep(1)
        browser.find_element_by_id('antalansatte_antalansatte').send_keys(company.numberemployees)
        browser.find_element_by_id('ambidrag_ambidragValgt').click()
        browser.find_element_by_id('MAANEDLIG_AFREGNING').click()
        browser.find_element_by_id('loen_nyStartdato').send_keys(company.effectDate)
        
        if company.more_than_nine == True:
            browser.find_element_by_id('atp_atpValgt').click()
            time.sleep(1)
            browser.find_element_by_id('atp_nyStartdato').send_keys(company.effectDate)
            time.sleep(1)
            browser.find_element_by_xpath("/html/body/form/div/div[2]/div[2]/div[4]/div/div/div/input[2]").click()
    
    browser.get(url="https://erst.virk.dk/aendringer/" + ID + "/overblik/tilOpsummering/tilOpsummering-button")
    
    timeToExecute = (time.time() - start_time)
    try:
        while 'opsummering/index' in browser.current_url:
            time.sleep(1)
    except:
        pass
    return timeToExecute, ID

def FindCompanyOnList(html, name):
    html = html.split('<div id="searchResultHeader">')
    html = html[1]
    html = html.split('<h1 class="section">Dine virksomheder</h1>')
    html = html[0]
    results = html.split('<div class="row searchResult ">')
    i = 1
    for item in results:
        if name in item:
            print('YAY')
            break
        i+=1
    return i

def MainCapitalCompany(browser, legalOwnerList, managementList, company, jsondata, email):
    Login(browser)

    start_time = time.time()
    browser.get("https://indberet.virk.dk/nemlogin/login?f=/integration/ERST/Start_virksomhed")

    # ----- Page 1 -----
    browser.get("https://erst.virk.dk/start/type/aps")
    browser.find_element_by_id('navn').send_keys(company.name + " " + company.companytype)
    
    # Secondary name
    for item in company.secondaryName:
        time.sleep(1)
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/fieldset[1]/div[3]/div[2]/input").click()
        time.sleep(2)
        browser.find_element_by_id('binavn_binavn').send_keys(item)
        

    # Inserting the adress
    browser.find_element_by_id('hjemstedsadresse_adresse').send_keys(company.validateadress)
    # See if there is a suggestions and clicks it.
    time.sleep(1)
    try:
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/fieldset[2]/div[1]/div/span/span[2]/div[1]/span/div").click()
    except:
        pass

    # E-mail reklamebeskyttelse
    browser.find_element_by_id('obligatoriskEmail').send_keys(company.email)
    browser.find_element_by_id("reklamebeskyttelse").click()
    
    # Stiftelses og virkningsdato
    browser.find_element_by_id('stiftelsesdato').send_keys(company.signingDate)
    browser.find_element_by_id('virkningsdato').send_keys(company.effectDate)

    ID = browser.current_url[27:39]

    browser.find_element_by_id("virknext").click()

    # ----- Page 2 -----

    # Owners
    PopulateOwners(browser, jsondata, legalOwnerList)
    
    # Management
    time.sleep(1)
    PopulateManagement(browser, jsondata, managementList)
    
    time.sleep(2)
    browser.get(url="https://erst.virk.dk/start/" + ID + "/formaal/index")

    # ----- Page 2 -----
    time.sleep(1)
    browser.find_element_by_id('formaal').send_keys(company.purpose)
    browser.find_element_by_id('tegningsregelEdit').send_keys(company.powertobind)

    if company.industrycode != "":    
        browser.find_element_by_id("hovedbrancheknap").click()
        time.sleep(1)
        browser.find_element_by_id('er3branchekodevaelger').send_keys(company.industrycode)
        time.sleep(1)
        try:
            browser.find_element_by_class_name("btn_vaelg").click()
        except:
            pass
    
    browser.find_element_by_id("gemOgLukKladdenLink").click()
    time.sleep(2)
    browser.get(url="https://erst.virk.dk/start/" + ID + "/kapital/index")

    # ----- Page 3 -----
    
    # Selskabskapital
    select = Select(browser.find_element_by_id("kapital_kapitalIndskud_kapitalPoster_0_indbetalingsMaade"))
    select.select_by_visible_text("Kontant klientkonto")    
    browser.find_element_by_id('kapital_kapitalIndskud_kapitalPoster_0_nomineltBeloeb').send_keys(company.capital)
    browser.find_element_by_id('kapital_kapitalIndskud_kapitalPoster_0_kurs').send_keys("100")

    # Aktieklasser
    browser.find_element_by_id("false").click()

    # Kapitalgodkendelse
    if email != 'test@legaldesk.dk':
        browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/form/div[1]/div[3]/fieldset/div[2]/input").click()
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="hentGodkendelseFraTredjepartSubmit"]').click()
        time.sleep(2)
        browser.find_element_by_id('kapitalIndskud_tredjepartsInvitationer[0]_email').send_keys(email)
        browser.find_element_by_id("tilfoejGodkendelse").click()
        time.sleep(1)

    # Regnskabsår
    browser.find_element_by_id('regnskab_regnskabsaar_startDato-field').send_keys(company.fiscalstart)
    browser.find_element_by_id('regnskab_regnskabsaar_slutDato-field').send_keys(company.fiscalend)

    # Revisor
    if company.audited == False:
        time.sleep(1)
        browser.find_element_by_id("FRAVALGT").click()
        time.sleep(1)
        browser.find_element_by_id("revision_accepteretErklaeringFravalgRevision").click()
    else:
        browser.find_element_by_id("VALGT").click()
        browser.find_element_by_linkText('Revisionsvirksomhed').click()
        #browser.find_elements_by_class_name('btn-group')[0].click()
        #browser.find_elements_by_class_name('linkCprPerson')[0].click()        

    #First Fiscal Year
    yearList = ["2025", "2024", "2023", "2022", "2021", "2020"]
    
    browser.find_element_by_id("gemOgLukKladdenLink").click()
    time.sleep(2)
    browser.get(url="https://erst.virk.dk/start/" + ID + "/kapital/index")
    time.sleep(1)
    try:
        select = Select(browser.find_element_by_id('regnskab_foersteregnskabsperiode_slutDato'))
        for item in yearList:
            try:
                select.select_by_visible_text(item)
                break
            except:
                pass
    except:
        pass
    
    browser.find_element_by_id("virknext").click()
    browser.get(url="https://erst.virk.dk/start/" + ID + "/opsummering/index")
    
    timeToExecute = (time.time() - start_time)

    try:
        while not "virksomhedsregistrering/registreringer" in browser.current_url:
            time.sleep(1)
    except:
        pass
    return timeToExecute, ID

def PopulateOwners(browser, jsondata, legalOwnerList):
    i = 0
    while i < int(jsondata['ejere']['antalejer_radio']):
        # Open dropdown
        time.sleep(1)
        browser.find_elements_by_class_name('btn-group')[0].click()
        # If Danish company
        if legalOwnerList[i].cvr != "":
            browser.find_elements_by_class_name('linkVrVirksomhed')[0].click()
            time.sleep(1)
            browser.find_element_by_id('stiftere_vrVirksomhed_vrNummer').send_keys(legalOwnerList[i].cvr)
            if legalOwnerList[i].cvr == 'Indtast CVR-nummer <---':
                while len(browser.find_element_by_id('stiftere_vrVirksomhed_vrNummer').get_attribute("value")) != 8:
                    print(browser.find_element_by_id('stiftere_vrVirksomhed_vrNummer').get_attribute("value"))
                    time.sleep(1)

        # If Danish person
        if legalOwnerList[i].cpr != "":
            browser.find_elements_by_class_name('linkCprPerson')[0].click()
            time.sleep(1)
            browser.find_element_by_id('stiftere_cprPerson_navn').send_keys(legalOwnerList[i].name)
            browser.find_element_by_id('stiftere_cprPerson_cprNummer').send_keys(legalOwnerList[i].cpr)
        
        browser.find_element_by_id("ejerTilfoejKnap").click()
        i+=1

def PopulateManagement(browser, jsondata, managementList):
    i = 0
    for item in managementList:
        time.sleep(1)
        browser.find_elements_by_class_name('btn-group')[1].click()
        browser.find_elements_by_class_name('linkCprPerson')[1].click()
        
        time.sleep(1)
        browser.find_element_by_id('ledelse_cprPerson_navn').send_keys(managementList[i].name)
        browser.find_element_by_id('ledelse_cprPerson_cprNummer').send_keys(managementList[i].cpr)
        time.sleep(1)

        # Executive properties
        if managementList[i].executive == True:
            browser.find_element_by_id("ledelse_medlemIDirektion").click()
            if managementList[i].president == True:
                browser.find_element_by_id("ADM_DIREKTOER").click()
            else:
                browser.find_element_by_id("DIREKTOER").click()

        # Board properties
        if managementList[i].board == True:
            browser.find_element_by_id("ledelse_medlemIBestyrelse").click()
            if managementList[i].president == True:
                browser.find_element_by_id("BESTYRELSESFORMAND").click()
            else:
                browser.find_element_by_id("BESTYRELSESMEDLEM").click()
        
        time.sleep(1)
        try:
            browser.find_elements_by_id("ejerTilfoejKnap")[0].click()
        except:
            pass
        try:
            browser.find_elements_by_id("ejerTilfoejKnap")[1].click()
        except:
            pass
        try:
            browser.find_elements_by_id("ejerTilfoejKnap")[2].click()
        except:
            pass
        try:
            browser.find_elements_by_id("ejerTilfoejKnap")[3].click()
        except:
            pass
        i+=1
    return i
