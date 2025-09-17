class _LineageArtifactTracker(object):
    '''Lineage Artifact Tracker'''

    def __init__(self, trial_component_arn, sagemaker_session):
        '''Initialize a `_LineageArtifactTracker` instance.

        Args:
            trial_component_arn (str): The ARN of the trial component to be
                associated with the input/output artifacts.
            sagemaker_session (sagemaker.session.Session): Session object which
                manages interactions with Amazon SageMaker APIs and any other
                AWS services needed.
        '''
        self.trial_component_arn = trial_component_arn
        self.sagemaker_session = sagemaker_session
        self.input_artifacts = []
        self.output_artifacts = []

    def add_input_artifact(self, name, source_uri, etag, artifact_type):
        '''Add a Lineage input artifact locally

        Args:
            name (str): The name of the Lineage input artifact to be added.
            source_uri (str): The source URI used to create the Lineage input artifact.
            etag (str): The S3 Etag used to create the Lineage input artifact.
            artifact_type (str): The type of the Lineage input artifact.
        '''
        artifact = {
            'name': name,
            'source_uri': source_uri,
            'etag': etag,
            'artifact_type': artifact_type
        }
        self.input_artifacts.append(artifact)

    def add_output_artifact(self, name, source_uri, etag, artifact_type):
        '''Add a Lineage output artifact locally

        Args:
            name (str): The name of the Lineage output artifact to be added.
            source_uri (str): The source URI used to create the Lineage output artifact.
            etag (str): The S3 Etag used to create the Lineage output artifact.
            artifact_type (str): The type of the Lineage output artifact.
        '''
        artifact = {
            'name': name,
            'source_uri': source_uri,
            'etag': etag,
            'artifact_type': artifact_type
        }
        self.output_artifacts.append(artifact)

    def save(self):
        '''Persist any artifact data saved locally'''
        for artifact in self.input_artifacts:
            self._create_artifact_and_association(artifact, 'input')
        
        for artifact in self.output_artifacts:
            self._create_artifact_and_association(artifact, 'output')
        
        self.input_artifacts.clear()
        self.output_artifacts.clear()

    def _create_artifact_and_association(self, artifact, association_type):
        try:
            artifact_arn = self.sagemaker_session.sagemaker_client.create_artifact(
                ArtifactName=artifact['name'],
                Source={
                    'SourceUri': artifact['source_uri'],
                    'SourceTypes': [
                        {
                            'SourceIdType': 'S3ETag',
                            'Value': artifact['etag']
                        }
                    ]
                },
                ArtifactType=artifact['artifact_type']
            )['ArtifactArn']
        except Exception:
            artifacts = self.sagemaker_session.sagemaker_client.list_artifacts(
                SourceUri=artifact['source_uri']
            )['ArtifactSummaries']
            
            if artifacts:
                artifact_arn = artifacts[0]['ArtifactArn']
            else:
                return

        association_type_mapping = {
            'input': 'ContributedTo',
            'output': 'Produced'
        }

        try:
            self.sagemaker_session.sagemaker_client.add_association(
                SourceArn=artifact_arn if association_type == 'input' else self.trial_component_arn,
                DestinationArn=self.trial_component_arn if association_type == 'input' else artifact_arn,
                AssociationType=association_type_mapping[association_type]
            )
        except Exception:
            pass