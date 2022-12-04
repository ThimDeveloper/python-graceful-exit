from graceful_exit.logging.custom_logging import get_logger

logger = get_logger("SignalExceptions")


class SigTerm(SystemExit):
    logger.debug("registering SigTerm")


class SigInt(SystemExit):
    logger.debug("registering SigInt")
