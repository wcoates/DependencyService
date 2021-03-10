import inspect
import unittest

from src.Client.ClientWrapper import ClientWrapper
from src.Client.Clients import MockJiraClient
from src.Client.Config.ClientConfig import ConfigClient, ClientName
from src.Script.Scripts import ScriptRunner


class TestConfig(unittest.TestCase):

    def test_config_not_empty(self):
        config_client = ConfigClient()
        for x in ClientName:
            self.assertNotEqual(config_client.get_config_by_name(x.value), None, "Missing config in file for client")

    def test_credentials_not_empty(self):
        config_client = ConfigClient()
        for x in ClientName:
            self.assertNotEqual(config_client.credentials[x.value], None, "Missing credential key")

    def test_config_has_client_name_keys(self):
        config = ConfigClient.retrieve_credentials()
        for x in ClientName:
            self.assertTrue(x.name in config.keys(), "No matching client key defined in configuration")

    def test_config_has_client_attr_values(self):
        config = ConfigClient.retrieve_config()['client_config']
        client_attributes = []
        config_values = []
        client_wrapper = ClientWrapper(ConfigClient())

        #TODO wtf isn't this showing attributes
        for x in client_wrapper.client_list.values():
            for i in inspect.getmembers(x):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]):
                        client_attributes.append(i[0])

        for x in config.values():
            config_values.append(x.keys())

        print(client_attributes)

        for x in client_attributes:
            self.assertTrue(x in config_values, "Could not find matching config value for client attribute: " + x)

        for x in config_values:
            self.assertTrue(x in client_attributes, "Could not find matching client attribute for config value: " + x)

    def test_client_list_not_empty(self):
        client_wrapper = ClientWrapper(ConfigClient())

        for x in ClientName:
            self.assertNotEqual(client_wrapper.client_list[x.name], None)

    def test_client_attributes_not_empty(self):
        client_wrapper = ClientWrapper(ConfigClient())

        for x in client_wrapper.client_list.values():
            for i in inspect.getmembers(x):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]):
                        self.assertNotEqual(i[1], '', "Missing config value for: " + type(x).__name__ + "." + i[0])

    def test_script_runner_client_attributes_not_empty(self):
        script_runner = ScriptRunner(None)
        client_wrapper = script_runner.ClientWrapper

        for x in client_wrapper.client_list.values():
            for i in inspect.getmembers(x):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]):
                        self.assertNotEqual(i[1], '', "Missing config value for: " + type(x).__name__ + "." + i[0])


if __name__ == '__main__':
    unittest.main()
