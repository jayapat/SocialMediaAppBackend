from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)

def varify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)