class DataMapper:
    model_database = None
    model_schema = None

    def map_to_domain_entity(self, model):
        return self.model_schema.model_validate(model, from_attributes=True)

    def map_to_persistence_entity(self, schema):
        return self.model_database(**schema.model_dump())
