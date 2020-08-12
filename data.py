import json
import re
import requests

class Company:
  def __init__(self, name, companytype, secondaryName, adress, adress2, zipcode, city, validateadress, email, advertising, signingDate, effectDate, purpose, powertobind, industrycode, capital, fiscalstart, fiscalend, audited, accountantname, accountantcvr, vat, lonsum, imports, exports, numberemployees, more_than_nine):
    self.name = name
    self.companytype = companytype
    self.cvr = 'NULL'
    self.secondaryName = secondaryName
    self.adress = adress
    self.adress2 = adress2
    self.zipcode = zipcode
    self.city = city
    self.validateadress = validateadress
    self.email = email
    self.advertising = advertising
    self.signingDate = signingDate
    self.effectDate = effectDate
    self.purpose = purpose
    self.powertobind = powertobind
    self.industrycode = industrycode
    self.capital = capital
    self.fiscalstart = fiscalstart
    self.fiscalend = fiscalend
    self.audited = audited
    self.accountantname =  accountantname
    self.accountantcvr = accountantcvr
    self.vat = vat
    self.lonsum = lonsum
    self.imports = imports
    self.exports = exports
    self.numberemployees = numberemployees
    self.more_than_nine = more_than_nine

class LegalOwner:
    def __init__(self, name, cpr, cvr, adress, zipcode, city, country):
        self.name = name
        self.cpr = cpr
        self.cvr = cvr
        self.adress = adress
        self.zipcode = zipcode
        self.city = city
        self.country = country

class RealOwner:
    def __init__(self, kind, name, cpr, realowner, percentage):
        self.realowner = realowner
        self.name = name
        self.cpr = cpr
        self.percentage = percentage

class Management:
    def __init__(self, name, cpr, adress, zipcode, city, country, executive, president, board, chairman):
        self.name = name
        self.cpr = cpr
        self.adress = adress
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.executive = executive
        self.president = president
        self.board = board
        self.chairman = chairman

class Board:
    def __init__(self, name, cpr, adress, zipcode, city, country, chairman):
        self.name = name
        self.cpr = cpr
        self.adress = adress
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.chairman = chairman

def JsonParser(data):
    # Parse JSON data
    jsondata = json.loads(data, strict=False)
        
    # Create owners
    legalOwnerList = CreateLegalOwners(jsondata)

    # Create board, only used for easy consolidation into Management class
    boardList = CreateBoard(jsondata, legalOwnerList)

    # Create management
    managementList = CreateManagement(jsondata, legalOwnerList, boardList)

    # Create company
    company = CreateCompany(jsondata, legalOwnerList)

    return legalOwnerList, managementList, company, jsondata

def CreateLegalOwners(jsondata):
    ownerList = ["owner1", "owner2", "owner3", "owner4", "owner5", "owner6"]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    while i < int(jsondata['ejere']['antalejer_radio']):
        ownerList[i] = LegalOwner("", "", "", "", "", "", "")
        if jsondata['ejere']['ejer' + abc[i] + '_navn'] == "":
            ownerList[i].name = jsondata['ejere']['ejer' + abc[i] + '_selskabsnavn']
        else:
            ownerList[i].name = jsondata['ejere']['ejer' + abc[i] + '_navn']
        ownerList[i].cpr = jsondata['oplysninger']['ejer' + abc[i] + '_cpr']
        # If it is a company and CVR is not populated the we assume that we have open data
        if jsondata['ejere']['ejer' + abc[i] + '_navn'] == "" and jsondata['oplysninger']['ejer' + abc[i] + '_adresse'] == "":
            ownerList[i].cvr = jsondata['oplysninger']['ejer' + abc[i] + '_data_cvr']
            ownerList[i].adress = jsondata['oplysninger']['ejer' + abc[i] + '_data_adresse']
            ownerList[i].zipcode = jsondata['oplysninger']['ejer' + abc[i] + '_data_postnummer']
            ownerList[i].city = jsondata['oplysninger']['ejer' + abc[i] + '_data_by']
            ownerList[i].city = jsondata['oplysninger']['ejer' + abc[i] + '_data_land']
        else: 
            if jsondata['oplysninger']['ejer' + abc[i] + '_stiftelse'] == True and jsondata['oplysninger']['ejer' + abc[i] + '_cvr'] == "":
                ownerList[i].cvr = 'CVR-nummer mangler!'
            else:
                ownerList[i].cvr = jsondata['oplysninger']['ejer' + abc[i] + '_cvr']
            ownerList[i].adress = jsondata['oplysninger']['ejer' + abc[i] + '_adresse']
            ownerList[i].zipcode = jsondata['oplysninger']['ejer' + abc[i] + '_postnummer']
            ownerList[i].city = jsondata['oplysninger']['ejer' + abc[i] + '_by']
            if jsondata['oplysninger']['ejer' + abc[i] + '_land'] == 'DK':
                ownerList[i].country = 'Danmark'
            else:
                ownerList[i].country = jsondata['oplysninger']['ejer' + abc[i] + '_landenavn']
        #print(ownerList[i].__dict__)
        i+=1
    return ownerList

