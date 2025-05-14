"""
Grammar module for the LL(1) and SLR(1) parser implementation.
This module provides the Grammar class to represent context-free grammars.
"""

class Grammar:
    """
    A class representing a context-free grammar.
    """
    
    def __init__(self, productions):
        """
        Initialize the grammar from a dictionary of productions.
        
        Args:
            productions (dict): A dictionary mapping non-terminals to lists of productions
        """
        self.productions = productions
        
        # The first non-terminal is considered the start symbol
        self.start_symbol = next(iter(productions)) if productions else None
        
        # Extract terminals and non-terminals
        self.non_terminals = set(productions.keys())
        
        # Find all terminals
        self.terminals = set()
        for rhs_list in productions.values():
            for rhs in rhs_list:
                for symbol in rhs:
                    # No terminals son mayúsculas, terminales no son mayúsculas
                    if symbol != 'e' and not symbol[0].isupper():
                        self.terminals.add(symbol)
        
        # Add end marker to terminals
        self.terminals.add('$')
        
        # Normalize the productions to handle epsilon
        self._normalize_productions()
    
    def _normalize_productions(self):
        """
        Normalize productions by converting string lists to tuples.
        Also handles epsilon ('e') productions.
        """
        normalized = {}
        
        for lhs, rhs_list in self.productions.items():
            normalized[lhs] = []
            
            for rhs in rhs_list:
                if rhs == 'e':
                    # Epsilon production
                    normalized[lhs].append(())
                else:
                    # Create a tuple from the RHS
                    normalized[lhs].append(tuple(rhs))
        
        self.productions = normalized
    
    def get_productions(self, non_terminal):
        """
        Get all productions for a given non-terminal.
        
        Args:
            non_terminal (str): The non-terminal symbol
            
        Returns:
            list: A list of tuples representing the productions for the non-terminal
        """
        return self.productions.get(non_terminal, [])
    
    def get_all_productions(self):
        """
        Get all productions in the grammar.
        
        Returns:
            list: A list of tuples (lhs, rhs) where lhs is a non-terminal and rhs is a tuple of symbols
        """
        all_productions = []
        
        for lhs, rhs_list in self.productions.items():
            for rhs in rhs_list:
                all_productions.append((lhs, rhs))
        
        return all_productions
    
    def has_epsilon_production(self, non_terminal):
        """
        Check if a non-terminal has an epsilon production.
        
        Args:
            non_terminal (str): The non-terminal symbol
            
        Returns:
            bool: True if the non-terminal has an epsilon production, False otherwise
        """
        for rhs in self.productions.get(non_terminal, []):
            if len(rhs) == 0:  # Empty tuple means epsilon
                return True
        
        return False
    
    def __str__(self):
        """
        Return a string representation of the grammar.
        
        Returns:
            str: A string representation of the grammar
        """
        result = []
        
        for lhs, rhs_list in self.productions.items():
            rhs_strings = []
            
            for rhs in rhs_list:
                if len(rhs) == 0:
                    rhs_strings.append('e')
                else:
                    rhs_strings.append(' '.join(rhs))
            
            result.append(f"{lhs} -> {' | '.join(rhs_strings)}")
        
        return '\n'.join(result)
