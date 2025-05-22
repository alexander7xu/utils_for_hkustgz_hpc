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

If you are interested in using Proxy with EasyConnect, I recommend [NJU-EasyConnect-Script](https://github.com/tangruize/NJU-EasyConnect-Script/) as a multi-platform reference.

However, I will not rewrite the script using EasyConnect, for the below reasons:
- I am using Windows ARM, while EasyConnect doesn't provide ARM versions, including Windows/Linux/MacOS.
- My solution is running it on an Android phone, with [Termux](https://termux.dev/en/) as a SSH Server.
- Secure concern: See [转发给你的同学看看 如何应对与卸载删除它？有什么替代方案？-哔哩哔哩](https://b23.tv/z356yuD). It requires extremely great permissons, while it doesn't update since 2020.

Connect to PulseSecure VPN, setting the routing rules in order to use Proxy

Routing rules:
- Only traffics to login.hpc.hkust-gz.edu.cn will go through PulseSecureVPN
- Other traffics keep their default routes.

Usage (recommend running in a virtual machine, with tools to keep running after logging out like `screen`):

`python3 pulse_vpn.py $username $password`

**!!! Known problem: Each time disconnect the VPN, you must reboot your system before reconnect next time.**

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
