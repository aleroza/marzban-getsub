from ipaddress import IPv4Address, IPv6Address 
import re
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="GETSUB",
    load_dotenv=True,
    settings_files=['./.secrets.yml'],
)

secrets_values = settings.to_dict()
if 'LOAD_DOTENV' in secrets_values and secrets_values['LOAD_DOTENV'] is True:
    del secrets_values['LOAD_DOTENV']
secrets_values = list(secrets_values.values())

settings.load_file(['./settings.yml'])

settings.validators.register(
    Validator("BOT_TOKEN", must_exist=True, is_type_of=str, cast=str, condition=lambda x: bool(re.fullmatch(r'^\d+:[A-Za-z0-9_-]{35}$', x))),
    Validator("PANEL_URL", must_exist=True, is_type_of=str, cast=str, condition=lambda x: re.match(r"^https://", x)),
    Validator("PANEL_USER", must_exist=True, is_type_of=str, cast=str),
    Validator("PANEL_PASSWORD", must_exist=True, is_type_of=str, cast=str),

    Validator("SUPPORT_LINK", is_type_of=str, cast=str, condition=lambda x: re.match(r"^https://", x)),

    Validator("WEBHOOK_URL", is_type_of=str, cast=str, condition=lambda x: re.match(r"^https://", x)),
    Validator("WEBHOOK_URL_PATH", is_type_of=str, cast=str, default="/"),
    Validator("WEBHOOK_LISTEN", is_type_of=str, cast=str, default="0.0.0.0", condition=lambda x: bool(isinstance(IPv4Address(x), IPv4Address) or isinstance(IPv6Address(x), IPv6Address))),
    Validator("WEBHOOK_PORT", is_type_of=int, cast=int, default=8080, condition=lambda x: bool(1 <= x <= 65535)),

    Validator("SUBSCRIPTION_OPTIONS", is_type_of=list, cast=list),
    Validator("TG_UID_SALT", is_type_of=str, cast=str, default="some_salt"),
    Validator("REDACT_SECRETS", is_type_of=bool, cast=bool, default=True),
)

settings.validators.validate()