# Resolves an owner i.e. "ejerb" into an integer "1"
def OwnerNumber(data):
    n = 0
    letter = data[-1]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    for item in abc:
        if item == letter:
            numberonlist = n
        n+=1
    return numberonlist

def CreateManagement(jsondata, ownerList, boardList):
    managementList = ["executive1", "executive2", "executive3", "executive4", "executive4", "executive6", "executive7", "executive8", "executive9", "executive10"]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    # Looping through the CEOs
    while i < int(jsondata['medlemmerledelse']['valg_direktorer']):
        managementList[i] = Management("","","","","","","","","","")
        managementList[i].executive = True
        # Defaulting the board and chairman value to False
        managementList[i].board = False
        managementList[i].chairman = False
        # If executive is a known owner
        if jsondata['medlemmerledelse']['direktion_medlem' + abc[i] + '_navn'] == "":
            ownerletter = OwnerNumber(jsondata['medlemmerledelse']['direktion_medlem' + abc[i] + '_radio'])
            managementList[i].name = ownerList[ownerletter].name
            managementList[i].cpr = ownerList[ownerletter].cpr
            managementList[i].adress = ownerList[ownerletter].adress
            managementList[i].zipcode = ownerList[ownerletter].zipcode
            managementList[i].city = ownerList[ownerletter].city
            managementList[i].country = ownerList[ownerletter].country
        # If executive is a previous unknown person
        else:
            managementList[i].name = jsondata['medlemmerledelse']['direktion_medlem' + abc[i] + '_navn']
            managementList[i].cpr = jsondata['oplysninger']['direktion' + abc[i] + '_cpr']
            managementList[i].adress = jsondata['oplysninger']['direktion' + abc[i] + '_adresse']
            managementList[i].zipcode = jsondata['oplysninger']['direktion' + abc[i] + '_postnummer']
            managementList[i].city = jsondata['oplysninger']['direktion' + abc[i] + '_by']
            if jsondata['oplysninger']['direktion' + abc[i] + '_land'] == 'DK':
                managementList[i].country = 'Danmark'
            else:
                managementList[i].country = jsondata['oplysninger']['direktion' + abc[i] + '_landenavn']
        if i == 0 and int(jsondata['medlemmerledelse']['valg_direktorer']) > 1:
            managementList[i].president = True
        else:
            managementList[i].president = False
        i+=1

    # Creating list of names
    executiveNameList = []
    for item in managementList:
        try:
            executiveNameList.append(item.name)
        except:
            pass

    # Looping through the Board
    if jsondata['medlemmerledelse']['valg_bestyrelse'] != "":
        n = 0
        while n < int(jsondata['medlemmerledelse']['valg_bestyrelse']):
            # If know editing know entity
            if boardList[n].name in executiveNameList:
                numberInList = executiveNameList.index(boardList[n].name)
                managementList[numberInList].board = True
                managementList[numberInList].chairman = boardList[n].chairman
            # If unknow creating new entity
            else:
                
                managementList[i] = Management("","","","","","","","","","")
                managementList[i].name = boardList[n].name
                managementList[i].cpr = boardList[n].cpr
                managementList[i].adress = boardList[n].adress
                managementList[i].zipcode = boardList[n].zipcode
                managementList[i].city = boardList[n].city
                managementList[i].country = boardList[n].country
                managementList[i].chairman = boardList[n].chairman
                managementList[i].board = True
                managementList[i].executive = False
                managementList[i].president = False
                i+=1
            n+=1

    # Removed all items that are strings and thus not instances of a class
    managementList = [x for x in managementList if not isinstance(x, str)]

    return managementList

