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
        self.fail = None
        self.output = []

    def __repr__(self):
        '''
        Textual representation of node.
        '''
        return f"TrieNode(char='{self.char}', children={list(self.children.keys())}, is_end_of_word={self.is_end_of_word})"