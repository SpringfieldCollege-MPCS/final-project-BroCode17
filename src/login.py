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
    # isEmail = False
    # isPassword = False
    us = db.get_entity_by_email(User, email)
    if us.email == email and us.password == password:
        return True
    # for i in user:
    #     for v in i.values():
    #         if v == email:
    #             isEmail = True
    #         if v == password:
    #             isPassword = True
    #         if isEmail and isPassword:
    #             break
    return False

"""
This function set all users login to False because,
the user might close the terminal instead of login 
"""
def default_login_out():
    all_users = db.get_users()
    for user  in all_users:
        # set user login to false
        user.login = False
        # Update db
        db.update_user(user)
# end of function

def user_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    global_user = None
    if not validate(email, password):
        i = 0
        while i < 4:
            print("Incorrent password or email, Try again")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            isTrue = validate(email, password)
            if isTrue:
                break
            i += 1

    if validate(email, password):
        # client.main()
        # Set global user the client user
        global_user = db.get_entity_by_email(User, email)
        # set login to true
        global_user.login = True
        # Persist t to db
        db.update_user(global_user)
        while True:
            print("1. Create Conversation:\n2. View and Join\n3. Logout\n4: Quit")
            user_ans = input("Enter #: ")
            if user_ans == '1':
                conv_name = input("Enter conversation name: ")
                db.create_conversation(conv_name)
                # Get conversation
                get_conv_with_name = db.get_conv_by_name(Conversation, conv_name)
                # create group message table with user and conversation primary keys
                # Get user's id
                user = db.get_entity_by_email(User, email)
                print(f"{user.id} {get_conv_with_name.id}")
                db.create_group_message(user.id, get_conv_with_name.id)
                print(get_conv_with_name)
            elif user_ans == '2':
                print("Join:")
                index = 1
                for conv in db.get_conversations():
                    print(f"{index} {conv.conversation_name}")
                    index += 1
                
                join_option = input("Selete option ( Enter name of the group): ")
                get_conv_id = db.get_conv_by_name(Conversation, join_option)
                user = db.get_entity_by_email(User, email)
                # Check if the id is not associate with user already
                user_already_belong_togroup = db.get_group_userid_conversationid(user.id,get_conv_id.id)
                print(user_already_belong_togroup)
                if user_already_belong_togroup != None and user_already_belong_togroup.conversation_id == get_conv_id.id:
                    print(f"{user.first_name} belong to the group already")
                else:
                    # Add user to the group
                    db.create_group_message(user.id, get_conv_id.id)
                    print("Added successfully")
                # print(db.get_group_userid_conversationid(user_id=user.id, conversation_id=get_conv_id.id))
                # Showing message
                # Loading prevous msg
                msg = db.get_messages(get_conv_id.id)
                # for m in msg:
                #     print(f"{m.from_email}:{m.sent_date}-> {m.message_text}")
                # Starting the client function
                c2.start(get_conv_id.id, email)
            elif user_ans == '3' or user_ans == 'logout' or user_ans == 'Logout':
                # Logout the user
                global_user.login = False
                # Update db
                db.update_user(global_user)
                #Your logged out
                print("You logged out <-> See your soon")
                # send the user back to login page
                user_login()
            elif user_ans == '4' or user_ans == 'quit' or user_ans == 'Quit':
                exit(0)
        # end of while loop
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
        if us!= None:
            new_password = input("Enter new password: ")
            if new_password != '':
                us.password = new_password
                db.update_user(us)
                print("Password updated Successfully")
    else :
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