def CreateBoard(jsondata, ownerList):
    boardList = ["boardmember1", "boardmember2", "boardmember3", "boardmember4", "boardmember5", "boardmember6"]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    if jsondata['medlemmerledelse']['valg_bestyrelse'] != "":
        while i < int(jsondata['medlemmerledelse']['valg_bestyrelse']):
            boardList[i] = Board("","","","","","","")
            if jsondata['medlemmerledelse']['bestyrelse_medlema_navn'] == "":
                ownerletter = OwnerNumber(jsondata['medlemmerledelse']['bestyrelse_medlem' + abc[i] + '_radio'])
                boardList[i].name = ownerList[ownerletter].name
                boardList[i].cpr = ownerList[ownerletter].cpr
                boardList[i].adress = ownerList[ownerletter].adress
                boardList[i].zipcode = ownerList[ownerletter].zipcode
                boardList[i].city = ownerList[ownerletter].city
                boardList[i].country = ownerList[ownerletter].country
            else:
                boardList[i].name = jsondata['medlemmerledelse']['bestyrelse_medlem' + abc[i] + '_navn']
                boardList[i].cpr = jsondata['oplysninger']['bestyrelse' + abc[i] + '_cpr']
                boardList[i].adress = jsondata['oplysninger']['bestyrelse' + abc[i] + '_adresse']
                boardList[i].zipcode = jsondata['oplysninger']['bestyrelse' + abc[i] + '_postnummer']
                boardList[i].city = jsondata['oplysninger']['bestyrelse' + abc[i] + '_by']
                if jsondata['oplysninger']['bestyrelse' + abc[i] + '_land'] == 'DK':
                    boardList[i].country = 'Danmark'
                else:
                    boardList[i].country = jsondata['oplysninger']['bestyrelse' + abc[i] + '_landenavn']
            if i == 0 and int(jsondata['medlemmerledelse']['valg_bestyrelse']) > 1:
                boardList[i].chairman = True
            else:
                boardList[i].chairman = False
            #print(boardList[i].__dict__)
            i+=1
    return boardList

