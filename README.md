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

## pulse_vpn.py

Connect to PulseSecure VPN, setting the routing rules in order to use Proxy

Routing rules:
- Only traffics to login.hpc.hkust-gz.edu.cn will go through PulseSecureVPN
- Other traffics keep their default routes.

Usage (recommend running in a virtual machine, with tools to keep running after logging out like `screen`):

`python3 pulse_vpn.py $username $password`

**!!! Known problem: Each time disconnect the VPN, you must reboot your system before reconnect next time.**
