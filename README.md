# LL(1) and SLR(1) Parser Implementation

## Group Members
- **Samuel Herrera Galvis**
- **Emmanuel Alvarez Castrillon**

## Versions and Tools
- **Operating System**: Compatible with Windows, macOS, and Linux (tested on [specify specific OS version if applicable])
- **Programming Language**: Python 3.11
- **Development Environment**: Visual Studio Code

## Project Description
This project provides tools for analyzing context-free grammars and building parsers using LL(1) and SLR(1) techniques. It is ideal for students and professionals interested in understanding the theory and implementation of parsers and grammar analysis. The project includes the following features:

1. **First and Follow Set Calculation**:
   - The `first_follow.py` module contains the `FirstFollowCalculator` class, which computes the First and Follow sets for a given context-free grammar. These sets are essential for constructing parsing tables for LL(1) and SLR(1) parsers.

2. **Grammar Representation**:
   - The `grammar.py` module defines the `Grammar` class, which represents a context-free grammar. It provides methods to retrieve productions, check for epsilon productions, and represent the grammar as a string.

3. **LL(1) Parser**:
   - The `ll1_parser.py` module implements the `LL1Parser` class, which builds LL(1) parsing tables using First and Follow sets. It also verifies whether a grammar is LL(1) and parses input strings accordingly.

4. **SLR(1) Parser**:
   - The `slr1_parser.py` module contains the `SLR1Parser` class, which constructs SLR(1) parsing tables based on canonical collections of LR(0) items. It verifies whether a grammar is SLR(1) and parses input strings.

5. **Main Program**:
   - The `main.py` script serves as the entry point for the project. It allows users to input a context-free grammar, calculate First and Follow sets, and use either LL(1) or SLR(1) parsers to analyze input strings. The program also determines whether the provided grammar is LL(1), SLR(1), both, or neither.

## Features
- **Interactive Input**: Users can input grammars in a simple format and test parsing of strings.
- **Error Handling**: Clear feedback when the grammar does not conform to LL(1) or SLR(1) properties.
- **Educational Tool**: Perfect for learning and experimenting with parsing techniques and grammar analysis.

## Use Cases
This project is valuable for:
- Learning how parsers work and how to construct them.
- Experimenting with context-free grammars and their parsing.
- Understanding the theory behind LL(1) and SLR(1) parsing techniques.

## Installation and Setup Instructions

### Prerequisites
Make sure you have the following installed on your system:
1. **Python 3.11**: Download and install it from [Python's official website](https://www.python.org/downloads/).
2. **Visual Studio Code**: Install it from [Visual Studio Code's official website](https://code.visualstudio.com/).

### Steps to Run the Implementation
1. Clone this repository to your local machine using the following command:
   ```bash
   git clone https://github.com/Emmanuel0930/Proyecto-LF-Samuel-y-Emmanuel.git

2. When running the program, you will need to input the grammar in the following format:

   n
   S -> a b c
   B -> d e f
   C -> g h i
   D -> j k l
   Where `n` is the number of non-terminals, and each production is separated by a blank space.

3. After providing the grammar, the program may present you with three possible scenarios:

- **Case 1: The grammar is either LL(1) or SLR(1):**
  - Simply input the string you want to analyze.

- **Case 2: The grammar is neither LL(1) nor SLR(1):**
  - In this case, the program will terminate execution.

- **Case 3: The grammar is both LL(1) and SLR(1):**
  - You will be prompted to select a parser:
    ```
    Select a parser (T: for LL(1), B: for SLR(1), Q: exit):
    ```
  - Based on your selection, you can then input the strings you wish to analyze.
