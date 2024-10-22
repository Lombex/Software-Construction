import unittest
from datetime import datetime
from api.models.clients import Clients

class Test_Clients(unittest.TestCase):
    def setUp(self):
        self.clients = Clients(root_path='', is_debug=True)
        self.clients.data = []

    def test_add_client(self):
        clientlength = len(self.clients.get_client())
        new_client = {
            "id": clientlength,
            "name": "Jane Doe",
            "address": "Second Street 2",
            "city": "Utrecht",
            "zip_code": "3511AA",
            "country": "Netherlands",
            "contact_name": "Jane Doe",
            "contact_phone": "+31687654321",
            "contact_email": "jane.doe@example.com"
        }
        self.clients.add_client(new_client)
        self.assertEqual(clientlength, clientlength + 1)
        self.assertEqual(self.clients.get_client()[clientlength]["name"], "Jane Doe")

    def test_get_client(self):
        clientlength = len(self.clients.get_client())
        retrieved_client = self.clients.get_client(clientlength)
        self.assertIsNotNone(retrieved_client)
        self.assertEqual(retrieved_client["name"], "John Doe")

    def test_update_timestamp(self):
        clientlength = len(self.clients.get_client())
        new_client = {
            "id": clientlength,
            "name": "Jane Doe",
            "address": "Second Street 2",
            "city": "Utrecht",
            "zip_code": "3511AA",
            "country": "Netherlands",
            "contact_name": "Jane Doe",
            "contact_phone": "+31687654321",
            "contact_email": "jane.doe@example.com"
        }
        self.clients.add_client(new_client)
        added_client = self.clients.get_client(3)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(added_client["created_at"], current_time)
        self.assertEqual(added_client["updated_at"], current_time)
    
    def test_remove_client(self):
        clientlength = len(self.clients.get_client())
        new_client = {
            "id": clientlength,
            "name": "Jane Doe",
            "address": "Second Street 2",
            "city": "Utrecht",
            "zip_code": "3511AA",
            "country": "Netherlands",
            "contact_name": "Jane Doe",
            "contact_phone": "+31687654321",
            "contact_email": "jane.doe@example.com"
        }
        self.clients.add_client(new_client)
        self.assertEqual(clientlength, clientlength + 1)
        self.clients.remove_client(clientlength)
        self.assertEqual(clientlength, clientlength - 1)

if __name__ == '__main__':
    unittest.main()