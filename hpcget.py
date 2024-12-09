#!/usr/bin/python3
import os
import json
import argparse
from pathlib import Path
from socket import gethostbyname
from re import findall as re_findall


def resolve(path: Path) -> dict:
    hcl_path = tuple(path.glob('*.hcl'))
    assert len(hcl_path) == 1
    hcl_path = hcl_path[0]

    log_path = tuple(path.glob('output.*.txt'))
    assert len(log_path) == 1
    log_path = log_path[0]

    name = str(hcl_path.stem)
    with open(hcl_path) as file:
        hcl = file.read()
    host = re_findall(r'host\s*=\s*"(.+)"', hcl)
    port = re_findall(r'"-p",\s*"(\d+):22"', hcl)
    gpus = re_findall(r'envs\s*=.*"NVIDIA_VISIBLE_DEVICES=(.+)"', hcl)
    assert len(host) == len(port) == 1
    host, port = str(host[0]), int(port[0])
    gpus = '' if len(gpus) == 0 else str(gpus[0]).replace(',', '|')

    job = int(log_path.stem[len('output.') :])
    with open(log_path) as file:
        log = file.read()

    datetime = re_findall(r'INFO (.+?) (.+?) [\s\S]+success', log)
    assert len(datetime) == 1 and len(datetime[0]) == 2
    date, time = map(str, datetime[0])

    # image = re_findall(r'Status: Image is up to date for .+/(.+)', log)
    # assert len(image) == 1
    # image = str(image[0])

    try:
        ip = gethostbyname(host)
    except Exception:
        ip = None

    return {
        'name': name,
        'job': job,
        'date': date,
        'time': time,
        'ip': ip,
        'port': port,
        #'image': image,
        'gpus': gpus,
        'host': host,
    }


class FormatterRegister:
    formatters = dict()

    @classmethod
    def register(cls, name: str):
        def decorator(func):
            cls.formatters[name] = func
            return func

        return decorator


@FormatterRegister.register('config')
def formatter_config(data: list, username: str) -> str:
    results = [
        f'''\
# If you are using ssh-proxy, add: ProxyCommand ssh $ProxyName -W %h:%p
# Try get this output by running: ssh -T HpcLogin python3 {__file__}

Host HpcLogin
    HostName login.hpc.hkust-gz.edu.cn
    User {username}
    Port 22
'''
    ]

    for i in range(len(data)):
        results.append(
            f'''\
Host {data[i]["name"]}
    HostName {data[i]["ip"] or data[i]["host"]}
    User {username}
    Port {data[i]['port']}
'''
        )

    return '\n'.join(results)


@FormatterRegister.register('json')
def formatter_json(data: list, username: str) -> str:
    return json.dumps(data, indent=4)


@FormatterRegister.register('csv')
def formatter_csv(data: list, username: str) -> str:
    assert len(data) > 0
    results = [','.join(data[0].keys())]
    for i in range(len(data)):
        results.append(','.join(map(str, data[i].values())))
    return '\n'.join(results)


def get_data(username: str = None) -> list:
    if username is None:
        username = os.getlogin()
    paths = map(
        lambda x: x.parent.parent,
        Path(f'/hpc2ssd/JH_DATA/spooler/{username}/').glob(
            '*/*/.*/trans_application.post.sh'
        ),
    )
    data = [resolve(path) for path in paths]
    return data


def main(args: argparse.Namespace) -> None:
    formatter = FormatterRegister.formatters[args.format]
    username = os.getlogin()
    data = get_data(username)
    print(formatter(data, username))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--format',
        '-f',
        default=tuple(FormatterRegister.formatters.keys())[0],
        choices=FormatterRegister.formatters.keys(),
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    main(args)
