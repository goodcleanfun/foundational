class ClientProxy(object):
    client = None

    def __getattr__(self, name):
        return getattr(self.client, name)

    def __getitem__(self, name):
        return self.client[name]

    def __setitem__(self, name, value):
        self.client[name] = value

    def __delitem__(self, name):
        del self.client[name]
