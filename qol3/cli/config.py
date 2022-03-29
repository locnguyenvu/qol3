import qol3.dbconfig

def set(name:str, value:str):
    qol3.dbconfig.set(name, value)
    print("update success!")
    pass