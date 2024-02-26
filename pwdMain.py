# import yfinance as yf
#
#
#
#
# def ma():
#     pass
#
#
# def ema():
#     pass
#
# def wma():
#     pass
#
#
# def macd():
#     pass
#
#
# def rsi():
#     pass
#
#
# def vwap():
#     pass

# Password generator/ manager
# 1) Ask user if they want to store or retrieve a password
# 2) for store ask what for (google, website, etc) - then take their username/pwd and store in json or csv file
# 3) if retrieving a pwd ask you ask them for what service and then you print all of the users and password with that,
# because you can have multiple saves accounts on one service.

# Bonus tasks:
# 1) Make a master password, which you'll have to enter in order to access the choice to either store or get a password.
# So if a user enters incorrect master password you don't let them in.
# 2) Encrypt the passwords before saving and then decrypt them before printing them out, when the user requests them.
# 3) Use database to store passwords
# 4) Add user ability to delete credentials (CRUD maybe, please god hope you remember what this means)
# this project uses a cool ascii art for the terminal interface https://github.com/Abhijeetbyte/MYPmanager/blob/main/main.py

import cryptography
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import db
import os
import sqlite3

# import db  #we need to write the functions we'll want to call on the data base in the db file




def derive(param):
    salt = b'\xa66k\xd6)\xe1\xef\xc4)\x1d\nl\xc3I\x19\xa5'
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)

    encrypt = kdf.derive(param.encode("utf-8"))
    return encrypt


def verify(param, user):
    salt = b'\xa66k\xd6)\xe1\xef\xc4)\x1d\nl\xc3I\x19\xa5'
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)

    kdf.verify(param.encode("utf-8"), user)


#
# //User should input their username and pwd to gain access to all of their stored credentials IF NONE EXITS ALREADY
def set_master_credentials():
    # //get user inputs for username + pwd
    user = input(""" 
Welcome to your
______                                   _  
| ___ \                                 | | 
| |_/ /_ _ ___ _____      _____  _ __ __| | 
|  __/ _` / __/ __\ \ /\ / / _ \| '__/ _` | 
| | | (_| \__ \__  \ V  V / (_) | | | (_| | 
\_|  \__,_|___/___/ \_/\_/ \___/|_|  \__,_|                                                                                  
 ___  ___                                   
 |  \/  |                                   
 | .  . | __ _ _ __   __ _  __ _  ___ _ __  
 | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__| 
 | |  | | (_| | | | | (_| | (_| |  __/ |    
 \_|  |_/\__,_|_| |_|\__,_|\__, |\___|_|    
                            __/ |           
                           |___/                             
    
    
Input master username: """)


    key1 = derive(user)

    user_check = db.user_exits(key1)

    if user_check:
        master_user_pwd = input("Login: ")
        safeword = "gibberish " + master_user_pwd
        verify(safeword, db.get_password(key1))
        key = derive(master_user_pwd)

    else:
        master_user_pwd = input("Create your master password: ")
        key = derive(master_user_pwd)
        # making a safeword so we don't store the encryption key in the db
        safeword = derive("gibberish " + master_user_pwd)
        db.new_user(key1, safeword)

    id = db.get_ID(key1)

    return key, id


# //verifying the user and encrypted password, we'll use this later to allow us into actions
def verify_master_user():
    pwdCorrect = set_master_credentials
    progress = main()

    if pwdCorrect == None:
        progress



def encrypt(key, v):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encodedValue = v.encode("utf-8")

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(encodedValue)
    padded_data += padder.finalize()

    ct = encryptor.update(padded_data) + encryptor.finalize()

    return ct + iv


# def decrypt(key, iv, ct):
#     cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
#     decryptor = cipher.decryptor()
#     decrypted_text = decryptor.update(ct) + decryptor.finalize()
#
#     # we padded the encrypted word above so must remove the padding or else we'll print gibberish as well
#     unpadder = padding.PKCS7(128).unpadder()
#     unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()
#
#     return unpadded_text.decode("utf-8")

def decrypt(key, input_values):
    ct = input_values[0:-16]
    iv= input_values[-16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ct) + decryptor.finalize()

    # we padded the encrypted word above so must remove the padding or else we'll print gibberish as well
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()

    return unpadded_text.decode("utf-8")


def do_action():
    action = input("Do you want to Store, Retrieve, or Delete a password? S/R/D. Else Q to Quit: ").upper()
    return action



def add_creds(key, id):
    get_site = input("What website is this for?: ").lower()

    get_login = input("enter your username: ")

    get_pwd = input("enter your password: ")

# website not encrypted as will be used to reference master_users credentials
# reducing the amount of data needed to be decrypted per user
    key1 = get_site
    key2 = encrypt(key, get_login)
    key3 = encrypt(key, get_pwd)



    db.write_to_db(str(key1), key2, key3, id)



def get_creds(key, id):
    site = input("Which site do you need your logins for?  ").lower()
    input_values = db.read_from_db(id, site)

    username = decrypt(key, input_values[0])
    password = decrypt(key, input_values[1])

    print(f"{username, password}")






# // user interaction options for storing/retrieving/deleting etc credentials
def main():
    key, id = set_master_credentials()


    while True:
        action = do_action()
        if action == "S":
            add_creds(key, id)
        elif action == "R":
            get_creds(key, id)
        # elif action == "D":
        #     delete_credentials()
        elif action == "Q":
            break  # Exit the loop
        else:
            print("Invalid action. Please choose S(tore), R(etrieve), D(elete), or Q(uit).")


# print(encrypt(derive("222"), "test"))
# print(
#     decrypt(derive("222"), b'e\x8d8\x9a,\x8b+;j\x13\xcd$D\xc6\xbbC', b'\xf6\xb1\xb8\x9a!\x14\x05<?B\xc5\xaf0\xb8\xf0x'))
# set_master_credentials()
# verify_master_user()
# encrypt(key, v)
main()
# add_creds()
# continue_action()

# write_data_json()
# # read_creds = read_user_json()
#
# print(read_creds)

# get_creds(do_action())


# if __name__ == "__main__":
#     main()


