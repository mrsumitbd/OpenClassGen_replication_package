class UploadedFileRelations(object):
    '''
    Contains run method that will be called via project upload file post-processor.
    '''

    def __init__(self, activity):
        '''
        :param activity: CopyActivity: info about the activity associated with the files we are uploading
        '''
        self.activity = activity

    def run(self, data_service, file_details):
        '''
        Attach a remote file to activity with wasGeneratedBy relationship,
        and, if there is a matching used entity, attach wasDerivedFrom.
        :param data_service: DataServiceApi: service used to attach relationship
        :param file_details: dict: response from DukeDS POST to /files/ containing current_version id
        '''
        current_version = file_details.get('current_version', {})
        file_version_id = current_version.get('id')
        if not file_version_id:
            return

        # wasGeneratedBy: file_version -> activity
        data_service.create_relationship(
            subject_id=file_version_id,
            subject_type='FILE_VERSION',
            predicate='wasGeneratedBy',
            object_id=self.activity.id,
            object_type='ACTIVITY'
        )

        # wasDerivedFrom: file_version -> used input file (if any)
        used_entity_id = self._lookup_used_entity_id(file_details)
        if used_entity_id:
            data_service.create_relationship(
                subject_id=file_version_id,
                subject_type='FILE_VERSION',
                predicate='wasDerivedFrom',
                object_id=used_entity_id,
                object_type='FILE_VERSION'
            )

    def _lookup_used_entity_id(self, file_details):
        '''
        Return the file_version_id associated with the path from file_details.
        The file_version_id is looked up from a dictionary in the activity.
        :param file_details: dict: response from DukeDS POST to /files/
        :return: str or None: file_version_id uuid
        '''
        path = file_details.get('path')
        if not path:
            return None
        used_map = getattr(self.activity, 'used_entities', {})
        return used_map.get(path)