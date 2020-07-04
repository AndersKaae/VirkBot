from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, UnicodeText, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db')
Base = declarative_base()

class Json_Data(Base):
	__tablename__ = 'json_data'
	id = Column(Integer, primary_key=True)
	json = Column(UnicodeText(length=2**31), nullable=False)
	email = Column(String(50), nullable=False)

Session = sessionmaker(bind=engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
Base.metadata.create_all(engine)

def insertjson(json, email):
	data = Json_Data(json = json, email = email)
	session.add(data)
	session.commit() 
	session.close()

def getjson():
	query = session.query(Json_Data).order_by(Json_Data.id.desc()).first()
	json = query.json
	session.close()
	return json