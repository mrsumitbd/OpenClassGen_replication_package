class PhenoModelHandler(object):
    '''Class handling phenomodels creation and use'''

    def __init__(self, database):
        '''Initialize with a database connection
        Args:
            database: pymongo database object
        '''
        self.db = database

    def phenomodels(self, institute_id):
        '''Return all phenopanels for a given institute
        Args:
            institute_id(str): institute id
        Returns:
            phenotype_models(pymongo.cursor.Cursor)
        '''
        return self.db.phenomodels.find({'institute_id': institute_id})

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
            'institute_id': institute_id,
            'name': name,
            'description': description,
            'subpanels': {},
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now()
        }
        result = self.db.phenomodels.insert_one(phenomodel_obj)
        phenomodel_obj['_id'] = result.inserted_id
        return phenomodel_obj

    def update_phenomodel(self, model_id, model_obj):
        '''Update a phenotype model using its ObjectId
        Args:
            model_id(str): document ObjectId string id
            model_obj(dict): a dictionary of key/values to update a phenomodel with

        Returns:
            updated_model(dict): the phenomodel document after the update
        '''
        from bson import ObjectId
        model_obj['updated_at'] = datetime.datetime.now()
        result = self.db.phenomodels.update_one(
            {'_id': ObjectId(model_id)},
            {'$set': model_obj}
        )
        if result.modified_count > 0:
            return self.db.phenomodels.find_one({'_id': ObjectId(model_id)})
        return None

    def phenomodel(self, model_id):
        '''Retrieve a phenomodel object using its ObjectId
        Args:
            model_id(str): document ObjectId string id
        Returns
            model_obj(dict)
        '''
        from bson import ObjectId
        return self.db.phenomodels.find_one({'_id': ObjectId(model_id)})