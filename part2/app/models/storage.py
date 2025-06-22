class Storage:
    def __init__(self):
        self.models = {}

    def save(self, model):
        model_id = model.id
        self.models[model_id] = model

    def load(self, model_id):
        return self.models.get(model_id)

    def all(self):
        return self.models.values()

    def delete(self, model_id):
        if model_id in self.models:
            del self.models[model_id]