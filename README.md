﻿# Flappy Bird bot

Flappy bird bot trained with a genetic algorithm.
It takes into account:
- distance on the x axis to the next pylon
- distance on the y axis to the center of the gap between the pylons
- speed on the y axis of the bird

It starts with a population of 100 birds with random coeficients, and the last 10 to survive are combined and mutated to obtain the population (better) for the next training iteration. 
After 30 training iterations the most suitable coeficients are obtained.
