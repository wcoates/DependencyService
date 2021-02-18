class ConfigClient:
    def __init__(self):
        self.ClientConfig = self.retrieve_config()

    def retrieve_config(self):
        return ClientConfig("WC045050", "credentials")


class ClientConfig:
    def __init__(self, user, key):
        self.user = user
        self.key = key
