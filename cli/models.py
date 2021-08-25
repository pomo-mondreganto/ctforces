from typing import Optional

from pydantic import BaseModel


class AdminConfig(BaseModel):
    user: str
    password: str


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str = 'postgres'
    port: int = 5432
    dbname: str = 'ctforces'


class RabbitMQConfig(BaseModel):
    user: str
    password: str
    host: str = 'rabbitmq'
    port: int = 5672
    vhost: str = 'forcad'


class SendgridConfig(BaseModel):
    user: str


class SMTPConfig(BaseModel):
    host: str
    user: str
    port: int
    password: str


class EmailConfig(BaseModel):
    url: str
    smtp: Optional[SMTPConfig]
    sendgrid: Optional[SendgridConfig]


class DjangoConfig(BaseModel):
    debug: bool = False
    secret_key: Optional[str]
    email: EmailConfig


class Config(BaseModel):
    admin: AdminConfig
    db: DatabaseConfig
    rabbitmq: RabbitMQConfig
    django: DjangoConfig