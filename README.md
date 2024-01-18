__Deployment__

Use deploy.sh ``./deploy.sh``

----

__FastAPI installation on Termux__

- ``pkg update && pkg upgrade``
- ``pkg install python`` python-pip included
- ``pip install fastapi[all]`` uvicorn included otherwise install fastapi and uvicorn separately

Some device architectures may encounter the problem building the wheel for the maturin package during fastapi installation. Try install maturin via proot-distro. Login to __proot-distro__ using ``pd login <your-installed-distro>`` (e.g. pd login ubuntu) and run: 
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

__Optional: Setup SSH Server on Termux using openssh__

On Termux (host):
- ``pkg update && pkg upgrade``
- ``pkg install openssh``
- To set password use ``passwd <Termux UID>``. ``whoami`` to see the UID

On remote devices (example for local network):
- If you need to remove the existing host fingerprint``ssh-keygen -R "[<host_name_or_ip>]:8022"``
- Add Termux to known_hosts: ``ssh-keyscan -H <hostname_or_ip> >> ~/.ssh/known_hosts``
- Verify it has successfully added ``ssh-keyscan -H <hostname_or_ip> >> ~/.ssh/known_hosts``
- Access host ``ssh -p 8022 <Termux UID>@<Termux IP Address>``. Example: ssh -p 8022 u0_a254@192.168.0.2. Enter the host password.
  
