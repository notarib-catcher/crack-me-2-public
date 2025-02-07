# Challenge URL - crackme2-gdsc.mitb.tech [Will be open through]
# SOLUTION FOR GDSC CRACKME2

# Author - A.D (aaryan@aary.dev - Send feedback here!)
# For GDSC-MITB, 2024


# ------------- SPOILER ALERT! ---------------------------------
# The seed Isn't actually random 😁! 
# because random.random() generates a value b/w 0 and 1
# time.gmtime type-casts it to int which forces it to be zero! 
# and therefore the time string is always the same (Unix 0)
# Therefore the seed is actually ALWAYS THE SAME!
# Therefore the JWT Secret key can be predicted.
# Therefore you can sign your own JWT with HMAC... lets do that.
# --------------------------------------------------------------

import random
import time
import jwt




version = "0064-PROD" # at the bottom of the page!




# Generate the seed in the same way
not_actually_random = time.strftime("%Y %H:%M:%S +0000", time.gmtime(random.random())) + version
always_the_same_seed = int.from_bytes(bytes(not_actually_random, 'utf-8'), byteorder='little', signed=False)
random.seed(always_the_same_seed)

print(always_the_same_seed)

# generate a JWT secret to sign your fake token
# just copied the code from app.py here

jwt_secret = ""
for i in range(1,50):
    jwt_secret += str(random.randint(0,9))

print(jwt_secret)

# Sign the JWT as admin 
# (if you read the login code, the account id is "0" - a string - not an int hehe - this messes people up a bit :P)

token = jwt.encode({"id" : "0"}, jwt_secret, algorithm="HS256")


print("Token: ", token) # Place this in your cookies - replace the account cookie with it
# we did it!!!!!!!


# All rights reserved - aaryan@aary.dev 2024