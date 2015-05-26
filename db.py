from sqlalchemy import Column,String,Integer,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
        __tablename__ = 'user'
        id = Column(String(20), primary_key=True)
        name = Column(String(20))
        password = Column(String(32))

class Hostinfo(Base):
	__tablename__ = 'hostinfo'
	hid = Column(Integer, primary_key=True,autoincrement='ignore_fk')
	wan_ip = Column(String(12))
	lan_ip = Column(String(12))
	hostname = Column(String(20))
	groupname = Column(String(20))

class Commandhistory(Base):
	__tablename__ = 'commandhistory'
	cid = Column(Integer, primary_key=True,autoincrement='ignore_fk')
	hosts = Column(String(20))
	module = Column(String(20))
	command = Column(String(160))
	datetime = Column(String(20))

class Playbook(Base):
	__tablename__ = 'playbook'
	pid = Column(Integer, primary_key=True,autoincrement='ignore_fk')
	bookname = Column(String(40))
	bookpage = Column(Integer)
	hosts = Column(String(20))
	module = Column(String(20))
	command = Column(String(160))

engine = create_engine('mysql+mysqlconnector://root:password@127.0.0.1:3306/wyangsun')

DBSession = sessionmaker(bind=engine)
