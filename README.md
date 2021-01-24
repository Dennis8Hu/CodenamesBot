# CodenamesBot
A python Discord bot that allows you to play Codenames on your server.

The premise of the original Codenames game mechanic is simple.
The board starts with 25 cards, 5 columns, and rows, each with a different word.
There are two teams, red and blue, which both have spymasters and operatives.

When the game starts only the spymaster receives a layout of the board where each of the cards gets a color, either red, blue, grey, or black.
He or she then tries to come up with a hint, a word that ties characteristics of as many cards with the team color together.
Along with a number of cards that have to be guessed the spymaster gives his operatives the hint. The goal of the operatives is to find the cards without choosing the opponent's team cards until they have found all the cards of their color.
Choosing grey cards or the opponent's cards means that the turn is switched to the other team. Black cards end the game entirely and the team with the least cards left wins.
#### Commands
Prefix: '$CN'
* list
* listshow
* new
* start
* hint
* guess

#### How to play
To create a new set of cards use ```$CNlist [namelist] [entries seperated by spaces]```.
Lists are limited to 2000 characters due to Discords chat limit.

To show the show the created lists use ```$CNlistshow``` and for the contents of a list use ```$CNlistshow [namelist]```.

Before to start a game or to refresh the teams use ```$CNnew``` this initializes the team list.

```$CNstart``` starts a new game and sends the spymaster and operatives the right game plot.

For the spymaster to send a hint message the bot directly the command ```$CNhint [one-word] [integer]```.

Afterwards the operatives can guess using ```$CNguess [integer]```.