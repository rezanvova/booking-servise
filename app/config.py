from environs import Env
class Settings:
    def __init__(self):
        self.env = Env()
        self.env.read_env()

        self.DB_HOST = self. env.str("DB_HOST")
        self.DB_PORT = self.env.int("DB_PORT")
        self.DB_NAME = self.env.str("DB_NAME")
        self.DB_USER = self. env.str("DB_USER")
        self.DB_PASS = self.env.str("DB_PASS")
        self.DATABASE_URL = f"postgresql+asyncpg://{self.DB_USER}:{self. DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self. DB_NAME}"
        self.SECRET_KEY = self.env.str("SECRET_KEY")
        self.ALGORITHM = self.env.str("ALGORITHM")
        self.SMTP_PORT = self. env.str("SMTP_PORT")
        self.SMTP_USER = self. env.str("SMTP_USER")
        self.SMTP_PASS = self. env.str("SMTP_PASS")
        self.SMTP_HOST = self. env.str("SMTP_HOST")

        self.REDIS_HOST = self. env.str("REDIS_HOST")
        self.REDIS_PORT = self. env.str("REDIS_PORT")

setting = Settings()