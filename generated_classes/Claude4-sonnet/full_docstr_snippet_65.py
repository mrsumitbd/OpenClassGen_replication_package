class PhenoModelHandler(object):
    '''Class handling phenomodels creation and use'''

    def __init__(self, adapter):
        self.adapter = adapter

    def phenomodels(self, institute_id):
        '''Return all phenopanels for a given institute
        Args:
            institute_id(str): institute id
        Returns:
            phenotype_models(pymongo.cursor.Cursor)
        '''
        return self.adapter.phenomodel_collection.find({'institute': institute_id})

    def create_phenomodel(self, institute_id, name, description):
        '''Create an empty advanced phenotype model with data provided by a user
        Args:
            institute_id(str): institute id
            name(str) a model name
            description(str) a model description
        Returns:
            phenomodel_obj(dict) a newly created model
        '''
        phenomodel_obj = {
            '_id': ObjectId(),
            'institute': institute_id,
            'name': name,
            'description': description,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            'features': []
        }
        
        self.adapter.phenomodel_collection.insert_one(phenomodel_obj)
        return phenomodel_obj

    def update_phenomodel(self, model_id, model_obj):
        '''Update a phenotype model using its ObjectId
        Args:
            model_id(str): document ObjectId string id
            model_obj(dict): a dictionary of key/values to update a phenomodel with

        Returns:
            updated_model(dict): the phenomodel document after the update
        '''
        model_obj['updated_at'] = datetime.now()
        
        self.adapter.phenomodel_collection.update_one(
            {'_id': ObjectId(model_id)},
            {'$set': model_obj}
        )
        
        return self.adapter.phenomodel_collection.find_one({'_id': ObjectId(model_id)})

    def phenomodel(self, model_id):
        '''Retrieve a phenomodel object using its ObjectId
        Args:
            model_id(ObjectId): document ObjectId
        Returns
            model_obj(dict)
        '''
        return self.adapter.phenomodel_collection.find_one({'_id': model_id})