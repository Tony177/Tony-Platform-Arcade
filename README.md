[![DeepSource](https://deepsource.io/gh/Tony177/Tony-Platform-Arcade.svg/?label=resolved+issues&show_trend=true)](https://deepsource.io/gh/Tony177/Tony-Platform-Arcade/?ref=repository-badge)
# Tony177's Platform Arcade
Simple platform game created for educational and learning purpose.

## Game Logic
### Button
- Press A,D or ARROW LEFT, RIGHT to move
- Press W or ARROW UP or SPACE to jump
- Press S or ARROW DOWN to move down on ladder
- Press ESC to open menu

### Logic
If you collect 100 coins you get an extra life  
If you lose all the lifes you've lost the game\
Click with the mouse to start character selection\
Click on one of the four image to select a character\
You save the game every time you leave the game from Pause Menu

## Structure of the game
Game's Feature to implement/implemented:
- Movement and Physics Engine :heavy_check_mark:
- First chapter (still uncomplete):heavy_check_mark:
- Death objects :heavy_check_mark:
- Simple sound (picking coin and death) :heavy_check_mark:
- Multiple layer map :heavy_check_mark:
- Other chapter (still unknown number) :x:
- Enemies :x:
- Background Music :heavy_check_mark:
- General Objective of the game :x:
- Simple animation of the images :heavy_check_mark:
- Selection of various characters :heavy_check_mark:
- Starting View with various function :x:
- Game Over View :x:
- Moving Platform :x:
- Level Menu :x:
- Pause Menu (ESC) interface (works but it's ugly) :x:
- Control Volume on Pause Menu :heavy_check_mark:
- Generate config file to save user settings :heavy_check_mark:
- Added encryption and decryption with Fernet Cryptography :heavy_check_mark:
- Implemented Load and Save function (handling crypted file) :heavy_check_mark:

Ideas:
- Add some kind of lore
- Add a clear single and final enemy/objective
- Beatify graphical contents

## Cryptography
Using the <b><i>Fernet Cryptography Module</b></i>, the saving file is encrypted/decrypted using the game_key.key generated with [key.py](#key.py) program\
Upon generating a key it can be used to encrypt (encrypt function) and to decrypt (decrypt function)

## Thanks
This game experiment is possible thanks to [Arcade Library](https://github.com/pythonarcade/arcade), and to the free image and sound sample offered by https://kenney.nl/