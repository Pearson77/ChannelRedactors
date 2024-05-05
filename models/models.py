from sqlalchemy import create_engine, Column, Integer, String, BigInteger, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    # Отношение к 'access' через 'ChannelAccess'
    accesses = relationship("ChannelAccess", back_populates="channel")


class Redactor(Base):
    __tablename__ = 'redactors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False)
    username = Column(String(32), nullable=False)
    schedule_type = Column(String(32), nullable=False)
    next_act_type = Column(String(32), nullable=False)
    next_act_time = Column(TIMESTAMP, nullable=False)

    # Отношение к 'access' через 'RedactorAccess'
    accesses = relationship("ChannelAccess", back_populates="redactor")


class ChannelAccess(Base):
    __tablename__ = 'access'
    redactor_id = Column(ForeignKey('redactors.id'), primary_key=True)
    channel_id = Column(ForeignKey('channels.id'), primary_key=True)

    # Отношения к 'Redactor' и 'Channel'
    redactor = relationship("Redactor", back_populates="accesses")
    channel = relationship("Channel", back_populates="accesses")


def get_session():
    session_maker = sessionmaker(bind=engine)
    return session_maker()
