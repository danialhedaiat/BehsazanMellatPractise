import json


class KeyDepth:
    def __init__(self, *args, **kwargs):
        self.file = None
        self.result = {}

    def load_json(self, data) -> 'KeyDepth':
        if isinstance(data, dict):
            self.file = data
        else:
            self.file = json.load(data)


    def get_depth(self) -> dict:
        if not self.file:
            raise ValueError("self.file variable is empty! please use load_json method")

        self.result = {}
        self.inner_dict(self.file, 0)
        return self.result

    def inner_dict(self, obj, depth):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key not in self.result or depth < self.result[key]:
                    self.result[key] = depth
                self.inner_dict(value, depth + 1)

        elif isinstance(obj, list):
            for item in obj:
                self.inner_dict(item, depth)


test_data = {"name": "John", "age": 30, "address": {"street": "123 Main St", "city": "Anytown", "postalCode": "12345"},
             "phoneNumbers": [{"type": "home", "number": "123-456-7890"}, {"type": "work", "number": "987-654-3210"}]}

depth = KeyDepth()
depth.load_json(data=test_data)
print(depth.get_depth())
