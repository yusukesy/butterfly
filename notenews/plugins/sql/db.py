from sqlalchemy import Column, String, Numeric, Boolean
from . import SESSION, BASE

class database(BASE):
    __tablename__ = "database"
    website = Column(String, primary_key=True)
    link = Column(String)

    def __init__(self, website, link):
        self.website = website
        self.link = link

database.__table__.create(checkfirst=True)

def get_link(website):
    try:
        return SESSION.query(database).get(website)
    except:
        return None
    finally:
        SESSION.close()

def update_link(website, link):
    to_check = get_note(website)
    if not to_check:
        adder = Notes(website, reply)
        SESSION.add(adder)
        SESSION.commit()
        return
    rem = SESSION.query(Notes).get(website)
    SESSION.delete(rem)
    SESSION.commit()
    adder = Notes(website, reply)
    SESSION.add(adder)
    SESSION.commit()
    # adder = SESSION.query(database).get(website)
    # if adder:
        # adder.link = link
    # else:
        # adder = database(
            # website,
            # link
        # )
    # SESSION.add(adder)
    # SESSION.commit()
    
#
def get_all():
    try:
        return SESSION.query(database).all()
    except:
        return None
    finally:
        SESSION.close()
#