Constraint Satisfaction Problems

![](images/CSP/Slide_1_Image_1.png)

> **[Visual Context: Slide_1_Image_1.png]**
> **Category:** Constraint Satisfaction Problems
> **Core Concept:** CSPs (constraint satisfaction problems) like Sudoku as CSP, domain size calculation
> **Structural Elements:** Node WA, Variable X1, Grid 9x9
> **Logic:** CSPs involve finding valid assignments of variables to constraints
> **Pedagogical Value:** This image is from a lecture on CSP algorithms and related concepts.


## Another type of search problems: Identification

◆ All the above cases are about planning, which is only one type of search problems.

◆ Planning: a sequence of actions. ◆ We care about the path to the goal.

Planning

Identifica tion

◆ Identification: an assignment

Search

◆ We care about the goal itself, not the path. ◆ For example, a taxi firm assigns taxis 𝑎, 𝑏, 𝑐 to customers 𝑥, 𝑦, 𝑧 such that the cost incurred (e.g., fuel) is minimal.

## Search -> Identification -> CSP

![](images/CSP/Slide_3_Image_01.png)

**----- Start of picture text -----**<br>
Identification<br>Planning<br>CSPs (i.e.,<br>Identifica having<br>tion constraints<br>but no<br>Search preferences)<br>**----- End of picture text -----**<br>

◆ Constraint Satisfaction Problems (CSPs): Identification problems have constraints to be satisfied; there is no preference in CSPs.

◆ Constraints refer to hard constraints which a legal solution cannot violate. ◆ Preferences sometimes are referred to as soft constraints (or objectives), where we need to optimise, e.g., to minimise cost.

## CSPs

- A constraint satisfaction problem consists of

  - A set of variables

  - A domain for each variable

  - A set of constraints

- In a CSP, an assignment is complete if every variable has a value, otherwise it is partial. Solutions are complete assignments satisfying all the constraints.

- Example: Module scheduling problem

◆ Variables – Modules: AI1, Data Structure, Software Engineering, OOP, AI2, Neural Computation, Evolutionary Computation… ◆ Domain - year-term: {1-1, 1-2, 2-1, 2-2, 3-1, 3-2} ◆ Constraints - pre-requisites: {AI1 < AI2, OOP < SE…} ◆ Solutions - e.g.: (AI1=1-2, OOP=1-1, AI2=2-2, SE=2-1…)

## Standard Search Problems vs CSPs

◆ Standard Search problems

◆ State is a “black-box”: arbitrary data structure

◆ Goal test can be any function over states

◆ Constraint Satisfaction Problems (CSPs)

◆ State is defined by variables 𝑋1, 𝑋2 ,… with values from domains 𝐷1, 𝐷2, …

◆ Goal test is a set of constraints specifying allowable combinations of values of variables.

◆ An example of a formal representation language, in which many search problems can be abstracted. This allows useful generalpurpose algorithms with more power than standard search algorithms.

Example: Map Colouring for Australia

Problem: Map colouring problem is to paint a map (e.g., via three colours red, green and blue) in such a way that none of adjacent regions can have the same colour.

![](images/CSP/Slide_6_Image_02.png)

◆ Variables: WA, NT, Q, NSW, V, SA, T ◆ Domain: D = {red, green, blue}

◆ Constraints: adjacent regions must have different colours

![](images/CSP/Slide_6_Image_05.png)

- WA ≠ NT, WA ≠ SA, NT ≠ SA, NT ≠ Q,…

- ◆ Solutions: e.g. {WA=red, NT=green,

- Q=red, NSW=green, V=red, SA=blue, T=green}

## Constraint Graphs

◆ Constraint graphs are used to represent relations among constraints in CSPs, where nodes correspond to the variables and arcs reflect the constraints.

![](images/CSP/Slide_7_Image_02.png)

![](images/CSP/Slide_7_Image_03.png)

What is the difference between a constraint graph and a search state graph?

## Example: Einstein Puzzle

Problem: There are two houses, and each house has a different colour (either blue or red), and a different pet (cat, dog or fish). We also have the following constraints: The first house does not have a dog nor fish. The blue house has a fish. Which colour and pet each house has?

- Variables: Colour1, Colour2, Pet1, Pet2

