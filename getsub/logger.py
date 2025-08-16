import logging
import logging.config
import yaml

from getsub.config import settings, secrets_values
from getsub.logger_filter import ExactValueRedactionFilter

with open('logging.yml', 'rt') as f:
    logging_config = yaml.safe_load(f.read())

logging.config.dictConfig(logging_config)

if settings.get("REDACT_SECRETS"):
    # Attach the filter instance to all handlers
    redact_filter = ExactValueRedactionFilter(secrets_values)
    for handler in logging.root.handlers:
        handler.addFilter(redact_filter)
