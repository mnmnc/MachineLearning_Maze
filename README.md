MachineLearning_Maze
====================

Passing Through Maze

## Input
Input data is provided in two files:
  - maze_128x128 
  - maze_16x16

Both contain coordinates for each wall in a maze.

#### Input format:

Two first are x and y coordinates. Last one is an instruction how to draw a wall.

`0 0 0` - means draw in 0,0: one wall down and one wall to the right. `┌`

`0 0 1` - means draw in 0,0: only wall to the right `─`

`0 0 2` - means draw in 0,0: only wall down `│`

`0 0 3` - means draw in 0,0: no wall at all


## Output for Tremaux:
```python
Time spent solving: 0.11201095581054688 seconds
Iterations counted: 14641
Path lenght: 5547
Dead ends lenght: 4547
```
![Maze solved with Tremaux algorithm](https://raw.githubusercontent.com/mnmnc/img/master/tremaux.png)


## Output for Dead End Filler

Long processing time.
```python
Time spent solving: 119.60996007919312 seconds
Iterations counted: 3700
Path length: 0
Dead ends length: 27218
```

![Maze solved with Dead End Filler algorithm](https://raw.githubusercontent.com/mnmnc/img/master/dead_end_filler.png)

## Bonus round 

Tremaux without randomness in path picking step (always picks first one - similar to Wall Follower, although its capable of leaving loops)

![Maze solved with Tremaux algorithm without randomness in path picking step](https://raw.githubusercontent.com/mnmnc/img/master/tremaux_no_randomnes.png)
