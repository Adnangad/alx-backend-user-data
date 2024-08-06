#!/usr/bin/env python3
""" Main 5
"""
import uuid
from api.v1.auth.basic_auth import BasicAuth
from models.user import User

user_email = str(uuid.uuid4())
user_clear_pwd = str(uuid.uuid4())
user = User()
user.email = user_email
user.first_name = "Obuya"
user.last_name = "Gard"
user.password = user_clear_pwd
print("New user: {}".format(user.display_name()))
user.save()

ls = User.all()
print(ls)
try:
    lz = User.search({"email":user_email})
except AttributeError:
    print("Att error")
print(f"the search method result is:{lz}")
uz = lz[0]
user_inst = User.get(uz.id)
if not user_inst.is_valid_password(user_clear_pwd):
    print(None)
else:
    print(user_inst.display_name())
