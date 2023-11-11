# Search-Algorithms

This project centers around the exploration of diverse AI search algorithms, encompassing both uninformed and informed approaches, to address a challenge involving agent movement and the optimization of paths. The primary objective is to implement and compare these algorithms to efficiently solve the specified problem.

## Overview

The scenario involves a map with `n` rows and `m` columns, featuring an agent positioned at the starting point (0, 0). The map also includes allies, gates, and orcs, each proximity to the agent resulting in health loss. The agent's mission is to locate allies, escort them to the gates, and safeguard health to avoid defeat.

## Implemented Algorithms

### Uninformed Search Strategies
- **BFS (Breadth-First Search):** Explores the search space solely based on information from the problem definition.
- **IDS (Iterative Deepening Depth-First Search):** A strategy that blends the space efficiency of depth-first search with the completeness of breadth-first search.

### Informed Search Strategy
- **A\* (A-Star):** Leverages heuristic functions to determine the most promising path to the goal state.

## Project Goals

This project strives to achieve the following objectives:
1. Clarify the terms 'Agent' and 'State' within the realm of AI search strategies.
2. Implement BFS (Breadth-First Search).
3. Implement IDS (Iterative Deepening Depth-First Search).
4. Formulate a heuristic function.
5. Define an evaluation function.
6. Implement the A\* (A-Star) algorithm.

By accomplishing these objectives, the project aims to delve into and apply a variety of AI search algorithms tailored to the given challenge, providing valuable insights into their performance and efficacy.
