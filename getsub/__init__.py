import logging
import sys
import time

from getsub import logger
from getsub import config


logger = logging.getLogger(__name__)


if sys.version_info[0] < 3 or sys.version_info[1] < 11:
    logger.critical(
        """
=============================================================
You MUST need to be on python 3.11 or above, shutting down the bot...
=============================================================
"""
    )
    sys.exit(1)
