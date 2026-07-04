import bcrypt

async def verify_password(plain_password:str,hashed_password)->bool:
    verified:bool=bcrypt.checkpw(plain_password.encode(),hashed_password.encode())
    return verified

def get_password_hash(password:str)->str:
    hashed_password:bytes=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
    decoded_password:str=hashed_password.decode()
    return decoded_password