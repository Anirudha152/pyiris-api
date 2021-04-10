# API
# done
import os


def main(directory):
    if os.path.isdir(directory):
        for dirpath, _, filenames in os.walk(directory):
            for f in filenames:
                yield os.path.abspath(os.path.join(dirpath, f))
    else:
        yield os.path.abspath(directory)
