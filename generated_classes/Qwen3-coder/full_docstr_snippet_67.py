class CaseGroupHandler(object):
    '''Part of the pymongo adapter that handles case groups.
    Case groups are sets of cases with a common group id, for which user assessments are shared.
    '''

    def __init__(self, database):
        '''Initialize the handler with a database connection.
        
        Args:
            database: pymongo database instance
        '''
        self.db = database
        self.case_groups = self.db.case_groups
        self.cases = self.db.cases

    def init_case_group(self, owner):
        '''Initialize a case group, creating entry and marking paired case as belonging to group.

        Args:
          owner(str): institute id
        '''
        from bson import ObjectId
        
        # Create a new case group
        case_group_doc = {
            'owner': owner,
            'label': 'Unnamed Group',
            'created_at': datetime.utcnow(),
            'cases': []
        }
        
        result = self.case_groups.insert_one(case_group_doc)
        return result.inserted_id

    def remove_case_group(self, case_group_id):
        '''Remove a case group.

        Args:
            case_group_id
        '''
        from bson import ObjectId
        
        if isinstance(case_group_id, str):
            case_group_id = ObjectId(case_group_id)
            
        # Remove the case group
        result = self.case_groups.delete_one({'_id': case_group_id})
        
        # Also remove references to this group from cases
        self.cases.update_many(
            {'case_group': case_group_id},
            {'$unset': {'case_group': ''}}
        )
        
        return result.deleted_count

    def case_group_label(self, case_group_id):
        '''Return case group label for case_group.

        Args:
            case_group_id(ObjectId)
        '''
        from bson import ObjectId
        
        if isinstance(case_group_id, str):
            case_group_id = ObjectId(case_group_id)
            
        case_group = self.case_groups.find_one({'_id': case_group_id})
        if case_group:
            return case_group.get('label', 'Unnamed Group')
        return None

    def case_group_update_label(self, case_group_id, case_group_label):
        '''Change case group label.

        Args:
            case_group_id(ObjectId)
            case_group_label(str)
        '''
        from bson import ObjectId
        
        if isinstance(case_group_id, str):
            case_group_id = ObjectId(case_group_id)
            
        result = self.case_groups.update_one(
            {'_id': case_group_id},
            {'$set': {'label': case_group_label}}
        )
        return result.modified_count