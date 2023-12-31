__Deployment__

Use deploy.sh ``./deploy.sh``

----

__Crucial FastAPI requirements and installation on Termux__

- ``pkg update && pkg upgrade``
- ``pkg install python`` python-pip included
- ``pip install fastapi[all]`` uvicorn included otherwise install fastapi and uvicorn separately.
- ``pip list`` and verify the fastapi and uvicorn is installed

If you got error *'Building wheel for maturin (pyproject.toml) did not run successfully.'*. Install maturin using below steps:
- ``pkg install rust``
- ``rustc update``
- ``pip install maturin``
- ``pip install fastapi[all]``

If still facing same error, try to install rust via proot-distro. Login to __proot-distro__ using ``pd login <your-installed-distro>`` (i.e. pd login ubuntu) and run: 
- ``apt update``
- ``apt upgrade``
- ``apt install make``
- ``apt install cmake``
- ``curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh``
- ``rustup update``
- ``source $HOME/.cargo/env``
- ``cargo install maturin``
- ``pip install fastapi[all]``

____

__Setup SSH Server using openssh__

On Termux (host):
- ``pkg update && pkg upgrade``
- ``pkg install openssh``
- Use ``whoami`` to see the UID
- To set password use ``passwd <Termux UID>``
- 

On remote device:
- ``ssh-keygen -R "[<host_name_or_ip>]:8022"`` to remove the old host fingerprint if existed
- If you already know the IP of host name of Termux add it to known_hosts: ``ssh-keyscan -H <hostname_or_ip> >> ~/.ssh/known_hosts``
- Verify known host is  ``ssh-keyscan -H <hostname_or_ip> >> ~/.ssh/known_hosts``
- Accessing from remote device in the same network ``ssh -p 8022 <Termux UID>@<Termux IP Address>``.
Example: ssh -p 8022 u0_a254@192.168.0.2. Enter the host password.
  
