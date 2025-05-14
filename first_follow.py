"""
First and Follow set calculation for context-free grammars.
This module provides functionality to compute the First and Follow sets.
"""

class FirstFollowCalculator:
    """
    A class for calculating First and Follow sets for a context-free grammar.
    """
    
    def __init__(self, grammar):
        """
        Initialize the calculator with a grammar.
        
        Args:
            grammar: The grammar for which to calculate First and Follow sets
        """
        self.grammar = grammar
        # To keep track of which non-terminals can derive epsilon
        self.nullable = {nt: self.grammar.has_epsilon_production(nt) for nt in self.grammar.non_terminals}
    
    def compute_first(self):
        """
        Compute the First sets for all symbols in the grammar.
        
        Returns:
            dict: A dictionary mapping symbols to their First sets
        """
        # Initialize First sets
        first = {}
        
        # Initialize First sets for terminals
        for terminal in self.grammar.terminals:
            first[terminal] = {terminal}
        
        # Initialize First sets for non-terminals
        for non_terminal in self.grammar.non_terminals:
            first[non_terminal] = set()
            # If the non-terminal directly produces epsilon, add it to its First set
            if self.grammar.has_epsilon_production(non_terminal):
                first[non_terminal].add('e')
        
        # Iterate until no more changes
        changed = True
        while changed:
            changed = False
            
            # Process each production
            for nt in self.grammar.non_terminals:
                for rhs in self.grammar.get_productions(nt):
                    if not rhs:  # Epsilon production
                        if 'e' not in first[nt]:
                            first[nt].add('e')
                            changed = True
                        continue
                    
                    # For terminals directly in the first position
                    if rhs[0] in self.grammar.terminals:
                        if rhs[0] not in first[nt]:
                            first[nt].add(rhs[0])
                            changed = True
                        continue
                    
                    # For non-terminals, calculate First set following the chain
                    all_derive_epsilon = True
                    for symbol in rhs:
                        # Add all non-epsilon symbols from First(symbol)
                        for s in first[symbol] - {'e'}:
                            if s not in first[nt]:
                                first[nt].add(s)
                                changed = True
                        
                        # If this symbol cannot derive epsilon, stop here
                        if 'e' not in first[symbol]:
                            all_derive_epsilon = False
                            break
                    
                    # If all symbols in the production can derive epsilon, add epsilon to First(nt)
                    if all_derive_epsilon and 'e' not in first[nt]:
                        first[nt].add('e')
                        changed = True
        
        return first
    
    def compute_follow(self):
        """
        Compute the Follow sets for all non-terminals in the grammar.
        
        Returns:
            dict: A dictionary mapping non-terminals to their Follow sets
        """
        # Initialize Follow sets
        follow = {nt: set() for nt in self.grammar.non_terminals}
        
        # Add $ to the Follow set of the start symbol
        follow[self.grammar.start_symbol].add('$')
        
        # Get the First sets
        first = self.compute_first()
        
        # Iterate until no more changes
        changed = True
        while changed:
            changed = False
            
            # Process each production
            for nt in self.grammar.non_terminals:
                for rhs in self.grammar.get_productions(nt):
                    if not rhs:  # Skip epsilon productions
                        continue
                    
                    # Process each position in the right-hand side
                    for i in range(len(rhs)):
                        symbol = rhs[i]
                        
                        # Only process non-terminals
                        if symbol not in self.grammar.non_terminals:
                            continue
                        
                        # If it's the last symbol, add Follow(nt) to Follow(symbol)
                        if i == len(rhs) - 1:
                            for s in follow[nt]:
                                if s not in follow[symbol]:
                                    follow[symbol].add(s)
                                    changed = True
                        else:
                            # Process what follows this symbol
                            first_beta = self._compute_first_of_sequence(rhs[i+1:], first)
                            
                            # Add all non-epsilon symbols from First(beta) to Follow(symbol)
                            for s in first_beta - {'e'}:
                                if s not in follow[symbol]:
                                    follow[symbol].add(s)
                                    changed = True
                            
                            # If epsilon is in First(beta), add Follow(nt) to Follow(symbol)
                            if 'e' in first_beta:
                                for s in follow[nt]:
                                    if s not in follow[symbol]:
                                        follow[symbol].add(s)
                                        changed = True
        
        return follow
    
    def _compute_first_of_sequence(self, sequence, first):
        """
        Compute the First set of a sequence of grammar symbols.
        
        Args:
            sequence: A sequence of grammar symbols
            first: The precalculated First sets
            
        Returns:
            set: The First set of the sequence
        """
        if not sequence:
            return {'e'}
        
        result = set()
        all_derive_epsilon = True
        
        for symbol in sequence:
            # Add all non-epsilon symbols from First(symbol)
            result.update(first[symbol] - {'e'})
            
            # If this symbol cannot derive epsilon, we're done
            if 'e' not in first[symbol]:
                all_derive_epsilon = False
                break
        
        # If all symbols can derive epsilon, add epsilon to the result
        if all_derive_epsilon:
            result.add('e')
        
        return result
    
    def _can_derive_epsilon(self, symbol, first):
        """
        Check if a symbol can derive epsilon.
        
        Args:
            symbol (str): The symbol to check
            first (dict): The First sets
        
        Returns:
            bool: True if the symbol can derive epsilon, False otherwise
        """
        return symbol in self.grammar.non_terminals and 'e' in first[symbol]
