class TagService:
    '''The tag service.'''

    def __init__(self):
        self.tags = {}  # obj_id -> {term: user}
        self.objects_by_tag = {}  # term -> set of obj_ids

    def _get_user(self, user):
        '''Helper to get current user if none provided.'''
        if user is not None:
            return user
        # In a real implementation, this would get the current logged in user
        # For now, we'll return a default user identifier
        return "current_user"

    def _get_obj_id(self, obj):
        '''Helper to get a consistent identifier for an object.'''
        return id(obj)

    def tag(self, obj, term, user=None):
        '''Apply a tag on a taggable object.

        If user is None, uses the current logged in user.
        '''
        user = self._get_user(user)
        obj_id = self._get_obj_id(obj)
        
        if obj_id not in self.tags:
            self.tags[obj_id] = {}
        
        # Store the tag with the user who applied it
        self.tags[obj_id][term] = user
        
        # Update the reverse index
        if term not in self.objects_by_tag:
            self.objects_by_tag[term] = set()
        self.objects_by_tag[term].add(obj_id)

    def untag(self, obj, term, user=None):
        '''Remove the given tag from the given object.

        See tag().
        '''
        user = self._get_user(user)
        obj_id = self._get_obj_id(obj)
        
        if obj_id in self.tags and term in self.tags[obj_id]:
            # In a real implementation, you might want to check if the user
            # has permission to remove this tag
            del self.tags[obj_id][term]
            
            # Clean up empty dictionaries
            if not self.tags[obj_id]:
                del self.tags[obj_id]
            
            # Update the reverse index
            if term in self.objects_by_tag:
                self.objects_by_tag[term].discard(obj_id)
                
                # Clean up empty sets
                if not self.objects_by_tag[term]:
                    del self.objects_by_tag[term]

    def get_objects_tagged_with(self, term):
        '''Returns a list of objects tagged with a given term.'''
        if term not in self.objects_by_tag:
            return []
        
        # In a real implementation, you would return the actual objects
        # For now, we'll return the object IDs
        return list(self.objects_by_tag[term])

    def get_tags_applied_on(self, obj):
        '''Returns a list of tags applied on a given document.'''
        obj_id = self._get_obj_id(obj)
        
        if obj_id not in self.tags:
            return []
        
        return list(self.tags[obj_id].keys())