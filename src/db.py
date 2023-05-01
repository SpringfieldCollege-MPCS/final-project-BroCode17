import pathlib
from datetime import date
import datetime
from typing import Optional, List  #

from sqlmodel import Field, SQLModel, create_engine, Column, Integer, ForeignKey, Session, select
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlite3 import Connection as SQLite3Connection

# TOP_DIR = pathlib.Path(__file__).parent

# Database connection goes here
# sqlite_file_name = TOP_DIR / 'database' / 'database.db'
sqlite_url = f"sqlite:///database.db"  #
engine = create_engine(sqlite_url, echo=False)  #


# This is needed to enforce foreign key constraints
# You can ignore this


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


### Model Definitions ###
class User(SQLModel, table=True):  #
    id: Optional[int] = Field(
        default=None, primary_key=True)  # this will autoincrement by default
    first_name: str
    last_name: str
    email: str
    password: str
    login: bool


class Conversation(SQLModel, table=True):  #
    id: Optional[int] = Field(default=None, primary_key=True)  #
    conversation_name: str
    # user_id: Optional[int] = Field(
    #     sa_column=Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    # )
    # name: str
    # date_created: str


class GroupMember(SQLModel, table=True):  #
    id: Optional[int] = Field(default=None, primary_key=True)  #
    user_id: Optional[int] = Column(Integer, ForeignKey("user.id"))
    conversation_id: Optional[int] = Column(Integer, ForeignKey("conversation.id"))
    # join_date: str
    # left_date: str


class Message(SQLModel, table=True):
    message_id: Optional[int] = Field(default=None, primary_key=True)
    from_email: str
    message_text: str
    sent_date: str
    conversation_id: Optional[int] = Column(Integer, ForeignKey("conversation.id"))


### Function Definitions ###
def create_user(first_name: str, last_name: str, email: str, password: str, login: bool = False, save=True):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password, login=login)
    if save:
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
    return user


def create_conversation(conversation_name: str, save=True):
    conversation = Conversation(conversation_name=conversation_name)
    if save:
        with Session(engine) as session:
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

    return conversation


# join_date:str=None, left_date:str=None,
def create_group_message(user_id: Optional[int] = None, conversation_id: Optional[int] = None, save=True):
    group_member = GroupMember(user_id=user_id, conversation_id=conversation_id)
    if save:
        with Session(engine) as session:
            session.add(group_member)
            session.commit()
            session.refresh(group_member)

    return group_member


def create_message(from_email: str, message_text, sent_date: str, conversation_id: Optional[int] = None, save=True):
    message = Message(from_email=from_email, message_text=message_text, sent_date=sent_date,
                      conversation_id=conversation_id)
    if save:
        with Session(engine) as session:
            session.add(message)
            session.commit()
            session.refresh(message)

    return message


def get_users() -> List[User]:
    with Session(engine) as session:
        return list(session.query(User).all())


def get_conversations() -> List[User]:
    with Session(engine) as session:
        return list(session.query(Conversation).all())


def get_group_member() -> List[GroupMember]:
    with Session(engine) as session:
        return list(session.query(GroupMember).all())


def get_all_messages() -> List[Message]:
    with Session(engine) as session:
        return list(session.query(Message).all())


def get_messages(converation_id) -> List[Message]:
    l = []
    with Session(engine) as session:
        statement = select(Message).where(Message.conversation_id == converation_id)
        res = session.exec(statement)
        for r in res:
            l.append(r)
    return l


# def get_worklists(user_id=1):
#     with Session(engine) as session:
#         return list(session.query(Worklist).where(Worklist.user_id == user_id))

# def get_tasks(worklist_id=1):
#     with Session(engine) as session:
#         return list(session.query(Task).where(Task.worklist_id == worklist_id))

def update_entity(entity):
    with Session(engine) as session:
        session.add(entity)
        session.commit()
        session.refresh(entity)
    return entity


def get_entity(model: SQLModel, id):
    with Session(engine) as session:
        entity = session.get(model, id)
        return entity


def get_entity_by_email(model: SQLModel, email):
    with Session(engine) as session:
        statement = select(model).where(model.email == email)
        me = session.exec(statement)
        for m in me:
            return m


def get_group_userid_conversationid(user_id, conversation_id):
    with Session(engine) as session:
        statement = select(GroupMember).where(
            GroupMember.user_id == user_id and GroupMember.conversation_id == conversation_id)
        res = session.exec(statement)
        for m in res:
            return m


def get_conv_by_name(model: SQLModel, conversation_name: str):
    with Session(engine) as session:
        statement = select(model).where(model.conversation_name == conversation_name)
        me = session.exec(statement)
        for m in me:
            return m


def delete_entity(entity):
    with Session(engine) as session:
        session.delete(entity)
        session.commit()


def create_fake_data():
    """Insert your fake data in here"""
    create_user("Ebenezer", "Frimpong", "you@me.com", "1234")
    create_user("Frimpong", "Ebenezer", "me@you.com", "1234")
    create_conversation("We")
    create_conversation("Me")
    create_group_message(1, 1)
    create_group_message(2, 2)


def create_db_and_tables():  #
    """This creates our tables and add some fake data"""
    SQLModel.metadata.drop_all(engine)  #
    SQLModel.metadata.create_all(engine)  #
    create_fake_data()


# Create tables and fake data by: python -m todolist.db
if __name__ == "__main__":  #
    # create_db_and_tables()  #
    now = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    # create_message("me@you.com","how are you doing",str(now),2)
    me = get_users()
    print(get_group_member())
    print(get_conversations())
    print(get_all_messages())

