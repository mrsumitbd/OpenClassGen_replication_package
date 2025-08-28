class PhenoModelHandler(object):
    '''Class handling phenomodels creation and use'''

    def __init__(self, db):
        """
        Args:
            db (pymongo.database.Database): a PyMongo Database instance
        """
        self.db = db
        self.collection = self.db.phenomodels

    def phenomodels(self, institute_id):
        '''Return all phenomodels for a given institute
        Args:
            institute_id(str): institute id
        Returns:
            phenotype_models(pymongo.cursor.Cursor)
        '''
        return self.collection.find({'institute_id': institute_id})

    def create_phenomodel(self, institute_id, name, description):
        '''Create an empty advanced phenotype model with data provided by a user
        Args:
            institute_id(str): institute id
            name(str) a model name
            description(str) a model description
        Returns:
            phenomodel_obj(dict) a newly created model
        '''
        now = datetime.datetime.utcnow()
        doc = {
            'institute_id': institute_id,
            'name': name,
            'description': description,
            'created_at': now,
            'modified_at': now
        }
        res = self.collection.insert_one(doc)
        doc['_id'] = res.inserted_id
        return doc

    def update_phenomodel(self, model_id, model_obj):
        '''Update a phenotype model using its ObjectId
        Args:
            model_id(str): document ObjectId string id
            model_obj(dict): a dictionary of key/values to update a phenomodel with
        Returns:
            updated_model(dict): the phenomodel document after the update
        '''
        oid = ObjectId(model_id)
        model_obj['modified_at'] = datetime.datetime.utcnow()
        self.collection.update_one({'_id': oid}, {'$set': model_obj})
        return self.collection.find_one({'_id': oid})

    def get_phenomodel(self, model_id):
        '''Retrieve a phenomodel object using its ObjectId
        Args:
            model_id(str): document ObjectId string id
        Returns:
            model_obj(dict)
        '''
        oid = ObjectId(model_id)
        return self.collection.find_one({'_id': oid})