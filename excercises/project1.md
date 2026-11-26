# Project 1: Iterated Prisoner's Dilemma

This project requires skills taught in the data_structures, functions, control_flow, computational_complexity, and dependencies files.

## Explanation

In the prisoner's dilemma, two players are each given the choice to either cooperate or defect. The payoff for each player depends on the combination of choices made by both players. For example, in this version, you get the highest payoff if you defect while the other player cooperates, but if both players defect, they both get a low payoff. If both players cooperate, they both get a moderate payoff:

| Player 1  | Player 2  | Player 1 payoff | Player 2 payoff |
|-----------|-----------|-----------------|-----------------|
| Cooperate | Cooperate | 3               | 3               |
| Cooperate | Defect    | 0               | 5               |
| Defect    | Cooperate | 5               | 0               |
| Defect    | Defect    | 1               | 1               |

With only one round, the best strategy in this version is to defect (50% change you get 5, 50% you get 1). If you cooperate, there's a 50% chance you get 3 and 50% you get 0.

But the strategy for a game like this gets complicated if the game is played multiple times, because you can learn about your opponent and adjust your strategy accordingly. For example, if your opponent defects in the first round, you might want to defect in the second round as well (otherwise you're a פראייר). But if your opponent cooperates in the first round, you might want to cooperate in the second round as well.

In the 1980s, Robert Axelrod ran a tournament of strategies for the iterated prisoner's dilemma (just like the one you are about to make), and found that the best strategy was "tit-for-tat", which cooperates on the first move, and then copies the opponent's last move for subsequent rounds. This shows how altruism (tending to cooperate) can be an optimal strategy even for self-interested agents.

## Project

In pairs or individually, you will implement a simple version of the iterated prisoner's dilemma in Python or R (your choice). It will be able to take two strategies as input, and play a number of rounds of the game, returning the total score for each player. You will also implement at least two strategies, and test them against each other.

The project will be turned in as a repository on GitHub (just publish the repository publically on Github, using the same account you used for the last assignment).

### Requirements

1. A function `play_game(strategy1, strategy2, rounds, game)` that takes two strategies, the number of rounds to play, and a specification of the game (what the payoffs are for each combination of moves). It should return the total score for each player after all rounds have been played.

2. At least two strategies: functions that take the history of moves and return the next move. For example, a simple strategy might be to always cooperate, while another might be to choose randomly. A more complex strategy might be to cooperate on the first move, and then copy the opponent's last move for subsequent rounds (tit-for-tat). An even more complex strategy might be to cooperate on the first move, and then to play the move that would have given the opponent the highest score in the previous round (the "best response" strategy).

3. Run at least two games (in a reproducible way) and record the results in comments.

4. A set of tests that demonstrate that your functions work as expected.

5. A README.md file that explains what is in the repo and how to use it.

6. **BONUS:** A function `play_tournament(strategies, games_per_pair, rounds_per_game, game)` that takes a list of strategies and plays a round-robin tournament (playing each strategy against every other strategy `games_per_pair` times), and returns the total score for each strategy after all rounds have been played.

### Reminders

- Organize your repo into short files so that it is easy to remember where everything is

- Write clear names for functions, parameters, objects, folders, etc. (in camel_case)

- Write short, informative comments that make it easier to read the code

- The results of simulated games should be **reproducible** (other people should be able to clone the repo to their computer and get the same results)