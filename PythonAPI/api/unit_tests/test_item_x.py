import unittest
from datetime import datetime
from api.models.item_types import ItemTypes
from api.models.item_groups import ItemGroups
from api.models.item_lines import ItemLines

class Test_ItemTypes(unittest.TestCase):
    def setUp(self):
        self.item_types = ItemTypes(root_path='', is_debug=True)
        self.item_types.data = []

    def test_add_item_type(self):
        item_length = len(self.item_types.get_item_types())
        new_item_type = {
            "id": item_length,
            "name": "Electronics",
            "description": "Category for electronic items"
        }
        self.item_types.add_item_type(new_item_type)
        self.assertEqual(len(self.item_types.get_item_types()), item_length + 1)
        self.assertEqual(self.item_types.get_item_types()[item_length]["name"], "Electronics")

    def test_get_item_type(self):
        item_length = len(self.item_types.get_item_types())
        retrieved_item_type = self.item_types.get_item_type(item_length)
        self.assertIsNotNone(retrieved_item_type)
        self.assertEqual(retrieved_item_type["name"], "Furniture")

    def test_update_timestamp(self):
        item_length = len(self.item_types.get_item_types())
        new_item_type = {
            "id": item_length,
            "name": "Electronics",
            "description": "Category for electronic items"
        }
        self.item_types.add_item_type(new_item_type)
        added_item_type = self.item_types.get_item_type(item_length)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(added_item_type["created_at"], current_time)
        self.assertEqual(added_item_type["updated_at"], current_time)

    def test_remove_item_type(self):
        item_length = len(self.item_types.get_item_types())
        new_item_type = {
            "id": item_length,
            "name": "Electronics",
            "description": "Category for electronic items"
        }
        self.item_types.add_item_type(new_item_type)
        self.assertEqual(len(self.item_types.get_item_types()), item_length + 1)
        self.item_types.remove_item_type(item_length)
        self.assertEqual(len(self.item_types.get_item_types()), item_length)

class Test_ItemGroups(unittest.TestCase):
    def setUp(self):
        self.item_groups = ItemGroups(root_path='', is_debug=True)
        self.item_groups.data = []

    def test_add_item_group(self):
        group_length = len(self.item_groups.get_item_groups())
        new_group = {
            "id": group_length,
            "name": "Premium",
            "description": "Premium item group"
        }
        self.item_groups.add_item_group(new_group)
        self.assertEqual(len(self.item_groups.get_item_groups()), group_length + 1)
        self.assertEqual(self.item_groups.get_item_groups()[group_length]["name"], "Premium")

    def test_get_item_group(self):
        group_length = len(self.item_groups.get_item_groups())
        retrieved_group = self.item_groups.get_item_group(group_length)
        self.assertIsNotNone(retrieved_group)
        self.assertEqual(retrieved_group["name"], "Basic")

    def test_update_timestamp(self):
        group_length = len(self.item_groups.get_item_groups())
        new_group = {
            "id": group_length,
            "name": "Premium",
            "description": "Premium item group"
        }
        self.item_groups.add_item_group(new_group)
        added_group = self.item_groups.get_item_group(group_length)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(added_group["created_at"], current_time)
        self.assertEqual(added_group["updated_at"], current_time)

    def test_remove_item_group(self):
        group_length = len(self.item_groups.get_item_groups())
        new_group = {
            "id": group_length,
            "name": "Premium",
            "description": "Premium item group"
        }
        self.item_groups.add_item_group(new_group)
        self.assertEqual(len(self.item_groups.get_item_groups()), group_length + 1)
        self.item_groups.remove_item_group(group_length)
        self.assertEqual(len(self.item_groups.get_item_groups()), group_length)

class Test_ItemLines(unittest.TestCase):
    def setUp(self):
        self.item_lines = ItemLines(root_path='', is_debug=True)
        self.item_lines.data = []

    def test_add_item_line(self):
        line_length = len(self.item_lines.get_item_lines())
        new_line = {
            "id": line_length,
            "name": "Smartphones",
            "description": "Line for smartphones"
        }
        self.item_lines.add_item_line(new_line)
        self.assertEqual(len(self.item_lines.get_item_lines()), line_length + 1)
        self.assertEqual(self.item_lines.get_item_lines()[line_length]["name"], "Smartphones")

    def test_get_item_line(self):
        line_length = len(self.item_lines.get_item_lines())
        retrieved_line = self.item_lines.get_item_line(line_length)
        self.assertIsNotNone(retrieved_line)
        self.assertEqual(retrieved_line["name"], "Laptops")

    def test_update_timestamp(self):
        line_length = len(self.item_lines.get_item_lines())
        new_line = {
            "id": line_length,
            "name": "Smartphones",
            "description": "Line for smartphones"
        }
        self.item_lines.add_item_line(new_line)
        added_line = self.item_lines.get_item_line(line_length)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(added_line["created_at"], current_time)
        self.assertEqual(added_line["updated_at"], current_time)

    def test_remove_item_line(self):
        line_length = len(self.item_lines.get_item_lines())
        new_line = {
            "id": line_length,
            "name": "Smartphones",
            "description": "Line for smartphones"
        }
        self.item_lines.add_item_line(new_line)
        self.assertEqual(len(self.item_lines.get_item_lines()), line_length + 1)
        self.item_lines.remove_item_line(line_length)
        self.assertEqual(len(self.item_lines.get_item_lines()), line_length)

if __name__ == '__main__':
    unittest.main()
