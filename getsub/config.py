import ipaddress
import re
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['./settings.yml', './.secrets.yml'],
    default_settings={
        "WEBHOOK_URL_PATH": "/",
        "WEBHOOK_LISTEN": "0.0.0.0",
        "WEBHOOK_PORT": 8080
    },
    load_dotenv=True,
)

settings.validators.register(
    Validator("BOT_TOKEN", must_exist=True, is_type_of=str, condition=lambda x: bool(re.fullmatch(r'^\d+:[A-Za-z0-9_-]{35}$', x))),
    Validator("PANEL_URL", must_exist=True, is_type_of=str, condition=lambda x: re.match(r"^https://", x)),
    Validator("PANEL_USER", must_exist=True, is_type_of=str),
    Validator("PANEL_PASSWORD", must_exist=True, is_type_of=str),

    Validator("SUPPORT_LINK", is_type_of=str, condition=lambda x: re.match(r"^https://", x)),

    Validator("WEBHOOK_URL", is_type_of=str, condition=lambda x: re.match(r"^https://", x)),
    Validator("WEBHOOK_URL_PATH", is_type_of=str),
    Validator("WEBHOOK_LISTEN", is_type_of=str, condition=lambda x: bool(isinstance(x, ipaddress.IPv4Address) or isinstance(x, ipaddress.IPv6Address))),
    Validator("WEBHOOK_PORT", is_type_of=int, condition=lambda x: bool(1 <= x <= 65535)),

    Validator("SUBSCRIPTION_OPTIONS", is_type_of=list),
)

settings.validators.validate()
