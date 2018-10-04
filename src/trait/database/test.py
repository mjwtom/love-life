import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import sessionmaker
from oslo_db.sqlalchemy import enginefacade

from oslo_config import cfg
from oslo_log import log as logging

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
DOMAIN = "demo"

logging.register_options(CONF)
logging.setup(CONF, DOMAIN)

# Oslo Logging uses INFO as default
LOG.info("Oslo Logging")
LOG.warning("Oslo Logging")
LOG.error("Oslo Logging")


print(sqlalchemy.__version__)
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')

session.add(ed_user)

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

our_user = session.query(User).filter_by(name='ed').first()

session.commit()
