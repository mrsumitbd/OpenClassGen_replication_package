class TagService:
    '''The tag service.'''
    
    def __init__(self):
        self._tags = {}  # {term: set of objects}
        self._object_tags = {}  # {object_id: set of (term, user) tuples}
        self._current_user = None
    
    def set_current_user(self, user):
        self._current_user = user

    def tag(self, obj, term, user=None):
        '''Apply a tag on a taggable object.

        If user is None, uses the current logged in user.
        '''
        if user is None:
            user = self._current_user
        
        obj_id = id(obj)
        
        if term not in self._tags:
            self._tags[term] = set()
        self._tags[term].add(obj)
        
        if obj_id not in self._object_tags:
            self._object_tags[obj_id] = set()
        self._object_tags[obj_id].add((term, user))

    def untag(self, obj, term, user=None):
        '''Remove the given tag from the given object.

        See tag().
        '''
        if user is None:
            user = self._current_user
        
        obj_id = id(obj)
        
        if term in self._tags:
            self._tags[term].discard(obj)
            if not self._tags[term]:
                del self._tags[term]
        
        if obj_id in self._object_tags:
            self._object_tags[obj_id].discard((term, user))
            if not self._object_tags[obj_id]:
                del self._object_tags[obj_id]

    def get_objects_tagged_with(self, term):
        '''Returns a list of objects tagged with a given term.'''
        return list(self._tags.get(term, set()))

    def get_tags_applied_on(self, obj):
        '''Returns a list of tags applied on a given document.'''
        obj_id = id(obj)
        tags = self._object_tags.get(obj_id, set())
        return [term for term, user in tags]