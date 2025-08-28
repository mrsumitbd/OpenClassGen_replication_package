class CaseGroupHandler(object):
    '''Part of the pymongo adapter that handles case groups.
    Case groups are sets of cases with a common group id, for which user assessments are shared.
    '''

    def __init__(self):
        self.case_groups = {}
        self.next_id = 1

    def init_case_group(self, owner):
        '''Initialize a case group, creating entry and marking paired case as belonging to group.

        Args:
          owner(str): institute id
        '''
        case_group_id = self.next_id
        self.next_id += 1
        
        self.case_groups[case_group_id] = {
            'owner': owner,
            'label': f'Case Group {case_group_id}',
            'cases': []
        }
        
        return case_group_id

    def remove_case_group(self, case_group_id):
        '''Remove a case group.

        Args:
            case_group_id
        '''
        if case_group_id in self.case_groups:
            del self.case_groups[case_group_id]

    def case_group_label(self, case_group_id):
        '''Return case group label for case_group.

        Args:
            case_group_id(ObjectId)
        '''
        if case_group_id in self.case_groups:
            return self.case_groups[case_group_id]['label']
        return None

    def case_group_update_label(self, case_group_id, case_group_label):
        '''Change case group label.

        Args:
            case_group_id(ObjectId)
            case_group_label(str)
        '''
        if case_group_id in self.case_groups:
            self.case_groups[case_group_id]['label'] = case_group_label