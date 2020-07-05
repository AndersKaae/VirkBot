import json
import re

class Company:
  def __init__(self, name, companytype, secondaryName, adress, adress2, zipcode, city, email, advertising, signingDate, effectDate, purpose, powertobind, industrycode, capital, fiscalstart, fiscalend, audited, accountantname, accountantcvr):
    self.name = name
    self.companytype = companytype
    self.secondaryName = secondaryName
    self.adress = adress
    self.adress2 = adress2
    self.zipcode = zipcode
    self.city = city
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
    company = Company("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
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
        company.country = jsondata['selskabsoplysninger']['selskab_by']

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
    
    #print(company.__dict__)
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

JsonParser('{"introduktion":{"type_parameter":"","type_id":"ApS"},"type":{"radio_radio":"ApS"},"navn":{"navn_navn":"Nordic Eye Institute","binavn_radio":"ja","binavn_antal":"1","binavna_binavn":"Øjenklinik CPH","binavnb_binavn":"","binavnc_binavn":"","binavnd_binavn":"","binavne_binavn":""},"formaal":{"formaal_radio":"generel","formaal_formaal":""},"ejere":{"antalejer_radio":"3","ejera_type":"person","ejera_navn":"Srdjan Zelenbabic","ejera_selskabsnavn":"","ejerb_type":"person","ejerb_navn":"Mohammed Kashaf Farooq","ejerb_selskabsnavn":"","ejerc_type":"person","ejerc_navn":"Francisco Javier Cabrerizo Nuñez","ejerc_selskabsnavn":"","ejerd_type":"","ejerd_navn":"","ejerd_selskabsnavn":"","ejere_type":"","ejere_navn":"","ejere_selskabsnavn":"","ejerf_type":"","ejerf_navn":"","ejerf_selskabsnavn":""},"kapital":{"ejera_nominel":"14000","ejerb_nominel":"14000","ejerc_nominel":"14000","ejerd_nominel":"","ejere_nominel":"","ejerf_nominel":""},"typeledelse":{"entostrenget_radio":"direktion"},"medlemmerledelse":{"valg_direktorer":"3","valg_bestyrelse":"","direktion_medlema_radio":"ejerc","direktion_medlema_navn":"","direktion_medlemb_radio":"ejerb","direktion_medlemb_navn":"","direktion_medlemc_radio":"ejera","direktion_medlemc_navn":"","direktion_medlemd_radio":"","direktion_medlemd_navn":"","bestyrelse_medlema_radio":"","bestyrelse_medlema_navn":"","bestyrelse_medlemb_radio":"","bestyrelse_medlemb_navn":"","bestyrelse_medlemc_radio":"","bestyrelse_medlemc_navn":"","bestyrelse_medlemd_radio":"","bestyrelse_medlemd_navn":"","bestyrelse_medleme_radio":"","bestyrelse_medleme_navn":"","bestyrelse_medlemf_radio":"","bestyrelse_medlemf_navn":""},"tegningsret":{"direktion_vanskeligt_to":"","direktion_vanskeligt_flere":"samtlige","bestyrelse_endirektor":""},"arsrapport":{"regnskabsaar_maaned":"1","revisor_radio":"nej","revisor_navn":"","revisor_cvr":""},"startdato":{"dato_radio":"nu","dato_dagsdato":"02.07.2020","dato_dato":""},"selskabsregistrering":{"registrering_radio":"ja"},"oplysninger":{"ejera_cpr":"240280-3447","ejera_cvr":"","ejera_stiftelse":"","ejera_adresse":"Ordrupvej 100, 2.th","ejera_postnummer":"2920","ejera_by":"Charlottenlund","ejera_land":"DK","ejera_landenavn":"","ejera_reel_radio":"","ejera_reel_reel1_radio":"","ejera_reel_reel1_navn":"","ejera_reel_reel1_cpr":"","ejera_reel_reel1_adresse":"","ejera_reel_reel1_postnummer":"","ejera_reel_reel1_by":"","ejera_reel_reel1_land":"DK","ejera_reel_reel1_landenavn":"","ejera_reel_reel2_radio":"","ejera_reel_reel2_navn":"","ejera_reel_reel2_cpr":"","ejera_reel_reel2_adresse":"","ejera_reel_reel2_postnummer":"","ejera_reel_reel2_by":"","ejera_reel_reel2_land":"DK","ejera_reel_reel2_landenavn":"","ejera_reel_reel3_radio":"","ejera_reel_reel3_navn":"","ejera_reel_reel3_cpr":"","ejera_reel_reel3_adresse":"","ejera_reel_reel3_postnummer":"","ejera_reel_reel3_by":"","ejera_reel_reel3_land":"DK","ejera_reel_reel3_landenavn":"","ejera_data_cvr":"","ejera_data_adresse":"","ejera_data_postnummer":"","ejera_data_by":"","ejera_data_land":"","ejerb_cpr":"181177-2379","ejerb_cvr":"","ejerb_stiftelse":"","ejerb_adresse":"Horsbred 156","ejerb_postnummer":"2625","ejerb_by":"Vallensbæk","ejerb_land":"DK","ejerb_landenavn":"","ejerb_reel_radio":"","ejerb_reel_reel1_radio":"","ejerb_reel_reel1_navn":"","ejerb_reel_reel1_cpr":"","ejerb_reel_reel1_adresse":"","ejerb_reel_reel1_postnummer":"","ejerb_reel_reel1_by":"","ejerb_reel_reel1_land":"DK","ejerb_reel_reel1_landenavn":"","ejerb_reel_reel2_radio":"","ejerb_reel_reel2_navn":"","ejerb_reel_reel2_cpr":"","ejerb_reel_reel2_adresse":"","ejerb_reel_reel2_postnummer":"","ejerb_reel_reel2_by":"","ejerb_reel_reel2_land":"DK","ejerb_reel_reel2_landenavn":"","ejerb_reel_reel3_radio":"","ejerb_reel_reel3_navn":"","ejerb_reel_reel3_cpr":"","ejerb_reel_reel3_adresse":"","ejerb_reel_reel3_postnummer":"","ejerb_reel_reel3_by":"","ejerb_reel_reel3_land":"DK","ejerb_reel_reel3_landenavn":"","ejerb_data_cvr":"","ejerb_data_adresse":"","ejerb_data_postnummer":"","ejerb_data_by":"","ejerb_data_land":"","ejerc_cpr":"081282-3671","ejerc_cvr":"","ejerc_stiftelse":"","ejerc_adresse":"Gråstensgade 6, 1.tv","ejerc_postnummer":"1677","ejerc_by":"København V","ejerc_land":"DK","ejerc_landenavn":"","ejerc_reel_radio":"","ejerc_reel_reel1_radio":"","ejerc_reel_reel1_navn":"","ejerc_reel_reel1_cpr":"","ejerc_reel_reel1_adresse":"","ejerc_reel_reel1_postnummer":"","ejerc_reel_reel1_by":"","ejerc_reel_reel1_land":"DK","ejerc_reel_reel1_landenavn":"","ejerc_reel_reel2_radio":"","ejerc_reel_reel2_navn":"","ejerc_reel_reel2_cpr":"","ejerc_reel_reel2_adresse":"","ejerc_reel_reel2_postnummer":"","ejerc_reel_reel2_by":"","ejerc_reel_reel2_land":"DK","ejerc_reel_reel2_landenavn":"","ejerc_reel_reel3_radio":"","ejerc_reel_reel3_navn":"","ejerc_reel_reel3_cpr":"","ejerc_reel_reel3_adresse":"","ejerc_reel_reel3_postnummer":"","ejerc_reel_reel3_by":"","ejerc_reel_reel3_land":"DK","ejerc_reel_reel3_landenavn":"","ejerc_data_cvr":"","ejerc_data_adresse":"","ejerc_data_postnummer":"","ejerc_data_by":"","ejerc_data_land":"","ejerd_cpr":"","ejerd_cvr":"","ejerd_stiftelse":"","ejerd_adresse":"","ejerd_postnummer":"","ejerd_by":"","ejerd_land":"DK","ejerd_landenavn":"","ejerd_reel_radio":"","ejerd_reel_reel1_radio":"","ejerd_reel_reel1_navn":"","ejerd_reel_reel1_cpr":"","ejerd_reel_reel1_adresse":"","ejerd_reel_reel1_postnummer":"","ejerd_reel_reel1_by":"","ejerd_reel_reel1_land":"DK","ejerd_reel_reel1_landenavn":"","ejerd_reel_reel2_radio":"","ejerd_reel_reel2_navn":"","ejerd_reel_reel2_cpr":"","ejerd_reel_reel2_adresse":"","ejerd_reel_reel2_postnummer":"","ejerd_reel_reel2_by":"","ejerd_reel_reel2_land":"DK","ejerd_reel_reel2_landenavn":"","ejerd_reel_reel3_radio":"","ejerd_reel_reel3_navn":"","ejerd_reel_reel3_cpr":"","ejerd_reel_reel3_adresse":"","ejerd_reel_reel3_postnummer":"","ejerd_reel_reel3_by":"","ejerd_reel_reel3_land":"DK","ejerd_reel_reel3_landenavn":"","ejerd_data_cvr":"","ejerd_data_adresse":"","ejerd_data_postnummer":"","ejerd_data_by":"","ejerd_data_land":"","ejere_cpr":"","ejere_cvr":"","ejere_stiftelse":"","ejere_adresse":"","ejere_postnummer":"","ejere_by":"","ejere_land":"DK","ejere_landenavn":"","ejere_reel_radio":"","ejere_reel_reel1_radio":"","ejere_reel_reel1_navn":"","ejere_reel_reel1_cpr":"","ejere_reel_reel1_adresse":"","ejere_reel_reel1_postnummer":"","ejere_reel_reel1_by":"","ejere_reel_reel1_land":"DK","ejere_reel_reel1_landenavn":"","ejere_reel_reel2_radio":"","ejere_reel_reel2_navn":"","ejere_reel_reel2_cpr":"","ejere_reel_reel2_adresse":"","ejere_reel_reel2_postnummer":"","ejere_reel_reel2_by":"","ejere_reel_reel2_land":"DK","ejere_reel_reel2_landenavn":"","ejere_reel_reel3_radio":"","ejere_reel_reel3_navn":"","ejere_reel_reel3_cpr":"","ejere_reel_reel3_adresse":"","ejere_reel_reel3_postnummer":"","ejere_reel_reel3_by":"","ejere_reel_reel3_land":"DK","ejere_reel_reel3_landenavn":"","ejere_data_cvr":"","ejere_data_adresse":"","ejere_data_postnummer":"","ejere_data_by":"","ejere_data_land":"","ejerf_cpr":"","ejerf_cvr":"","ejerf_stiftelse":"","ejerf_adresse":"","ejerf_postnummer":"","ejerf_by":"","ejerf_land":"DK","ejerf_landenavn":"","ejerf_reel_radio":"","ejerf_reel_reel1_radio":"","ejerf_reel_reel1_navn":"","ejerf_reel_reel1_cpr":"","ejerf_reel_reel1_adresse":"","ejerf_reel_reel1_postnummer":"","ejerf_reel_reel1_by":"","ejerf_reel_reel1_land":"DK","ejerf_reel_reel1_landenavn":"","ejerf_reel_reel2_radio":"","ejerf_reel_reel2_navn":"","ejerf_reel_reel2_cpr":"","ejerf_reel_reel2_adresse":"","ejerf_reel_reel2_postnummer":"","ejerf_reel_reel2_by":"","ejerf_reel_reel2_land":"DK","ejerf_reel_reel2_landenavn":"","ejerf_reel_reel3_radio":"","ejerf_reel_reel3_navn":"","ejerf_reel_reel3_cpr":"","ejerf_reel_reel3_adresse":"","ejerf_reel_reel3_postnummer":"","ejerf_reel_reel3_by":"","ejerf_reel_reel3_land":"DK","ejerf_reel_reel3_landenavn":"","ejerf_data_cvr":"","ejerf_data_adresse":"","ejerf_data_postnummer":"","ejerf_data_by":"","ejerf_data_land":"","direktiona_cpr":"","direktiona_adresse":"","direktiona_postnummer":"","direktiona_by":"","direktiona_land":"DK","direktiona_landenavn":"","direktionb_cpr":"","direktionb_adresse":"","direktionb_postnummer":"","direktionb_by":"","direktionb_land":"DK","direktionb_landenavn":"","direktionc_cpr":"","direktionc_adresse":"","direktionc_postnummer":"","direktionc_by":"","direktionc_land":"DK","direktionc_landenavn":"","direktiond_cpr":"","direktiond_adresse":"","direktiond_postnummer":"","direktiond_by":"","direktiond_land":"DK","direktiond_landenavn":"","bestyrelsea_cpr":"","bestyrelsea_adresse":"","bestyrelsea_postnummer":"","bestyrelsea_by":"","bestyrelsea_land":"DK","bestyrelsea_landenavn":"","bestyrelseb_cpr":"","bestyrelseb_adresse":"","bestyrelseb_postnummer":"","bestyrelseb_by":"","bestyrelseb_land":"DK","bestyrelseb_landenavn":"","bestyrelsec_cpr":"","bestyrelsec_adresse":"","bestyrelsec_postnummer":"","bestyrelsec_by":"","bestyrelsec_land":"DK","bestyrelsec_landenavn":"","bestyrelsed_cpr":"","bestyrelsed_adresse":"","bestyrelsed_postnummer":"","bestyrelsed_by":"","bestyrelsed_land":"DK","bestyrelsed_landenavn":"","bestyrelsee_cpr":"","bestyrelsee_adresse":"","bestyrelsee_postnummer":"","bestyrelsee_by":"","bestyrelsee_land":"DK","bestyrelsee_landenavn":"","bestyrelsef_cpr":"","bestyrelsef_adresse":"","bestyrelsef_postnummer":"","bestyrelsef_by":"","bestyrelsef_land":"DK","bestyrelsef_landenavn":""},"medarbejdere":{"medarbejdere_radio":"nej","medarbejdere_antal_radio":"","medarbejdere_omfang":""},"branche":{"branche_branche":"Privat Hospital","reklamebeskyttelse_ja":true,"alkohol_bevilling":"","import_import":false,"import_eksport":""},"moms":{"moms_radio":"Lønsum","moms_begge_begge":false},"selskabsoplysninger":{"selskab_radio":"ejerc","selskab_gadenavn":"","selskab_adresse2":"","selskab_postnummer":"","selskab_by":"","selskab_tlf":"","selskab_mail":"","valgfri_tlf":"","valgfri_mail":""},"underskrift":{"ejera_radio":"","ejera_underskriver1_radio":"","ejera_underskriver1_underskriv":"","ejera_underskriver2_radio":"","ejera_underskriver2_underskriv":"","ejerb_radio":"","ejerb_underskriver1_radio":"","ejerb_underskriver1_underskriv":"","ejerb_underskriver2_radio":"","ejerb_underskriver2_underskriv":"","ejerc_radio":"","ejerc_underskriver1_radio":"","ejerc_underskriver1_underskriv":"","ejerc_underskriver2_radio":"","ejerc_underskriver2_underskriv":"","ejerd_radio":"","ejerd_underskriver1_radio":"","ejerd_underskriver1_underskriv":"","ejerd_underskriver2_radio":"","ejerd_underskriver2_underskriv":"","ejere_radio":"","ejere_underskriver1_radio":"","ejere_underskriver1_underskriv":"","ejere_underskriver2_radio":"","ejere_underskriver2_underskriv":"","ejerf_radio":"","ejerf_underskriver1_radio":"","ejerf_underskriver1_underskriv":"","ejerf_underskriver2_radio":"","ejerf_underskriver2_underskriv":""},"afslut":{}}')