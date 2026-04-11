from loguru import logger


def configure_logging() -> None:
    logger.remove()
    logger.add(
        sink=lambda message: print(message, end=""),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    )
