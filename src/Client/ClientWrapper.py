import inspect

from src.Client.Clients import MockS3Client, MockJiraClient
from src.Client.Config.ClientConfig import ClientName
import logging


class ClientWrapper:
    def __init__(self, config_client):
        self.client_config = config_client
        self.client_list = self.create_client_list()

    def set_key(self):
        for x in ClientName:
            self.client_list[x.name].key = self.config_client.credentials[x.name]

    def create_client_list(self):
        return {ClientName.s3.name: self.bootstrap_client(MockS3Client,
                                                          self.client_config.get_config_by_name(ClientName.s3.value)),
                ClientName.jira.name: self.bootstrap_client(MockJiraClient,
                                                            self.client_config.get_config_by_name(ClientName.jira.value))}

    def get_client(self, client_name):
        if client_name not in self.client_list:
            logging.error("No client in client list with name: ", client_name)
        else:
            return self.client_list[client_name]

    @staticmethod
    def bootstrap_client(client, config):
        #TODO replace tuples with new tuples
        for i in inspect.getmembers(client):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    if i[0] in config.keys():
                       i[1] = config[i[0]]
        return client
