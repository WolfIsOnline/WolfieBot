def set_token():
    
    token = input("Enter bot token: ")
    with open(".env", "w") as env:
        env.write(f"TOKEN={token}")
    print(f"{env.name} written")    
    set_database()
    
def set_database():
    database = input("Enter MongoDB connection: ")
    with open("./database/.env", "w") as env:
        env.write(f"MONGODB_CONNECTION=\"{database}\"")
    print(f"{env.name} written")
    
set_token()