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
        self.fail = None
        self.output = []

    def __repr__(self):
        '''
        Textual representation of node.
        '''
        return f"TrieNode(char={self.char!r}, children={list(self.children.keys())}, fail={id(self.fail)}, output={self.output})"