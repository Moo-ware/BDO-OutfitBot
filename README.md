![sniper](https://github.com/Moo-ware/BDO-Outfit-Bot/assets/56319809/a578d909-45c4-4cb6-b385-7274a47d1659)
## DISCLAIMER
This program is for educational purposes only. I am **NOT** responsible if you use it and gets banned.

## **Supported Versions**
Currently, steam accounts and OTP enabled accounts are **NOT SUPPORTED**. Only launcher accounts with no OTP is supported. Links are set to NA but can be changed to other regions.

## About the project
Just a little test program I made for the game *Black Desert Online*, that will automatically buy any outfits listed on the central marketplace, faster than manual. I mainly made this as a proof of concept.


### How it works
When enabled, the program will continuously check for outfit stock, with a pre set delay. When outfits are detected, the program will automatically buy it for you.


For the buying to work, the program will need your login credentials to login to the [official](https://na-trade.naeu.playblackdesert.com/Intro/) BDO web-marketplace. Your credentials are then saved locally, and the program will auto-relogin for you if the login expires. This means that the program will work indefinitely as long as you keep it running.


## Issues
Program is still in BETA, so there will most likely be some issues or bugs. Please let me know if you found any.

## Getting Started
Follow these steps for installation.

### Prerequisites
- Latest version of [Python](https://www.python.org/downloads/windows/)

### Installation
To install, paste these commands into your CMD.

1. Clone the repo and navigate
```
git clone https://github.com/Moo-ware/BDO-OutfitBot.git

cd BDO-OutfitBot

```

2. Install required dependencies
```
pip install -r requirements.txt

```

### Running the program
To run the program, simply navigate to the program directory, and paste this into cmd
```
python main.py

```