def CreateCompany(jsondata, ownerList):
    # Instatiate the class
    company = Company("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    abc = ["a", "b", "c", "d", "e", "f", "g"]

    # Name and type
    company.name = jsondata['navn']['navn_navn']
    company.companytype = jsondata['type']['radio_radio']

    company.secondaryName = []
    i = 0
    if jsondata['navn']['binavn_antal'] != "":
        while i < int(jsondata['navn']['binavn_antal']):
            company.secondaryName.append(jsondata['navn']['binavn' + abc[i] + '_binavn'] + ' ' + company.companytype)
            i+=1

    # Company adress
    if jsondata['selskabsoplysninger']['selskab_gadenavn'] == "":
        ownerletter = OwnerNumber(jsondata['selskabsoplysninger']['selskab_radio'])
        company.adress = ownerList[ownerletter].adress
        company.zipcode = ownerList[ownerletter].zipcode
        company.city = ownerList[ownerletter].city
        company.country = ownerList[ownerletter].country
    else:
        company.adress = jsondata['selskabsoplysninger']['selskab_gadenavn']
        company.adress2 = jsondata['selskabsoplysninger']['selskab_adresse2']
        company.zipcode = jsondata['selskabsoplysninger']['selskab_postnummer']
        company.city = jsondata['selskabsoplysninger']['selskab_by']

    # We create validated adress
    company.validateadress = ValidateAdress(company.adress + ", " + company.zipcode + " " + company.city)
    # email and advertising protection
    company.email = jsondata['selskabsoplysninger']['valgfri_mail']
    company.advertising = jsondata['branche']['reklamebeskyttelse_ja']
    
    # signing and date of effect
    if jsondata['startdato']['dato_radio'] == 'nu':
        company.signingDate = jsondata['startdato']['dato_dagsdato']
        company.effectDate = jsondata['startdato']['dato_dagsdato']
    else:
        company.signingDate = jsondata['startdato']['dato_dagsdato']
        company.effectDate = jsondata['startdato']['dato_dato']

    # Company purpose
    if jsondata['formaal']['formaal_radio'] == 'generel':
        company.purpose = "Selskabets formål er at udøve virksomhed med handel og service samt aktiviteter i tilknytning hertil."
    elif jsondata['formaal']['formaal_radio'] == 'holding':
        company.purpose = "Selskabets formål er at eje ejerandele i andre selskaber samt andre investeringer efter ledelsens skøn."
    else:
        company.purpose = jsondata['formaal']['formaal_formaal']

    # Tegningsregel
    company.powertobind = CreatePowerToBind(jsondata)

    # Industry code
    if jsondata['formaal']['formaal_radio'] == 'holding':
        company.industrycode = '64.20.20'
    else:
        industry = jsondata['branche']['branche_branche']
        if len(re.findall(r'\d{6}', industry)) > 0:
            company.industrycode = re.findall(r'\d{6}', industry)[0]
        if len(re.findall(r'\b\d{2}\.\d{2}\.\d{2}\b', industry)) > 0:
            company.industrycode = re.findall(r'\b\d{2}\.\d{2}\.\d{2}\b', industry)[0]

    # Company capital
    capital = 0
    i = 0
    while i < int(jsondata['ejere']['antalejer_radio']):
        capital = capital + int(jsondata['kapital']['ejer' + abc[i] + '_nominel'])
        i+=1
    company.capital = capital

    # Fiscal year
    numberOfDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    company.fiscalstart = "01-" + "{:02d}".format(int(jsondata['arsrapport']['regnskabsaar_maaned']))
    end = (int(jsondata['arsrapport']['regnskabsaar_maaned']) - 13)*-1
    company.fiscalend = str(numberOfDays[end - 1]) + "-" + str(end) 

    # Accountant
    if jsondata['arsrapport']['revisor_radio'] == "nej":
        company.audited = False
    else:
        company.audited = True
        company.accountantname = jsondata['arsrapport']['revisor_navn']
        company.accountantcvr = jsondata['arsrapport']['revisor_cvr']

    # VAT / Lonsum    
    try:
        if jsondata['moms']['moms_begge_begge'] == True:
            moms_begge = True
        else:
            moms_begge = False
    except:
        moms_begge = False


    if moms_begge == True:
        company.vat = True
        company.lonsum = True
    elif jsondata['moms']['moms_radio'] == 'Moms':
        company.vat = True
        company.lonsum = False
    elif jsondata['moms']['moms_radio'] == 'Lønsum':
        company.vat = False
        company.lonsum = True
    
    # Imports / Exports
    company.imports = False
    company.exports = False
    if jsondata['branche']['import_import'] == True:
        company.imports = True
    if jsondata['branche']['import_eksport'] == True:
        company.exports = True

    # Employees
    if jsondata['medarbejdere']['medarbejdere_radio'] == 'nej':
        company.numberemployees = 0
    if jsondata['medarbejdere']['medarbejdere_radio'] == 'ja':
        company.numberemployees = jsondata['medarbejdere']['medarbejdere_antal_radio']
        if jsondata['medarbejdere']['medarbejdere_omfang'] == 'nej':
            company.more_than_nine = False
        if jsondata['medarbejdere']['medarbejdere_omfang'] == 'ja':
            company.more_than_nine = True

    print(company.__dict__)
    return company

def CreatePowerToBind(jsondata):
    provision = ""
    if jsondata['typeledelse']['entostrenget_radio'] == "direktion" and jsondata['medlemmerledelse']['valg_direktorer'] == "1":
        provision = "Selskabet tegnes af en direktør."

    if jsondata['tegningsret']['direktion_vanskeligt_to'] == "endirektor" or jsondata['tegningsret']['direktion_vanskeligt_flere'] == "endirektor":
        provision = "Selskabet tegnes af en direktør."

    if jsondata['tegningsret']['direktion_vanskeligt_to'] == "todirektorer" or jsondata['tegningsret']['direktion_vanskeligt_flere'] == "todirektorer":
        provision = "Selskabet tegnes af 2 direktører i forening."

    if jsondata['tegningsret']['direktion_vanskeligt_flere'] == "samtlige":
        provision = "Selskabet tegnes af den samlede direktion."

    if jsondata['tegningsret']['bestyrelse_endirektor'] == "et":
        provision = "Selskabet tegnes af bestyrelsens formand i forening med en direktør."
    
    if jsondata['tegningsret']['bestyrelse_endirektor'] == "to":
        provision = "Selskabet tegnes af to bestyrelsesmedlemmer i forening."

    if jsondata['tegningsret']['bestyrelse_endirektor'] == "tre":
        provision = "Selskabet tegnes af den samlede bestyrelse."
    return provision

def ValidateAdress(adress):
    url = 'https://dawa.aws.dk/datavask/adresser?betegnelse=' + adress
    response = requests.get(url)
    jsondata = json.loads(response.content, strict=False)
    jsonpath = jsondata['resultater'][0]['vaskeresultat']['variant']
    validatedadress = jsonpath['vejnavn'] + ' ' + jsonpath['husnr'] 
    if jsonpath['etage'] != None:
        validatedadress = validatedadress + ', ' + jsonpath['etage']
    if jsonpath['dør'] != None:
        validatedadress = validatedadress + ' ' + jsonpath['dør']
    validatedadress = validatedadress + ', ' + jsonpath['postnr'] + ' ' + jsonpath['postnrnavn']
    return validatedadress