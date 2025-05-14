"""
LL(1) parser implementation.
This module provides the functionality to build and use an LL(1) parsing table.
"""

class LL1Parser:
    """
    A class representing an LL(1) parser.
    """
    
    def __init__(self, grammar, first_sets, follow_sets):
        """
        Initialize the LL(1) parser.
        
        Args:
            grammar: The grammar to parse
            first_sets: The First sets for the grammar
            follow_sets: The Follow sets for the grammar
        """
        self.grammar = grammar
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.parsing_table = None
        try:
            self.parsing_table = self._build_parsing_table()
        except ValueError:
            # Grammar is not LL(1)
            pass
    
    def _build_parsing_table(self):
        """
        Build the LL(1) parsing table.
        
        Returns:
            dict: A dictionary representing the LL(1) parsing table
            
        Raises:
            ValueError: If the grammar is not LL(1)
        """
        table = {}
        
        # Initialize the table with empty dictionaries
        for non_terminal in self.grammar.non_terminals:
            table[non_terminal] = {}
        
        # Build the parsing table
        for lhs in self.grammar.non_terminals:
            for rhs in self.grammar.get_productions(lhs):
                # Calculate the First set of the right-hand side
                first_of_rhs = self._first_of_sequence(rhs)
                
                # For each terminal in First(rhs), add the production to the table
                for terminal in first_of_rhs:
                    if terminal != 'e':
                        if terminal in table[lhs]:
                            # Conflict detected
                            raise ValueError(f"LL(1) parsing table conflict at [{lhs}, {terminal}]")
                        else:
                            table[lhs][terminal] = rhs
                
                # If epsilon is in First(rhs), add the production to the table for each terminal in Follow(lhs)
                if 'e' in first_of_rhs:
                    for terminal in self.follow_sets[lhs]:
                        if terminal in table[lhs]:
                            # Conflict detected
                            raise ValueError(f"LL(1) parsing table conflict at [{lhs}, {terminal}]")
                        else:
                            table[lhs][terminal] = rhs
        
        return table
    
    def _first_of_sequence(self, sequence):
        """
        Calculate the First set of a sequence of symbols.
        
        Args:
            sequence (tuple): A sequence of grammar symbols
            
        Returns:
            set: The First set of the sequence
        """
        if not sequence:
            return {'e'}
        
        result = set()
        all_nullable = True
        
        for symbol in sequence:
            # If it's a terminal, add it and stop
            if symbol in self.grammar.terminals:
                result.add(symbol)
                all_nullable = False
                break
            
            # If it's a non-terminal, add all non-epsilon symbols from its First set
            for s in self.first_sets[symbol] - {'e'}:
                result.add(s)
            
            # If this symbol can't derive epsilon, we're done
            if 'e' not in self.first_sets[symbol]:
                all_nullable = False
                break
        
        # If all symbols can derive epsilon, add epsilon to the result
        if all_nullable:
            result.add('e')
        
        return result
    
    def is_ll1(self):
        """
        Check if the grammar is LL(1).
        
        Returns:
            bool: True if the grammar is LL(1), False otherwise
        """
        return self.parsing_table is not None
    
    def parse(self, input_string):
        """
        Parse an input string using the LL(1) parsing table.
        
        Args:
            input_string (str): The input string to parse
            
        Returns:
            bool: True if the input string is accepted, False otherwise
        """
        # Check if the grammar is LL(1)
        if not self.is_ll1():
            return False
        
        # Transform input string into a list of tokens
        tokens = list(input_string)
        
        # Ensure we have $ at the end if needed
        if not tokens or tokens[-1] != '$':
            tokens.append('$')
        
        # Initialize the stack with the end marker and the start symbol
        stack = ['$', self.grammar.start_symbol]
        
        # Initialize the input pointer
        i = 0
        
        # Parse until the stack is empty or an error occurs
        while stack:
            # Get the top of the stack
            top = stack.pop()
            
            # Get the current input symbol
            if i < len(tokens):
                symbol = tokens[i]
            else:
                # End of input
                symbol = '$'
            
            if top in self.grammar.terminals or top == '$':
                # If the top of the stack is a terminal or the end marker
                if top == symbol:
                    # Match, consume the input
                    i += 1
                else:
                    # Mismatch, error
                    return False
            else:
                # If the top of the stack is a non-terminal
                if top in self.parsing_table and symbol in self.parsing_table[top]:
                    # Get the production to use
                    production = self.parsing_table[top][symbol]
                    
                    # Push the production in reverse order onto the stack (skip epsilon)
                    if production:  # Not an epsilon production
                        for s in reversed(production):
                            stack.append(s)
                else:
                    # No production found, error
                    return False
        
        # Success if we've consumed all input or we're at the $ marker
        return (i == len(tokens)) or (i == len(tokens) - 1 and tokens[i] == '$')
