import sys

import conversation
import db
from db import User, Conversation, Message, GroupMember
import c2


def create_user():
    first_name = input("Enter your first name: ")
    second_name = input("Enter your last name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    user = db.get_entity_by_email(User, email)

    if user != None:
        print("User email already exist")
        exit(0)
    else:
        db.create_user(first_name, second_name, email, password, False)
        print(f"{first_name} {second_name} {email} {password}")


def validate(email, password):
    us = db.get_entity_by_email_and_password(User, email, password)
    if us is None:
        return False
    return True


"""
This function set all users login to False because,
the user might close the terminal instead of login 
"""


def default_login_out():
    all_users = db.get_users()
    for user in all_users:
        # set user login to false
        user.login = False
        # Update db
        db.update_user(user)


# end of function

# This method display the conversation
def showConversations() -> None:
    index = 1
    for conv in db.get_conversations():
        print(f"{index} {conv.conversation_name}")
        index += 1


def conv_id_from_db(email, global_user) -> Conversation:
    get_conv_id = None
    isTrue = True
    num_of_tries = 0
    while isTrue:
        if num_of_tries == 4:
            # Call start up again to restart the application
            start_up(email, global_user)
        join_option = input("Enter group name: ")
        if join_option == 'q' or join_option == 'Q':
            start_up(email, global_user)
        if join_option != None:
            get_conv_id = db.get_conv_by_name(Conversation, join_option)
            if get_conv_id != None:
                isTrue = False
            else:
                print("Enter a valid conversation name, create one or q to go back")
        num_of_tries += 1
    return get_conv_id


def start_up(email, global_user) -> None:
    while True:
        print("1. Create Conversation:\n2. View and Join\n3. View and Delete\n4. Logout\n5: Quit")
        user_ans = input("Enter #: ")
        if user_ans == '1':
            conv_name = input("Enter conversation name: ")
            db.create_conversation(conv_name)
            # Get conversation
            get_conv_with_name = db.get_conv_by_name(Conversation, conv_name)
            # create group message table with user and conversation primary keys
            # Get user's id
            user = db.get_entity_by_email(User, email)
            # Persist to db
            db.create_group_message(user.id, get_conv_with_name.id)
        elif user_ans == '2':
            print("Join:")
            # Show conversations
            showConversations()
            # Conversation verification
            get_conv_id = conv_id_from_db(email, global_user)
            # Get user details from db
            user = db.get_entity_by_email(User, email)
            # Check if the id is not associate with user already
            user_already_belong_to_group = db.get_group_userid_conversationid(user.id, get_conv_id.id)
            # if user_already_belong_to_group != None and user_already_belong_to_group.conversation_id == get_conv_id.id:
            #     print(f"{user.first_name} belong to the group already")
            if user_already_belong_to_group is None:
                # Add user to the group
                db.create_group_message(user.id, get_conv_id.id)
            # Start the client script
            c2.start(get_conv_id.id, email)
        elif user_ans == '3' or user_ans == 'View and Delete' or user_ans == 'view and delete':
            print("Delete:")
            # Show conversations
            showConversations()
            get_conv_id = conv_id_from_db(email, global_user)
            if get_conv_id is not None:
                # Call db function delete conversation
                db.delete_conversation(get_conv_id.conversation_name)
        elif user_ans == '4' or user_ans == 'logout' or user_ans == 'Logout':
            # Logout the user
            global_user.login = False
            # Update db
            db.update_user(global_user)
            # Your logged out
            print("You logged out <-> See your soon")
            # send the user back to login page
            user_login()
        elif user_ans == '5' or user_ans == 'quit' or user_ans == 'Quit':
            exit(0)


def user_login() -> None:
    email = ""
    password = ""
    global_user = None
    i = 0
    while i < 4:
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        if email == "q" or email == "Q" or password == "q" or password == "Q":
            exit(0)
        isTrue = validate(email, password)
        if isTrue:
            break
        print("Incorrect password or email, Try again")
        i += 1
    if validate(email, password):
        # client.main()
        # Set global user the client user
        global_user = db.get_entity_by_email(User, email)
        # set login to true
        global_user.login = True
        # Persist t to db
        db.update_user(global_user)
        # Start up
        start_up(email, global_user)
    else:
        print(f"Try again next time")
        exit(0)


# def find_user(email):
#     for i in user:
#         for v in i.values():
#             if v == email:
#                 return v
#     return None


def forgot():
    email = input("Enter your email: ")
    us = db.get_entity_by_email(User, email)
    if us.email == email:
        if us != None:
            new_password = input("Enter new password: ")
            if new_password != '':
                us.password = new_password
                db.update_user(us)
                print("Password updated Successfully")
    else:
        print("User does not exist")
    user_login()


def select():
    print("1 login: \n2. Register: \n3. Forget Password: \n4. Quit")
    option = input("Choose: ")
    if option == 'login' or option == '1':
        user_login()
    elif option == 'Register' or option == '2':
        create_user()
        user_login()
    elif option == 'Forget Password' or option == '3':
        forgot()
    else:
        exit(0)

# create_user()
# # create_user()
# user_login()
