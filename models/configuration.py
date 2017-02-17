import os
import sys


configuration = {}


def set_config(key, value):
    global configuration
    if os.environ.get(key) is not None:
        configuration[key] = os.environ.get(key)
    else:
        configuration[key] = value


def get_config(key):
    global configuration
    if key in configuration:
        return configuration[key]
    else:
        set_config(
            key,
            os.environ.get(key)
        )
        return configuration[key]


def __parse_env_line(line):
    args = line.split('=', 1)
    if len(args) == 2:
        set_config(
            args[0].strip(),
            args[1].strip()
        )
    else:
        sys.stderr.write(
            'Bad line in config: {}\n'.format(
                line.strip()
            )
        )
        sys.stderr.flush()


with open('.env', 'r') as f:
    for line in f:
        __parse_env_line(line)
