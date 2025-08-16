import logging

class ExactValueRedactionFilter(logging.Filter):
    def __init__(self, secrets_values):
        super().__init__()
        self.secrets_values = [val for val in secrets_values if val]  # Filter out None/empty

    def filter(self, record):
        try:
            # Redact exact matches in the message string
            msg = record.msg
            for value in self.secrets_values:
                if isinstance(msg, str):
                    msg = msg.replace(value, 'REDACTED')

            # Handle tuple args (e.g., if values appear in formatted strings)
            if record.args and isinstance(record.args, tuple):
                args = []
                for arg in record.args:
                    if isinstance(arg, str):
                        redacted_arg = arg
                        for value in self.secrets_values:
                            redacted_arg = redacted_arg.replace(value, 'REDACTED')
                        args.append(redacted_arg)
                    else:
                        args.append(arg)
                record.args = tuple(args)

            # For dict args, optionally redact values (but avoid key-based; scan stringified if needed)
            # Skip if not required, as per exact value focus

            record.msg = msg
        except Exception:
            pass  # Fallback to original
        return True
