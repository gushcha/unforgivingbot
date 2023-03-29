from dataclasses import dataclass, field
import yaml


@dataclass
class Config:
    bot_name: str
    bot_token: str
    db_host: str
    db_name: str
    db_port: int
    db_user_submitter: str
    db_password_submitter: str
    db_user_notifier: str
    db_password_notifier: str
    notifier_runtime_delta: int
    logging_level: str
    logging_filename: str
    logging_max_bytes: int
    logging_backup_count: int


__config: Config = None


def read_config():
    with open('config.yml', 'r') as file:

        file_contents = yaml.safe_load(file)
        global __config
        __config = Config(
            bot_name=file_contents['bot']['name'],
            bot_token=file_contents['bot']['token'],
            db_host=file_contents['db']['host'],
            db_name=file_contents['db']['name'],
            db_port=file_contents['db']['port'],
            db_user_submitter=file_contents['db']['user_submitter'],
            db_password_submitter=file_contents['db']['password_submitter'],
            db_user_notifier=file_contents['db']['user_notifier'],
            db_password_notifier=file_contents['db']['password_notifier'],
            notifier_runtime_delta=file_contents['notifier']['runtime_delta'],
            logging_level=file_contents['logging']['level'],
            logging_filename=file_contents['logging']['filename'],
            logging_max_bytes=file_contents['logging']['max_bytes'],
            logging_backup_count=file_contents['logging']['backup_count'],
        )


def get_config() -> Config:
    global __config
    return __config
