from pydantic import BaseSettings

class Settings(BaseSettings): # this environment varaibels are the case insensitive, pydantic make them
    database_password : str 
    database_username : str 
    database_hostname : str
    database_port : str
    database_name : str
    secret_key : str
    algorithm : str
    access_token_expire_minutes : int

    class Config:
        env_file = ".env"

settings = Settings()