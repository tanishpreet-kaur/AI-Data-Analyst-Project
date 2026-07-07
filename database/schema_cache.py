class SchemaCache:
    def __init__(self):
        self.schema = None

    def save(self, schema):
        self.schema = schema

    def load(self):
        return self.schema

    def clear(self):
        self.schema = None