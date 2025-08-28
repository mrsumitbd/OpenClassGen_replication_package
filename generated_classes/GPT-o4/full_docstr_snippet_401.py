class _LineageArtifactTracker(object):
    '''Lineage Artifact Tracker'''

    def __init__(self, trial_component_arn, sagemaker_session):
        self.trial_component_arn = trial_component_arn
        self.sagemaker_session = sagemaker_session
        self._input_artifacts = []
        self._output_artifacts = []

    def add_input_artifact(self, name, source_uri, etag, artifact_type):
        self._input_artifacts.append({
            'Name': name,
            'SourceUri': source_uri,
            'Etag': etag,
            'ArtifactType': artifact_type
        })

    def add_output_artifact(self, name, source_uri, etag, artifact_type):
        self._output_artifacts.append({
            'Name': name,
            'SourceUri': source_uri,
            'Etag': etag,
            'ArtifactType': artifact_type
        })

    def save(self):
        # save input artifacts
        for art in self._input_artifacts:
            src = {
                'SourceUri': art['SourceUri'],
                'S3Uri': art['SourceUri'],
                'S3ExecutionContext': {'Etag': art['Etag']}
            }
            art_arn = self.sagemaker_session.create_artifact(
                artifact_name=art['Name'],
                artifact_type=art['ArtifactType'],
                source=src,
                properties={}
            )
            self.sagemaker_session.add_association(
                source_arn=art_arn,
                destination_arn=self.trial_component_arn,
                association_type='ContributedTo'
            )

        # save output artifacts
        for art in self._output_artifacts:
            src = {
                'SourceUri': art['SourceUri'],
                'S3Uri': art['SourceUri'],
                'S3ExecutionContext': {'Etag': art['Etag']}
            }
            art_arn = self.sagemaker_session.create_artifact(
                artifact_name=art['Name'],
                artifact_type=art['ArtifactType'],
                source=src,
                properties={}
            )
            self.sagemaker_session.add_association(
                source_arn=self.trial_component_arn,
                destination_arn=art_arn,
                association_type='ContributedTo'
            )

        self._input_artifacts.clear()
        self._output_artifacts.clear()