# Helpful Tools for HPC in HUKST-GZ

## gapidown.py

When using gdown, we usually get:

> Failed to retrieve file url:
>
>     Too many users have viewed or downloaded this file recently. Please try accessing the file again later. If the file you are trying to access is particularly large or is shared with many people, it may take up to 24 hours to be able to view or download the file. If you still can't access a file after 24 hours, contact your domain administrator.
>
> You may still be able to access the file from the browser:
>
>     https://drive.google.com/uc?id=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
>
> but Gdown can't. Please check connections and permissions.

Based on Google Drive API, this script help you download file / folder without this error.

Usage:

1. Visit: https://developers.google.com/oauthplayground/
2. Select: Drive API v3 >> https://www.googleapis.com/auth/drive.readonly
3. Authorize API
4. Refresh and copy the access token
5. Run: `python3 ./gdown.py $access_token $file_id`
6. The the output path of downloaded file could be specified by option `-o $output_path` specify, or ./$filename by default.

## ~~pulse_vpn.py~~

**!!!Deprecated: HKUST-GZ dosen't support PulseSecure VPN since May 2025. Now the university use EasyConnect instead.**

RECOMMEND: Use the open source 3rd party client [EasierConnect](https://github.com/lyc8503/EasierConnect):

- Works on Windows 11 ARM.
- However, [Ncat](https://nmap.org/download.html) is required to proxy the ssh traffics. DNS seems not work properly.
- Usage: `ssh user@ip.addr.hpc.login -o ProxyCommand='ncat.exe --proxy-type socks5 --proxy 127.0.0.1:1080 %h %p'`

## hpcget.py

Getting your hpc instances infomation inside hpc, especially **real ip & port**.

Usage (In Login / Management / mgmt HPC Node):

`python3 hpcget.py`

The output format could be specified by option `-f $format`, or ssh_config, which could be copied into ~/.ssh/config, by default.

> **Note:**
> This script could also be run inside an hpc instance rather than mgmt node.
> However, ip address of the result instances could not be resolved due to the limited network permission inside the hpc instance.
> Therefore, you may get a wrong ip like `gpu1-42`.

## oh_my_hkust_gz_theme.sh

This is a [oh-my-bash](https://github.com/ohmybash/oh-my-bash) theme based on [cupcake](https://github.com/ohmybash/oh-my-bash/blob/master/themes/cupcake/cupcake.theme.sh)

```
┌─ username 🤖 HpcName(MM-DD-HPCID) 🐍 condaenv 📁 path/to/workspace gitbranch ⌀1 ✗
└❯ red          blue                    violet       yellow
```

Usage:

```bash
mkdir ~/.oh-my-bash/themes/oh_my_hkust_gz/
cp ./oh_my_hkust_gz.theme.sh ~/.oh-my-bash/themes/oh_my_hkust_gz/
```

edit `~/.bashrc`, modify the variable `OSH_THEME='oh_my_hkust_gz'`
