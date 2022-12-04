import sys

CONFIG = {
    "handlers": [
        {"sink": sys.stdout, "colorize": True, "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> {message}"},
        # {"sink": sys.stderr, "colorize":True, "format": "<red>{time:YYYY-MM-DD HH:mm:ss}</red> {message}"},
        # {"sink": "file_0.log", "serialize": True, "delay": True, "rotation": "50 MB"},
        {"sink": "file_0.log", "delay": True, "rotation": "50 MB"},
    ],
    # "extra": {"user": "someone"}
}