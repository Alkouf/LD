# LD
Liar's Dice game, aka Bluff. With simple graphical interface and AI players

For info on how the game is played see: https://en.wikipedia.org/wiki/Liar%27s_dice#Common_hand

The game can be played via graphical user interface (GUI) or via the terminal, by running the files GUI.py and GameCLI.py correspondingly. 
Is recommened to use the GUI option (the terminal one is bereft of functionalities).

The AI's main tool to define their strategy are the probabilities that a number of dice exist out of a set of unkonwn dice. 
E.g. if the opponents have 10 dice together how probable it is to exist at least 3 fives.

There are two types of opponents to select:
* Type 1: (PlayerSimpleAI) It's strategy is to minimize the probability to lose by selecting the safest option each time. 
* Type 2: (PlayerAImk2) Incorporates weights for each possible option using softmax function, and uses them to select what to play. 
That way it is more diffiult to decode the AI's hand. 
Moreover, it uses information from previous bids, that is consider what the previous players played and infers what they might have. 


Additionally, there is the option to calculate the probabilities standalone with its own graphical interface. Run file probabilities.py.
