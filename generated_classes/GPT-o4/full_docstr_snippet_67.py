class CaseGroupHandler(object):
    '''Part of the pymongo adapter that handles case groups.
    Case groups are sets of cases with a common group id, for which user assessments are shared.
    '''

    def __init__(self, db):
        self.db = db
        self.case_groups = db.case_groups
        self.cases = db.cases

    def init_case_group(self, owner):
        '''Initialize a case group, creating entry and marking paired case as belonging to group.

        Args:
          owner(str): institute id
        '''
        now = datetime.utcnow()
        entry = {
            'owner': owner,
            'label': '',
            'created_at': now,
            'updated_at': now
        }
        result = self.case_groups.insert_one(entry)
        group_id = result.inserted_id
        # mark paired cases as belonging to this new group
        self.cases.update_many(
            {'owner': owner, 'paired_case': True},
            {'$set': {'case_group_id': group_id, 'updated_at': now}}
        )
        return group_id

    def remove_case_group(self, case_group_id):
        '''Remove a case group.

        Args:
            case_group_id
        '''
        if not isinstance(case_group_id, ObjectId):
            case_group_id = ObjectId(case_group_id)
        # delete group
        self.case_groups.delete_one({'_id': case_group_id})
        # unset group from cases
        self.cases.update_many(
            {'case_group_id': case_group_id},
            {'$unset': {'case_group_id': ''}, '$set': {'updated_at': datetime.utcnow()}}
        )

    def case_group_label(self, case_group_id):
        '''Return case group label for case_group.

        Args:
            case_group_id(ObjectId)
        '''
        if not isinstance(case_group_id, ObjectId):
            case_group_id = ObjectId(case_group_id)
        doc = self.case_groups.find_one({'_id': case_group_id}, {'label': 1})
        return doc.get('label') if doc else None

    def case_group_update_label(self, case_group_id, case_group_label):
        '''Change case group label.

        Args:
            case_group_id(ObjectId)
            case_group_label(str)
        '''
        if not isinstance(case_group_id, ObjectId):
            case_group_id = ObjectId(case_group_id)
        self.case_groups.update_one(
            {'_id': case_group_id},
            {'$set': {'label': case_group_label, 'updated_at': datetime.utcnow()}}
        )