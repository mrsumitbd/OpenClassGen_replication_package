class TagService:
    '''The tag service.'''

    def __init__(self):
        # Map each object to a set of tag terms
        self._tags_by_obj = {}
        # Map each tag term to a set of objects
        self._objs_by_tag = {}

    def tag(self, obj, term, user=None):
        '''Apply a tag on a taggable object.

        If user is None, uses the current logged in user.
        '''
        # Add the term to the object's tag set
        self._tags_by_obj.setdefault(obj, set()).add(term)
        # Add the object to the term's object set
        self._objs_by_tag.setdefault(term, set()).add(obj)

    def untag(self, obj, term, user=None):
        '''Remove the given tag from the given object.

        See tag().
        '''
        # Remove the term from the object's tag set
        tags = self._tags_by_obj.get(obj)
        if tags and term in tags:
            tags.remove(term)
            if not tags:
                del self._tags_by_obj[obj]
        # Remove the object from the term's object set
        objs = self._objs_by_tag.get(term)
        if objs and obj in objs:
            objs.remove(obj)
            if not objs:
                del self._objs_by_tag[term]

    def get_objects_tagged_with(self, term):
        '''Returns a list of objects tagged with a given term.'''
        return list(self._objs_by_tag.get(term, []))

    def get_tags_applied_on(self, obj):
        '''Returns a list of tags applied on a given document.'''
        return list(self._tags_by_obj.get(obj, []))