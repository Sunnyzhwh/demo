class ModelMixin:
    def to_dict(self):
        data = {}
        for field in self._meta.fields:
            name = field.attname
            value = getattr(self, name)
            data[name] = value
        return data