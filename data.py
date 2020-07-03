import json

class Company:
  def __init__(self, name, companytype, secondaryName, adress, adress2, zipcode, city, email, advertising, signingDate, effectDate, purpose, powertobind, industrycode, capital, fiscalstart, fiscalend):
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

class Executive:
    def __init__(self, name, cpr, adress, zipcode, city, country, president):
        self.name = name
        self.cpr = cpr
        self.adress = adress
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.president = president

class Board:
    def __init__(self, name, cpr, adress, zipcode, city, country, president):
        self.name = name
        self.cpr = cpr
        self.adress = adress
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.president = president


def JsonParser(data):
    # Parse JSON data
    jsondata = json.loads(data, strict=False)
        
    # Create owners
    legalOwnerList = CreateLegalOwners(jsondata)

    # Create management
    executiveList = CreateExecutive(jsondata, ownerList)

    # Create company
    company = CreateCompany(jsondata, legalOwnerList)



    return legalOwnerList, company

def CreateLegalOwners(jsondata):
    ownerList = ["owner1", "owner2", "owner3", "owner4", "owner5", "owner6"]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    while i < int(jsondata['ejere']['antalejer_radio']):
        ownerList[i] = LegalOwner("", "", "", "", "", "", "")
        ownerList[i].name = jsondata['ejere']['ejer' + abc[i] + '_navn']
        ownerList[i].cpr = jsondata['oplysninger']['ejer' + abc[i] + '_cpr']
        ownerList[i].cvr = jsondata['oplysninger']['ejer' + abc[i] + '_cvr']
        ownerList[i].adress = jsondata['oplysninger']['ejer' + abc[i] + '_adresse']
        ownerList[i].zipcode = jsondata['oplysninger']['ejer' + abc[i] + '_postnummer']
        ownerList[i].city = jsondata['oplysninger']['ejer' + abc[i] + '_by']
        ownerList[i].country = jsondata['oplysninger']['ejer' + abc[i] + '_land']
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

def CreateExecutive(jsondata, ownerList):
    executiveList = ["executive1", "executive2", "executive3", "executive4"]
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    while i < int(jsondata['medlemmerledelse']['valg_direktorer']):
        executiveList[i] = Executive("","","","","","","")
        if jsondata['medlemmerledelse']['direktion_medlema_navn'] == "":
            ownerletter = OwnerNumber(jsondata['medlemmerledelse']['direktion_medlem' + abc[i] + '_radio'])
            executiveList[i].name = ownerList[ownerletter].name
            executiveList[i].cpr = ownerList[ownerletter].cpr
            executiveList[i].adress = ownerList[ownerletter].adress
    i+=1

def CreateCompany(jsondata, ownerList):
    # Instatiate the class
    company = Company("", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "")
    
    # Name and type
    company.name = jsondata['navn']['navn_navn']
    company.companytype = jsondata['type']['radio_radio']

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
        company.signingDate = jsondata['startdato']['dato_radio']
        company.effectDate = jsondata['startdato']['dato_radio']
    else:
        company.signingDate = jsondata['startdato']['dato_radio']
        company.effectDate = jsondata['startdato']['dato_dato']

    # Company purpose
    if jsondata['formaal']['formaal_radio'] == 'generel':
        company.purpose = "Selskabets formål er at udøve virksomhed med handel og service samt aktiviteter i tilknytning hertil."
    else:
        company.purpose = jsondata['formaal']['formaal_formaal']

    # Tegningsregel
    company.powertobind = 'MISSING'

    # Industry code
    company.industrycode = jsondata['branche']['branche_branche']

    # Company capital
    capital = []
    abc = ["a", "b", "c", "d", "e", "f", "g"]
    i = 0
    while i < int(jsondata['ejere']['antalejer_radio']):
        capital.append(jsondata['kapital']['ejer' + abc[i] + '_nominel'])
        i+=1
    company.capital = capital

    # Fiscal year
    numberOfDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    company.fiscalstart = "01-" + "{:02d}".format(int(jsondata['arsrapport']['regnskabsaar_maaned']))
    end = (int(jsondata['arsrapport']['regnskabsaar_maaned']) - 13)*-1
    company.fiscalend = str(numberOfDays[end - 1]) + "-" + str(end) 

    #print(company.__dict__)
    return company

