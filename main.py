#!/usr/bin/env python3
"""
Main program for the LL(1) and SLR(1) parser implementation.
This program reads a context-free grammar, calculates First and Follow sets,
and builds LL(1) and SLR(1) parsing tables if possible.
"""

import sys
from grammar import Grammar
from first_follow import FirstFollowCalculator
from ll1_parser import LL1Parser
from slr1_parser import SLR1Parser


def main():
    """
    Main function to process grammar input and perform parsing.
    """
    print("Welcome to the parsers LL(1) y SLR(1).\nPlease enter the grammar in the following format:")
    print("n\nA -> a b c\nB -> d e f\nC -> g h i\nD -> j k l")
    print("Where n is the number of non-terminals and each production is separated by a blank space.")
    # Read the grammar
    grammar = read_grammar()
    
    # Calculate First and Follow sets
    ff_calculator = FirstFollowCalculator(grammar)
    first_sets = ff_calculator.compute_first()
    follow_sets = ff_calculator.compute_follow()
    
    # Create parsers
    ll1_parser = LL1Parser(grammar, first_sets, follow_sets)
    slr1_parser = SLR1Parser(grammar, first_sets, follow_sets)
    
    # Check if the grammar is LL(1) and/or SLR(1)
    is_ll1 = ll1_parser.is_ll1()
    is_slr1 = slr1_parser.is_slr1()
    
    # Process based on grammar type
    if is_ll1 and is_slr1:
        process_ll1_slr1(ll1_parser, slr1_parser)
    elif is_ll1:
        print("The grammar is LL(1).")
        print("Using the LL(1) parser, please enter the string to be parsed: ")
        process_ll1(ll1_parser)
    elif is_slr1:
        print("The grammar is SLR(1).")
        print("Using the SLR1(1) parser, please enter the string to be parsed: ")
        process_slr1(slr1_parser)
    else:
        print("The grammar is neither LL(1) nor SLR(1).")


def read_grammar():
    """
    Read the grammar from standard input.
    
    Returns:
        Grammar: The parsed grammar object
    """
    try:
        # Read the number of non-terminals
        n = int(input().strip())
        
        # Read the productions
        productions = {}
        for _ in range(n):
            line = input().strip()
            
            # Split by "->"
            parts = line.split("->")
            if len(parts) != 2:
                raise ValueError(f"Invalid production format: {line}")
            
            # Get the non-terminal and its productions
            non_terminal = parts[0].strip()
            alternatives = parts[1].strip().split()
            
            # Process alternatives (they may be presented as 'a|b|c')
            processed_alternatives = []
            
            for alt in alternatives:
                # Check if it's a composite alternative with '|'
                if '|' in alt:
                    # Split by '|' and add each part as a separate alternative
                    for sub_alt in alt.split('|'):
                        if sub_alt:  # Skip empty parts
                            processed_alternatives.append(sub_alt)
                else:
                    processed_alternatives.append(alt)
            
            if non_terminal in productions:
                productions[non_terminal].extend(processed_alternatives)
            else:
                productions[non_terminal] = processed_alternatives
        
        # Create the grammar object
        return Grammar(productions)
    except ValueError as e:
        print(f"Error reading grammar: {e}")
        sys.exit(1)


def process_ll1_slr1(ll1_parser, slr1_parser):
    """
    Process input strings when the grammar is both LL(1) and SLR(1).
    
    Args:
        ll1_parser: The LL(1) parser
        slr1_parser: The SLR(1) parser
    """
    while True:
        print("Select a parser (T: for LL(1), B: for SLR(1), Q: exit):")
        choice = input().strip().upper()
        
        if choice == 'Q':
            break
        elif choice == 'T':
            print("Using the LL(1) parser, please enter the string to be parsed: ")
            process_parser(ll1_parser)
        elif choice == 'B':
            print("Using the SLR(1) parser, please enter the string to be parsed: ")
            process_parser(slr1_parser)
        else:
            # Invalid choice, ask again
            continue


def process_ll1(parser):
    """
    Process input strings using an LL(1) parser.
    
    Args:
        parser: The LL(1) parser
    """
    process_parser(parser)


def process_slr1(parser):
    """
    Process input strings using an SLR(1) parser.
    
    Args:
        parser: The SLR(1) parser
    """
    process_parser(parser)


def process_parser(parser):
    """
    Process input strings using the provided parser.
    
    Args:
        parser: The parser to use (LL(1) or SLR(1))
    """
    while True:
        input_string = input().strip()
        if not input_string:
            break
        
        # Make sure the input string ends with $
        if not input_string.endswith('$'):
            input_string += '$'
            
        # Parse the input string
        is_accepted = parser.parse(input_string)
        
        # Print the result
        print("Yes" if is_accepted else "No")
        print("To exit, press enter")


if __name__ == "__main__":
    main()
