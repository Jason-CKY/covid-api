from database import Base
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, Integer, String, text


class Report(Base):
    __tablename__ = 'reports'

    reportid = Column(BigInteger, primary_key=True, server_default=text("nextval('reports_reportid_seq'::regclass)"))
    province_state = Column(String(255), index=True)
    country_region = Column(String(255), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    last_update = Column(DateTime)
    lat = Column(Float(53))
    long_ = Column(Float(53))
    confirmed = Column(Integer)
    deaths = Column(Integer)
    recovered = Column(Integer)
    active = Column(Integer)
    incident_rate = Column(Float(53))
    case_fatality_ratio = Column(Float(53))