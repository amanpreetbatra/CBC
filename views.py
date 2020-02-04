from connection  import  *


def hello_world():
    user = list(col.find())
    print(user)
    return 'hello'