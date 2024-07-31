import sys

from pyrogram import Client

app = Client(name='my_account')

with app:
    me = app.get_me()
    text = f"""
    My name is {me.first_name}
    My surname is {me.last_name}
    My username is {me.username}
    My id is {me.id}
    """
    print(text)
    sys.exit(1)

# 27618579
# '2bde502799414029ff5e63be8b9529e8'
# +79080409710

# 26346875
# '611541e998721efc4e5dd0b55af0d13d'
# +79068664228