JsonParser('{"introduktion":{"type_parameter":"","type_id":"ApS"},"type":{"radio_radio":"ApS"},"navn":{"navn_navn":"Nitro rengøring","binavn_radio":"nej","binavn_antal":"","binavna_binavn":"Fake Binavn","binavnb_binavn":"","binavnc_binavn":"","binavnd_binavn":"","binavne_binavn":""},"formaal":{"formaal_radio":"generel","formaal_formaal":""},"ejere":{"antalejer_radio":"1","ejera_type":"person","ejera_navn":"Dennis Bjernemose","ejera_selskabsnavn":"","ejerb_type":"","ejerb_navn":"","ejerb_selskabsnavn":"","ejerc_type":"","ejerc_navn":"","ejerc_selskabsnavn":"","ejerd_type":"","ejerd_navn":"","ejerd_selskabsnavn":"","ejere_type":"","ejere_navn":"","ejere_selskabsnavn":"","ejerf_type":"","ejerf_navn":"","ejerf_selskabsnavn":""},"kapital":{"ejera_nominel":"40000","ejerb_nominel":"","ejerc_nominel":"","ejerd_nominel":"","ejere_nominel":"","ejerf_nominel":""},"typeledelse":{"entostrenget_radio":"direktion"},"medlemmerledelse":{"valg_direktorer":"1","valg_bestyrelse":"","direktion_medlema_radio":"ejera","direktion_medlema_navn":"","direktion_medlemb_radio":"","direktion_medlemb_navn":"","direktion_medlemc_radio":"","direktion_medlemc_navn":"","direktion_medlemd_radio":"","direktion_medlemd_navn":"","bestyrelse_medlema_radio":"","bestyrelse_medlema_navn":"","bestyrelse_medlemb_radio":"","bestyrelse_medlemb_navn":"","bestyrelse_medlemc_radio":"","bestyrelse_medlemc_navn":"","bestyrelse_medlemd_radio":"","bestyrelse_medlemd_navn":"","bestyrelse_medleme_radio":"","bestyrelse_medleme_navn":"","bestyrelse_medlemf_radio":"","bestyrelse_medlemf_navn":""},"tegningsret":{"direktion_vanskeligt_to":"","direktion_vanskeligt_flere":"","bestyrelse_endirektor":""},"arsrapport":{"regnskabsaar_maaned":"1","revisor_radio":"nej","revisor_navn":"","revisor_cvr":""},"startdato":{"dato_radio":"nu","dato_dagsdato":"02.07.2020","dato_dato":""},"selskabsregistrering":{"registrering_radio":"ja"},"oplysninger":{"ejera_cpr":"210571-2629","ejera_cvr":"","ejera_stiftelse":"","ejera_adresse":"Rentemestervej 9E, ST TV","ejera_postnummer":"2400","ejera_by":"København NV","ejera_land":"DK","ejera_landenavn":"","ejera_reel_radio":"","ejera_reel_reel1_radio":"","ejera_reel_reel1_navn":"","ejera_reel_reel1_cpr":"","ejera_reel_reel1_adresse":"","ejera_reel_reel1_postnummer":"","ejera_reel_reel1_by":"","ejera_reel_reel1_land":"DK","ejera_reel_reel1_landenavn":"","ejera_reel_reel2_radio":"","ejera_reel_reel2_navn":"","ejera_reel_reel2_cpr":"","ejera_reel_reel2_adresse":"","ejera_reel_reel2_postnummer":"","ejera_reel_reel2_by":"","ejera_reel_reel2_land":"DK","ejera_reel_reel2_landenavn":"","ejera_reel_reel3_radio":"","ejera_reel_reel3_navn":"","ejera_reel_reel3_cpr":"","ejera_reel_reel3_adresse":"","ejera_reel_reel3_postnummer":"","ejera_reel_reel3_by":"","ejera_reel_reel3_land":"DK","ejera_reel_reel3_landenavn":"","ejera_data_cvr":"","ejera_data_adresse":"","ejera_data_postnummer":"","ejera_data_by":"","ejera_data_land":"","ejerb_cpr":"","ejerb_cvr":"","ejerb_stiftelse":"","ejerb_adresse":"","ejerb_postnummer":"","ejerb_by":"","ejerb_land":"DK","ejerb_landenavn":"","ejerb_reel_radio":"","ejerb_reel_reel1_radio":"","ejerb_reel_reel1_navn":"","ejerb_reel_reel1_cpr":"","ejerb_reel_reel1_adresse":"","ejerb_reel_reel1_postnummer":"","ejerb_reel_reel1_by":"","ejerb_reel_reel1_land":"DK","ejerb_reel_reel1_landenavn":"","ejerb_reel_reel2_radio":"","ejerb_reel_reel2_navn":"","ejerb_reel_reel2_cpr":"","ejerb_reel_reel2_adresse":"","ejerb_reel_reel2_postnummer":"","ejerb_reel_reel2_by":"","ejerb_reel_reel2_land":"DK","ejerb_reel_reel2_landenavn":"","ejerb_reel_reel3_radio":"","ejerb_reel_reel3_navn":"","ejerb_reel_reel3_cpr":"","ejerb_reel_reel3_adresse":"","ejerb_reel_reel3_postnummer":"","ejerb_reel_reel3_by":"","ejerb_reel_reel3_land":"DK","ejerb_reel_reel3_landenavn":"","ejerb_data_cvr":"","ejerb_data_adresse":"","ejerb_data_postnummer":"","ejerb_data_by":"","ejerb_data_land":"","ejerc_cpr":"","ejerc_cvr":"","ejerc_stiftelse":"","ejerc_adresse":"","ejerc_postnummer":"","ejerc_by":"","ejerc_land":"DK","ejerc_landenavn":"","ejerc_reel_radio":"","ejerc_reel_reel1_radio":"","ejerc_reel_reel1_navn":"","ejerc_reel_reel1_cpr":"","ejerc_reel_reel1_adresse":"","ejerc_reel_reel1_postnummer":"","ejerc_reel_reel1_by":"","ejerc_reel_reel1_land":"DK","ejerc_reel_reel1_landenavn":"","ejerc_reel_reel2_radio":"","ejerc_reel_reel2_navn":"","ejerc_reel_reel2_cpr":"","ejerc_reel_reel2_adresse":"","ejerc_reel_reel2_postnummer":"","ejerc_reel_reel2_by":"","ejerc_reel_reel2_land":"DK","ejerc_reel_reel2_landenavn":"","ejerc_reel_reel3_radio":"","ejerc_reel_reel3_navn":"","ejerc_reel_reel3_cpr":"","ejerc_reel_reel3_adresse":"","ejerc_reel_reel3_postnummer":"","ejerc_reel_reel3_by":"","ejerc_reel_reel3_land":"DK","ejerc_reel_reel3_landenavn":"","ejerc_data_cvr":"","ejerc_data_adresse":"","ejerc_data_postnummer":"","ejerc_data_by":"","ejerc_data_land":"","ejerd_cpr":"","ejerd_cvr":"","ejerd_stiftelse":"","ejerd_adresse":"","ejerd_postnummer":"","ejerd_by":"","ejerd_land":"DK","ejerd_landenavn":"","ejerd_reel_radio":"","ejerd_reel_reel1_radio":"","ejerd_reel_reel1_navn":"","ejerd_reel_reel1_cpr":"","ejerd_reel_reel1_adresse":"","ejerd_reel_reel1_postnummer":"","ejerd_reel_reel1_by":"","ejerd_reel_reel1_land":"DK","ejerd_reel_reel1_landenavn":"","ejerd_reel_reel2_radio":"","ejerd_reel_reel2_navn":"","ejerd_reel_reel2_cpr":"","ejerd_reel_reel2_adresse":"","ejerd_reel_reel2_postnummer":"","ejerd_reel_reel2_by":"","ejerd_reel_reel2_land":"DK","ejerd_reel_reel2_landenavn":"","ejerd_reel_reel3_radio":"","ejerd_reel_reel3_navn":"","ejerd_reel_reel3_cpr":"","ejerd_reel_reel3_adresse":"","ejerd_reel_reel3_postnummer":"","ejerd_reel_reel3_by":"","ejerd_reel_reel3_land":"DK","ejerd_reel_reel3_landenavn":"","ejerd_data_cvr":"","ejerd_data_adresse":"","ejerd_data_postnummer":"","ejerd_data_by":"","ejerd_data_land":"","ejere_cpr":"","ejere_cvr":"","ejere_stiftelse":"","ejere_adresse":"","ejere_postnummer":"","ejere_by":"","ejere_land":"DK","ejere_landenavn":"","ejere_reel_radio":"","ejere_reel_reel1_radio":"","ejere_reel_reel1_navn":"","ejere_reel_reel1_cpr":"","ejere_reel_reel1_adresse":"","ejere_reel_reel1_postnummer":"","ejere_reel_reel1_by":"","ejere_reel_reel1_land":"DK","ejere_reel_reel1_landenavn":"","ejere_reel_reel2_radio":"","ejere_reel_reel2_navn":"","ejere_reel_reel2_cpr":"","ejere_reel_reel2_adresse":"","ejere_reel_reel2_postnummer":"","ejere_reel_reel2_by":"","ejere_reel_reel2_land":"DK","ejere_reel_reel2_landenavn":"","ejere_reel_reel3_radio":"","ejere_reel_reel3_navn":"","ejere_reel_reel3_cpr":"","ejere_reel_reel3_adresse":"","ejere_reel_reel3_postnummer":"","ejere_reel_reel3_by":"","ejere_reel_reel3_land":"DK","ejere_reel_reel3_landenavn":"","ejere_data_cvr":"","ejere_data_adresse":"","ejere_data_postnummer":"","ejere_data_by":"","ejere_data_land":"","ejerf_cpr":"","ejerf_cvr":"","ejerf_stiftelse":"","ejerf_adresse":"","ejerf_postnummer":"","ejerf_by":"","ejerf_land":"DK","ejerf_landenavn":"","ejerf_reel_radio":"","ejerf_reel_reel1_radio":"","ejerf_reel_reel1_navn":"","ejerf_reel_reel1_cpr":"","ejerf_reel_reel1_adresse":"","ejerf_reel_reel1_postnummer":"","ejerf_reel_reel1_by":"","ejerf_reel_reel1_land":"DK","ejerf_reel_reel1_landenavn":"","ejerf_reel_reel2_radio":"","ejerf_reel_reel2_navn":"","ejerf_reel_reel2_cpr":"","ejerf_reel_reel2_adresse":"","ejerf_reel_reel2_postnummer":"","ejerf_reel_reel2_by":"","ejerf_reel_reel2_land":"DK","ejerf_reel_reel2_landenavn":"","ejerf_reel_reel3_radio":"","ejerf_reel_reel3_navn":"","ejerf_reel_reel3_cpr":"","ejerf_reel_reel3_adresse":"","ejerf_reel_reel3_postnummer":"","ejerf_reel_reel3_by":"","ejerf_reel_reel3_land":"DK","ejerf_reel_reel3_landenavn":"","ejerf_data_cvr":"","ejerf_data_adresse":"","ejerf_data_postnummer":"","ejerf_data_by":"","ejerf_data_land":"","direktiona_cpr":"","direktiona_adresse":"","direktiona_postnummer":"","direktiona_by":"","direktiona_land":"DK","direktiona_landenavn":"","direktionb_cpr":"","direktionb_adresse":"","direktionb_postnummer":"","direktionb_by":"","direktionb_land":"DK","direktionb_landenavn":"","direktionc_cpr":"","direktionc_adresse":"","direktionc_postnummer":"","direktionc_by":"","direktionc_land":"DK","direktionc_landenavn":"","direktiond_cpr":"","direktiond_adresse":"","direktiond_postnummer":"","direktiond_by":"","direktiond_land":"DK","direktiond_landenavn":"","bestyrelsea_cpr":"","bestyrelsea_adresse":"","bestyrelsea_postnummer":"","bestyrelsea_by":"","bestyrelsea_land":"DK","bestyrelsea_landenavn":"","bestyrelseb_cpr":"","bestyrelseb_adresse":"","bestyrelseb_postnummer":"","bestyrelseb_by":"","bestyrelseb_land":"DK","bestyrelseb_landenavn":"","bestyrelsec_cpr":"","bestyrelsec_adresse":"","bestyrelsec_postnummer":"","bestyrelsec_by":"","bestyrelsec_land":"DK","bestyrelsec_landenavn":"","bestyrelsed_cpr":"","bestyrelsed_adresse":"","bestyrelsed_postnummer":"","bestyrelsed_by":"","bestyrelsed_land":"DK","bestyrelsed_landenavn":"","bestyrelsee_cpr":"","bestyrelsee_adresse":"","bestyrelsee_postnummer":"","bestyrelsee_by":"","bestyrelsee_land":"DK","bestyrelsee_landenavn":"","bestyrelsef_cpr":"","bestyrelsef_adresse":"","bestyrelsef_postnummer":"","bestyrelsef_by":"","bestyrelsef_land":"DK","bestyrelsef_landenavn":""},"medarbejdere":{"medarbejdere_radio":"ja","medarbejdere_antal_radio":"1","medarbejdere_omfang":"ja"},"branche":{"branche_branche":"Almindelig rengøring i bygninger\n\n[81.21.00] - Branchen omfatter almindelig indvendig rengøring i bygninger.","reklamebeskyttelse_ja":true,"alkohol_bevilling":"","import_import":"","import_eksport":""},"moms":{"moms_radio":"Moms","moms_begge_begge":""},"selskabsoplysninger":{"selskab_radio":"ejera","selskab_gadenavn":"","selskab_adresse2":"","selskab_postnummer":"","selskab_by":"","selskab_tlf":"","selskab_mail":"","valgfri_tlf":"22118324","valgfri_mail":"dnnsbj@gmail.com"},"underskrift":{"ejera_radio":"","ejera_underskriver1_radio":"","ejera_underskriver1_underskriv":"","ejera_underskriver2_radio":"","ejera_underskriver2_underskriv":"","ejerb_radio":"","ejerb_underskriver1_radio":"","ejerb_underskriver1_underskriv":"","ejerb_underskriver2_radio":"","ejerb_underskriver2_underskriv":"","ejerc_radio":"","ejerc_underskriver1_radio":"","ejerc_underskriver1_underskriv":"","ejerc_underskriver2_radio":"","ejerc_underskriver2_underskriv":"","ejerd_radio":"","ejerd_underskriver1_radio":"","ejerd_underskriver1_underskriv":"","ejerd_underskriver2_radio":"","ejerd_underskriver2_underskriv":"","ejere_radio":"","ejere_underskriver1_radio":"","ejere_underskriver1_underskriv":"","ejere_underskriver2_radio":"","ejere_underskriver2_underskriv":"","ejerf_radio":"","ejerf_underskriver1_radio":"","ejerf_underskriver1_underskriv":"","ejerf_underskriver2_radio":"","ejerf_underskriver2_underskriv":""},"afslut":{}}')