class Company:
  def __init__(self, name, secondaryName, adress, email, advertising, signingDate, effectDate, purpose, powertobind, industrycode, capital, fiscalstart, fiscalend, firstfiscalend):
    self.name = name
    self.secondaryName = secondaryName
    self.adress = adress
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
    self.firstfiscalend = firstfiscalend

class Owner:
    def __init__(self, kind, name, cpr):
        self.kind = kind
        self.name = name
        self.cpr = cpr

class Manager:
    def __init__(self, kind, name, cpr):
        self.kind = kind
        self.name = name
        self.cpr = cpr