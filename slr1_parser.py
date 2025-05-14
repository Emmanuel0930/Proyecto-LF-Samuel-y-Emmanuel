"""
SLR(1) parser implementation.
This module provides the functionality to build and use an SLR(1) parsing table.
"""

class SLR1Parser:
    """
    A class representing an SLR(1) parser.
    """
    
    def __init__(self, grammar, first_sets, follow_sets):
        """
        Initialize the SLR(1) parser.
        
        Args:
            grammar: The grammar to parse
            first_sets: The First sets for the grammar
            follow_sets: The Follow sets for the grammar
        """
        self.grammar = grammar
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.canonical_collection = None
        self.action_table = None
        self.goto_table = None
        
        try:
            self.canonical_collection = self._build_canonical_collection()
            self.action_table, self.goto_table = self._build_parsing_tables()
        except ValueError:
            # Grammar is not SLR(1)
            pass
    
    def _item_closure(self, items):
        """
        Compute the closure of a set of LR(0) items.
        
        Args:
            items (set): A set of LR(0) items represented as (lhs, rhs, dot_pos) tuples
            
        Returns:
            set: The closure of the items
        """
        closure = set(items)
        changed = True
        
        while changed:
            changed = False
            new_items = set()
            
            for lhs, rhs, dot_pos in closure:
                # If the dot is at the end, skip
                if dot_pos >= len(rhs):
                    continue
                
                # Get the symbol after the dot
                next_symbol = rhs[dot_pos]
                
                # If the symbol is a non-terminal, add its productions to the closure
                if next_symbol in self.grammar.non_terminals:
                    for next_rhs in self.grammar.get_productions(next_symbol):
                        new_item = (next_symbol, next_rhs, 0)
                        if new_item not in closure:
                            new_items.add(new_item)
                            changed = True
            
            closure.update(new_items)
        
        return closure
    
    def _goto(self, items, symbol):
        """
        Compute the GOTO function for a set of LR(0) items and a grammar symbol.
        
        Args:
            items (set): A set of LR(0) items
            symbol (str): A grammar symbol
            
        Returns:
            set: The GOTO of the items for the symbol
        """
        goto_items = set()
        
        for lhs, rhs, dot_pos in items:
            # If the dot is at the end, skip
            if dot_pos >= len(rhs):
                continue
            
            # If the symbol after the dot matches the input symbol,
            # add the item with the dot moved one position to the right
            if rhs[dot_pos] == symbol:
                goto_items.add((lhs, rhs, dot_pos + 1))
        
        return self._item_closure(goto_items)
    
    def _build_canonical_collection(self):
        """
        Build the canonical collection of LR(0) items.
        
        Returns:
            list: The canonical collection of LR(0) items
        """
        # Create an augmented grammar item with S' -> S
        augmented_start = "S'"
        start_rhs = (self.grammar.start_symbol,)
        
        # Start with the closure of the initial item
        initial_item = (augmented_start, start_rhs, 0)
        initial_set = self._item_closure({initial_item})
        
        canonical_collection = [initial_set]
        
        # Keep track of states to process
        states_to_process = [0]
        
        # Process states until no more states to process
        while states_to_process:
            state_idx = states_to_process.pop(0)
            state = canonical_collection[state_idx]
            
            # For each grammar symbol
            all_symbols = list(self.grammar.terminals) + list(self.grammar.non_terminals)
            for symbol in all_symbols:
                # Compute the GOTO for the state and the symbol
                goto_set = self._goto(state, symbol)
                
                # If the GOTO is not empty
                if goto_set:
                    # Check if the GOTO is already in the canonical collection
                    for i, existing_state in enumerate(canonical_collection):
                        if goto_set == existing_state:
                            # Already exists, nothing to do
                            break
                    else:
                        # New state, add it to the canonical collection
                        canonical_collection.append(goto_set)
                        states_to_process.append(len(canonical_collection) - 1)
        
        return canonical_collection
    
    def _build_parsing_tables(self):
        """
        Build the ACTION and GOTO tables for the SLR(1) parser.
        
        Returns:
            tuple: A tuple containing the ACTION and GOTO tables
            
        Raises:
            ValueError: If the grammar is not SLR(1)
        """
        if not self.canonical_collection:
            raise ValueError("Cannot build parsing tables without a canonical collection")
        
        action_table = [{} for _ in range(len(self.canonical_collection))]
        goto_table = [{} for _ in range(len(self.canonical_collection))]
        
        # Add transitions from canonical collection
        transitions = {}
        for i, state in enumerate(self.canonical_collection):
            for symbol in list(self.grammar.terminals) + list(self.grammar.non_terminals):
                goto_set = self._goto(state, symbol)
                if goto_set:
                    for j, existing_state in enumerate(self.canonical_collection):
                        if goto_set == existing_state:
                            transitions[(i, symbol)] = j
                            break
        
        # For each state in the canonical collection
        for i, state in enumerate(self.canonical_collection):
            # For each item in the state
            for lhs, rhs, dot_pos in state:
                # If the dot is not at the end
                if dot_pos < len(rhs):
                    # Get the symbol after the dot
                    next_symbol = rhs[dot_pos]
                    
                    # If the symbol is a terminal
                    if next_symbol in self.grammar.terminals:
                        # Get transition state
                        if (i, next_symbol) in transitions:
                            j = transitions[(i, next_symbol)]
                            
                            # Check for conflict
                            if next_symbol in action_table[i]:
                                raise ValueError(f"SLR(1) conflict at state {i}, symbol '{next_symbol}'")
                            
                            # Add a shift action to the ACTION table
                            action_table[i][next_symbol] = ('shift', j)
                else:
                    # The dot is at the end - we have a reduce item
                    # Special case for augmented grammar start production
                    if lhs == "S'" and dot_pos == 1 and rhs[0] == self.grammar.start_symbol:
                        # Add accept action for $
                        if '$' in action_table[i]:
                            raise ValueError(f"SLR(1) conflict at state {i}, symbol '$'")
                        action_table[i]['$'] = ('accept', None)
                    else:
                        # For each terminal in FOLLOW(lhs), add a reduce action
                        for terminal in self.follow_sets[lhs]:
                            if terminal in action_table[i]:
                                raise ValueError(f"SLR(1) conflict at state {i}, symbol '{terminal}'")
                            
                            # Find production index
                            prod_idx = -1
                            for idx, (p_lhs, p_rhs) in enumerate(self.grammar.get_all_productions()):
                                if p_lhs == lhs and p_rhs == rhs:
                                    prod_idx = idx
                                    break
                            
                            action_table[i][terminal] = ('reduce', (lhs, rhs))
            
            # Build the GOTO part of the table
            for non_terminal in self.grammar.non_terminals:
                if (i, non_terminal) in transitions:
                    goto_table[i][non_terminal] = transitions[(i, non_terminal)]
        
        return action_table, goto_table
    
    def is_slr1(self):
        """
        Check if the grammar is SLR(1).
        
        Returns:
            bool: True if the grammar is SLR(1), False otherwise
        """
        return self.action_table is not None and self.goto_table is not None
    
    def parse(self, input_string):
        """
        Parse an input string using the SLR(1) parsing table.
        
        Args:
            input_string (str): The input string to parse
            
        Returns:
            bool: True if the input string is accepted, False otherwise
        """
        # Check if the grammar is SLR(1)
        if not self.is_slr1():
            return False
        
        # Transform input string into tokens
        tokens = list(input_string)
        if not tokens or tokens[-1] != '$':
            tokens.append('$')  # Add end marker
        
        # Initialize the stack with the initial state
        stack = [0]
        
        # Initialize the input pointer
        i = 0
        
        # Parse until the input is accepted or an error occurs
        while True:
            # Get the current state
            state = stack[-1]
            
            # Get the current input symbol
            if i < len(tokens):
                symbol = tokens[i]
            else:
                return False  # Unexpected end of input
            
            # If there's no action table or the symbol is not in it, error
            if self.action_table is None or state not in range(len(self.action_table)) or symbol not in self.action_table[state]:
                return False
            
            # Get the action for the current state and symbol
            action, target = self.action_table[state][symbol]
            
            if action == 'shift':
                # Shift action: push the symbol and the target state onto the stack
                stack.append(symbol)
                stack.append(target)
                i += 1
            elif action == 'reduce':
                # Reduce action: pop 2 * |rhs| symbols from the stack and push the result
                lhs, rhs = target
                
                # Pop 2 * |rhs| symbols from the stack
                if rhs:  # No es producción vacía
                    for _ in range(len(rhs) * 2):
                        stack.pop()
                
                # Get the current state after popping
                current_state = stack[-1]
                
                # Push the lhs and the new state onto the stack
                stack.append(lhs)
                
                # Check if goto table exists and has the required entry
                if self.goto_table is None or current_state not in range(len(self.goto_table)) or lhs not in self.goto_table[current_state]:
                    return False  # No goto action found
                
                goto_state = self.goto_table[current_state][lhs]
                stack.append(goto_state)
            elif action == 'accept':
                # Accept action: the input string is accepted
                return True
            else:
                # Unknown action: the input string is not accepted
                return False
