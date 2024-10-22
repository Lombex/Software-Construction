import unittest
from httpx import Client
from httpx import codes
 
# 7 happy paths
# 9 edge cases
 
 
class TestClients(unittest.TestCase):
 
    def setUp(self):
        self.reader_token = "f6g7h8i9j0"
        self.client = Client(base_url="http://localhost:3000/api/v1/",
                             headers={"Content-Type": "application/json", "API_KEY": "a1b2c3d4e5"})
 
    def test_get_all_readertoken(self):
        self.client.headers["API_KEY"] = self.reader_token
        response = self.client.get("/clients")
 
        self.assertEqual(response.status_code, codes.OK)
   
    def test_get_single_readertoken(self):
        self.client.headers["API_KEY"] = self.reader_token
        response = self.client.get("/clients/8")
 
        self.assertEqual(response.status_code, codes.OK)
   
    def test_unauthorized_get_all(self):
        self.client.headers["API_KEY"] = "wrong_key"
        response = self.client.get("/clients")
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_get_single_incorrect_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        response = self.client.get("/clients/-90")
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_get_single_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        response = self.client.get("/clients/8")
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_create_client_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        new_client = {
            "id": 9,
            "name": "Alperen Smith",
            "address": "300 straat",
            "city": "Carrillomouth",
            "zip_code": "14452",
            "province": "Virginia",
            "country": "United States",
            "contact_name": "Sylvia Zimmerman",
            "contact_phone": "001-635-714-6053",
            "contact_email": "zsmith@example.com",
            "created_at": "1996-04-23 20:51:11",
            "updated_at": "1997-09-21 23:06:24"
 
        }
 
        response = self.client.post("/clients", json=new_client)
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_update_client_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        updated_client = {
            "id": 3,
            "name": "Alperen Baytimur",
            "address": "3 musketiers straat",
            "city": "Carrillomouth",
            "zip_code": "14452",
            "province": "Zuid-Holland",
            "country": "Netherlands",
            "contact_name": "Osman",
            "contact_phone": "001-635-714-6053",
            "contact_email": "zsmith@example.com",
            "created_at": "1996-04-23 20:51:11",
            "updated_at": "1997-09-21 23:06:24"
        }
 
        response = self.client.put("/clients/3", json=updated_client)
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_delete_client_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        response = self.client.delete("/clients/90")
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_delete_incorrect_id_unauthorized(self):
        self.client.headers["API_KEY"] = "wrong_key"
        response = self.client.delete("/clients/-10")
 
        self.assertEqual(response.status_code, codes.UNAUTHORIZED)
 
    def test_get_all(self):
        response = self.client.get("/clients")
 
        self.assertEqual(response.status_code, codes.OK)
        self.assertTrue(len(response.json()) > 0)
 
    def test_get_single(self):
        response = self.client.get("/clients/8")
 
        self.assertEqual(response.status_code, codes.OK)
        self.assertIn("id", response.json())
 
    def test_get_incorrect_id(self):
        response = self.client.get("/clients/-1")
 
        self.assertEqual(response.status_code, codes.NOT_FOUND)
 
    def test_create_client(self):
        new_client = {
            "id": 9,
            "name": "Alperen Smith",
            "address": "300 straat",
            "city": "Carrillomouth",
            "zip_code": "14452",
            "province": "Virginia",
            "country": "United States",
            "contact_name": "Sylvia Zimmerman",
            "contact_phone": "001-635-714-6053",
            "contact_email": "zsmith@example.com",
            "created_at": "1996-04-23 20:51:11",
            "updated_at": "1997-09-21 23:06:24"
 
        }
 
        response = self.client.post("/clients", json=new_client)
        self.assertEqual(response.status_code, 201)
 
    def test_update_client(self):
        updated_client = {
            "id": 3,
            "name": "Alperen Baytimur",
            "address": "3 musketiers straat",
            "city": "Carrillomouth",
            "zip_code": "14452",
            "province": "Zuid-Holland",
            "country": "Netherlands",
            "contact_name": "Osman",
            "contact_phone": "001-635-714-6053",
            "contact_email": "zsmith@example.com",
            "created_at": "1996-04-23 20:51:11",
            "updated_at": "1997-09-21 23:06:24"
        }
 
        response = self.client.put("/clients/3", json=updated_client)
 
        self.assertEqual(response.status_code, codes.OK)
 
    def test_delete_client(self):
        response = self.client.delete("/clients/90")
 
        self.assertEqual(response.status_code, codes.OK)
 
    def test_delete_incorrect_id(self):
        response = self.client.delete("/clients/-10")
 
        self.assertEqual(response.status_code, codes.NOT_FOUND)