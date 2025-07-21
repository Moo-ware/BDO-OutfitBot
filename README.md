![315768101-a578d909-45c4-4cb6-b385-7274a47d1659](https://github.com/Moo-ware/BDO-OutfitBot/assets/56319809/23157a97-7b80-4274-80c0-68b406f92ec2)

## DISCLAIMER
I mainly made this as a proof of concept, and it is for educational purposes only. Therefore, I am **NOT** responsible if you use it and get banned.

## **Supported Versions**
WORKING AS OF 7/14/25. If you are having problems, please message me on Discord (see below)

Currently, Steam accounts and OTP enabled accounts are **NOT SUPPORTED**. Only launcher accounts with no OTP are supported. Steam is WIP.

## About the project
Program I made for the game *Black Desert Online*, that will automatically and instantly buy any outfits listed on the central marketplace. I am still learning, so there probably will be plenty of bugs :)


### How it works
When enabled, the program will continuously check the outfit category for stock, with a preset delay. If a stock or stocks are detected, the program will automatically buy them for you.


For the buying to work, the program will need your login credentials to log in to the [official](https://na-trade.naeu.playblackdesert.com/Intro/) BDO web marketplace. Your credentials are then saved locally, and the program will auto-relogin for you if the login expires. This means that the program will work indefinitely (though not recommended) as long as you keep it running.

## Known Issues
If your IP reputation is low, you will encounter CAPTCHAs that the program currently will not bypass. If you are having issues logging in, this is most likely the issue. To confirm, try logging in manually on [BDO website](https://www.naeu.playblackdesert.com/en-US/Main/Index) and see if you get prompted by CAPTCHA.

If you encounter `unexpected result code 34` when attempting to make a purchase, it is normal. It simply means that the outfit has gone out of stock, and it is trying to place a pre-order for it when you already have an existing pre-order.

`unexpected result code -14` means price mismatch, most commonly caused by an outfit not being listed at the capped price. 

## Credits
decoder.py is by [shrddr](https://github.com/shrddr/huffman_heap)

## Contact me
For questions or bug reports, please message me on Discord: `._.__.__._._.__._____.__._.___.` (Yes this is the username)

## WIP / TODO ##
- Better security
- Steam account compatibility
- Spending limit
- Better UI