- Domain:

  - Colour1, Colour2 = {blue, red}

  - ◆ Pet1, Pet2 = {cat, dog, fish}

- Constraints:

  - Pet1 ≠ dog, fish

  - If Colour1 = blue, then Pet1 = fish

  - ◆ If Colour2 = blue, then Pet2 = fish ◆ Colour1 ≠ Colour2, Pet1 ≠ Pet2

## Example: Sudoku

Problem: Sudoku is to fill a 9×9 grid with digits so that each column, each row, and each of the regions contain all of the digits from 1 to 9.

- Variables: each open cell

- ◆ Domain: D = {1,2,3,…,9}

- Constraints:

  - Each row contains different numbers

  - Each column contains different numbers

  - Each region contains different numbers

![](images/CSP/Slide_9_Image_07.png)

## How to draw a constraint graph when a constraint relates to more than two variables?

## ◆ Use a square to represent a constraint, and connect all the variables involved in that constraint.

![](images/CSP/Slide_10_Image_02.png)

**----- Start of picture text -----**<br>
all<br>different<br>**----- End of picture text -----**<br>

![](images/CSP/Slide_10_Image_03.png)

## Minesweeper

◆ Minesweeper is a single-player puzzle game. The goal is to not uncover a square that contains a mine; if you've identified a square that you think it is a mine, then you flag it. ◆ When you uncover a square, if the square is a mine, the game ends and you lost. ◆ Otherwise, it is a numbered square indicating how many mines are around it (between 0 and 8). If you uncover all of the squares except for any mines, you win the game.

![](images/CSP/Slide_11_Image_02.png)

## Formalise Minesweeper as a CSP

◆ Variables: ◆ All squares to be uncovered 𝑋1 ,

𝑋 2 ,…

◆ Domain:

◆ 𝐷= {0, 1} , where 0 denotes not a mine and 1 denotes a mine

◆ Constraints:

## ◆ The number on a square is the sum of its neighbour’s values.

![](images/CSP/Slide_12_Image_07.png)

## Minesweeper - example

◆ Variables:

𝑋1 𝑋 𝑋 𝑋 1 , 2 , 3 , 4

◆ 𝑋1 , ◆ Domain:

𝐷= {0, 1} , where 0 denotes not

◆ 𝐷= {0, 1} a mine and 1 denotes a mine.

◆ Constraints:

◆ 𝑋 1 = 1

𝑋 1 + 𝑋2 = 1

◆

𝑋 1 + 𝑋2 + 𝑋3 + 𝑋4 = 3

◆

𝑋 4 = 1

◆

...

◆

![](images/CSP/Slide_13_Image_16.png)

**----- Start of picture text -----**<br>
𝑋<br>1<br>𝑋<br>2<br>𝑋 𝑋<br>4 3<br>**----- End of picture text -----**<br>

## Variety of CSPs

◆ Variables

◆ Finite domains (discrete), e.g. all the preceding examples. ◆ Infinite domains (discrete or continuous), e.g., variables involving time. ◆ Constraints ◆ Unary, binary and high-order constraints; i.e., how many variables involved in a constraint. ◆ CSPs are difficult search problems ◆ If a CSP has 𝑛 variables, the size of each domain is 𝑑 , then there are 𝑂(𝑑[𝑛] ) complete assignments. ◆ For the preceding representation of the 4 × 4 queens puzzle, there are 2[16] complete assignments.

## Real-world CSPs

◆ Assignment problems, e.g. who teaches which class ◆ Timetabling problems, e.g. which class is offered when and where ◆ Hardware configuration ◆ Transportation scheduling ◆ Factory scheduling ◆ Circuit layout ◆ Fault diagnosis

◆ …

Many of CSP problems can also consider the preferences (i.e., objectives), in which case they turn into constrained optimisation problems.

Homework: Cryptarithmetic

Cryptarithmetic is a puzzle where the digits of numbers are represented by letters. Each letter represents a unique digit. The goal is to find the digits such that a given equation is verified. Question: Formalise the cryptarithmetic problem as a CSP, i.e., formally give its variables, domain and constraints.

T W O

-      T  W O

8 3 6

-     8  3  6

* F O U R

* 1 6 7 2
