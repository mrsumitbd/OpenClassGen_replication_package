class TrieNode(object):
    '''
    Node of trie/Aho-Corasick automaton
    '''

    def __init__(self, char):
        '''
        Constructs an empty node
        '''
        self.char = char
        self.children = {}
        self.is_end_of_word = False
        self.failure_link = None
        self.output_link = None
        self.patterns = []

    def __repr__(self):
        '''
        Textual representation of node.
        '''
        return f"TrieNode('{self.char}')"