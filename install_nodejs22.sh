#!/bin/bash

# Script pour installer nodejs version 22

curl -sL https://deb.nodesource.com/setup_22.x | sudo bash -
sudo apt upgrade
sudo apt install nodejs -y
node --version
