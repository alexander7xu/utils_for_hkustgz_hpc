#!/usr/bin/python3
from subprocess import Popen as run_proc_async
from subprocess import PIPE
from socket import gethostbyname
import argparse


def main(args: argparse.Namespace) -> None:
    cmd = [
        '/opt/pulsesecure/bin/pulselauncher',
        '-U',
        'remote.hkust-gz.edu.cn',
        '-r',
        'Student',
        '-u',
        args.username,
        '-p',
        args.password,
    ]
    proc = run_proc_async(cmd, stdout=PIPE, stderr=PIPE)
    print('Running')

    try:
        for out in iter(proc.stdout.readline, b''):
            msg = out.decode()
            print(msg, end='')

            token = 'Assigned IPV4: '
            idx = msg.find(token)
            if idx == -1:
                continue

            print('Modifying route table')
            local_addr = msg[idx + len(token) : -1]
            remote_addr = gethostbyname('login.hpc.hkust-gz.edu.cn')
            run_proc_async(
                f'route del default && sudo route add {remote_addr} gw {local_addr} metric 100 dev tun0',
                shell=True,
            ).wait()
    except KeyboardInterrupt:
        proc.kill()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', '-u', type=str, required=True)
    parser.add_argument('--password', '-p', type=str, required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
