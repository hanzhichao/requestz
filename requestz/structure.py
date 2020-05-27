from collections import OrderedDict, defaultdict


class DotDict(dict):
    def __getattr__(self, item):
        return self.get(item, None)


class SameKeysDict(dict):
    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            arg1 = args[0]
            if isinstance(arg1, (list, tuple)):
                [self.__setitem__(*item)  for item in arg1 if isinstance(item, (list, tuple)) and len(item) == 2]
                return
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        if not hasattr(self, 'same_keys'):
            self.same_keys = defaultdict(list)

        if key not in self:
            super().__setitem__(key, value)
            return

        if key not in self.same_keys:
            self.same_keys[key].append(self.get(key))
        self.same_keys[key].append(value)
        super().__setitem__(key, self.same_keys.get(key))

    def update(self, m: dict, **kwargs):
        for key, value in m.items():
            self[key] = value


class CaseInsensitiveDict(SameKeysDict):  # 没有缓存
    @property
    def lower_key_dict(self):
        return {key.lower(): value for key, value in self.items()}

    def get(self, key, default=None):
        return self.lower_key_dict.get(key.lower(), default)

    def __getitem__(self, key):
        return self.lower_key_dict[key.lower()]

    def __contains__(self, item):
        return item in self.lower_key_dict

    def __eq__(self, other):
        return self.lower_key_dict == CaseInsensitiveDict(other).lower_key_dict
