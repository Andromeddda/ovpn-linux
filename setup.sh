#!/bin/bash

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

echo "checking for dependencies..."

if ! command_exists "python3"; then
  echo "Cannot find python3. Please install."
  exit 1
else
  echo "[+] python3"
fi

if ! command_exists "pip3"; then
  echo "Cannot find pip3. Please install."
  exit 1
else
  echo "[+] pip3"
fi

# добавить openvpn networkmanager networkmanager-openconnect networkmanager-openvpn networkmanager-vpnc 

if ! command_exists "nmcli"; then
  echo "Cannot find nmcli. Please install NetworkManager."
  exit 1
else
  echo "[+] NetworkManager"
fi


echo "Installing setuptools"
python3 -m pip install --upgrade setuptools --break-system-packages
python3 -m pip install -e . --break-system-packages