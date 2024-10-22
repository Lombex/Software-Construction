import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException

# Temporary FastAPI app for testing
app = FastAPI()

item_types_data = []
item_groups_data = []
item_lines_data = []

client = TestClient(app)

@app.post("/item_types/")
async def create_item_type(item_type: dict):
    if "id" not in item_type:
        raise HTTPException(status_code=400, detail="Item type must have an 'id'")
    for existing_item_type in item_types_data:
        if existing_item_type["id"] == item_type["id"]:
            raise HTTPException(status_code=400, detail="Item type already exists")
    item_types_data.append(item_type)
    return item_type

@app.get("/item_types/{item_type_id}")
async def get_item_type(item_type_id: int):
    for item_type in item_types_data:
        if item_type["id"] == item_type_id:
            return item_type
    raise HTTPException(status_code=404, detail="Item type not found")

@app.put("/item_types/{item_type_id}")
async def update_item_type(item_type_id: int, updated_item_type: dict):
    for index, item_type in enumerate(item_types_data):
        if item_type["id"] == item_type_id:
            item_types_data[index].update(updated_item_type)
            return item_types_data[index]
    raise HTTPException(status_code=404, detail="Item type not found")

@app.delete("/item_types/{item_type_id}")
async def delete_item_type(item_type_id: int):
    for index, item_type in enumerate(item_types_data):
        if item_type["id"] == item_type_id:
            del item_types_data[index]
            return {"detail": "Item type deleted"}
    raise HTTPException(status_code=404, detail="Item type not found")

@pytest.fixture
def sample_item_type():
    return {
        "id": 1,
        "name": "Electronics",
        "description": "Category for electronic items"
    }

def test_create_item_type(sample_item_type):
    response = client.post("/item_types/", json=sample_item_type)
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_get_item_type(sample_item_type):
    client.post("/item_types/", json=sample_item_type)
    response = client.get("/item_types/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics"

def test_update_item_type(sample_item_type):
    client.post("/item_types/", json=sample_item_type)
    updated_data = {"name": "Electronics Updated"}
    response = client.put("/item_types/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Electronics Updated"

def test_delete_item_type(sample_item_type):
    client.post("/item_types/", json=sample_item_type)
    response = client.delete("/item_types/1")
    assert response.status_code == 200
    assert client.get("/item_types/1").status_code == 404

# Routes for ItemGroups
@app.post("/item_groups/")
async def create_item_group(item_group: dict):
    if "id" not in item_group:
        raise HTTPException(status_code=400, detail="Item group must have an 'id'")
    for existing_group in item_groups_data:
        if existing_group["id"] == item_group["id"]:
            raise HTTPException(status_code=400, detail="Item group already exists")
    item_groups_data.append(item_group)
    return item_group

@app.get("/item_groups/{group_id}")
async def get_item_group(group_id: int):
    for group in item_groups_data:
        if group["id"] == group_id:
            return group
    raise HTTPException(status_code=404, detail="Item group not found")

@app.put("/item_groups/{group_id}")
async def update_item_group(group_id: int, updated_group: dict):
    for index, group in enumerate(item_groups_data):
        if group["id"] == group_id:
            item_groups_data[index].update(updated_group)
            return item_groups_data[index]
    raise HTTPException(status_code=404, detail="Item group not found")

@app.delete("/item_groups/{group_id}")
async def delete_item_group(group_id: int):
    for index, group in enumerate(item_groups_data):
        if group["id"] == group_id:
            del item_groups_data[index]
            return {"detail": "Item group deleted"}
    raise HTTPException(status_code=404, detail="Item group not found")

# Routes for ItemLines
@app.post("/item_lines/")
async def create_item_line(item_line: dict):
    if "id" not in item_line:
        raise HTTPException(status_code=400, detail="Item line must have an 'id'")
    for existing_line in item_lines_data:
        if existing_line["id"] == item_line["id"]:
            raise HTTPException(status_code=400, detail="Item line already exists")
    item_lines_data.append(item_line)
    return item_line

@app.get("/item_lines/{line_id}")
async def get_item_line(line_id: int):
    for line in item_lines_data:
        if line["id"] == line_id:
            return line
    raise HTTPException(status_code=404, detail="Item line not found")

@app.put("/item_lines/{line_id}")
async def update_item_line(line_id: int, updated_line: dict):
    for index, line in enumerate(item_lines_data):
        if line["id"] == line_id:
            item_lines_data[index].update(updated_line)
            return item_lines_data[index]
    raise HTTPException(status_code=404, detail="Item line not found")

@app.delete("/item_lines/{line_id}")
async def delete_item_line(line_id: int):
    for index, line in enumerate(item_lines_data):
        if line["id"] == line_id:
            del item_lines_data[index]
            return {"detail": "Item line deleted"}
    raise HTTPException(status_code=404, detail="Item line not found")

# Fixtures for tests
@pytest.fixture
def sample_item_group():
    return {
        "id": 1,
        "name": "Premium",
        "description": "Premium item group"
    }

@pytest.fixture
def sample_item_line():
    return {
        "id": 1,
        "name": "Smartphones",
        "description": "Line for smartphones"
    }

# Test cases for ItemGroups
def test_create_item_group(sample_item_group):
    response = client.post("/item_groups/", json=sample_item_group)
    assert response.status_code == 200
    assert response.json()["name"] == "Premium"

def test_get_item_group(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    response = client.get("/item_groups/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Premium"

def test_update_item_group(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    updated_data = {"name": "Premium Updated"}
    response = client.put("/item_groups/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Premium Updated"

def test_delete_item_group(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    response = client.delete("/item_groups/1")
    assert response.status_code == 200
    assert client.get("/item_groups/1").status_code == 404

# Test cases for ItemLines
def test_create_item_line(sample_item_line):
    response = client.post("/item_lines/", json=sample_item_line)
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphones"

def test_get_item_line(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    response = client.get("/item_lines/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphones"

def test_update_item_line(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    updated_data = {"name": "Smartphones Updated"}
    response = client.put("/item_lines/1", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Smartphones Updated"

def test_delete_item_line(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    response = client.delete("/item_lines/1")
    assert response.status_code == 200
    assert client.get("/item_lines/1").status_code == 404

####

@app.post("/item_groups/")
async def create_item_group(item_group: dict):
    if "id" not in item_group:
        raise HTTPException(status_code=400, detail="Item group must have an 'id'")
    for existing_group in item_groups_data:
        if existing_group["id"] == item_group["id"]:
            raise HTTPException(status_code=400, detail="Item group already exists")
    item_groups_data.append(item_group)
    return item_group

@app.get("/item_groups/{group_id}")
async def get_item_group(group_id: int):
    for group in item_groups_data:
        if group["id"] == group_id:
            return group
    raise HTTPException(status_code=404, detail="Item group not found")

@app.put("/item_groups/{group_id}")
async def update_item_group(group_id: int, updated_group: dict):
    for index, group in enumerate(item_groups_data):
        if group["id"] == group_id:
            item_groups_data[index].update(updated_group)
            return item_groups_data[index]
    raise HTTPException(status_code=404, detail="Item group not found")

@app.delete("/item_groups/{group_id}")
async def delete_item_group(group_id: int):
    for index, group in enumerate(item_groups_data):
        if group["id"] == group_id:
            del item_groups_data[index]
            return {"detail": "Item group deleted"}
    raise HTTPException(status_code=404, detail="Item group not found")

@app.post("/item_lines/")
async def create_item_line(item_line: dict):
    if "id" not in item_line:
        raise HTTPException(status_code=400, detail="Item line must have an 'id'")
    for existing_line in item_lines_data:
        if existing_line["id"] == item_line["id"]:
            raise HTTPException(status_code=400, detail="Item line already exists")
    item_lines_data.append(item_line)
    return item_line

@app.get("/item_lines/{line_id}")
async def get_item_line(line_id: int):
    for line in item_lines_data:
        if line["id"] == line_id:
            return line
    raise HTTPException(status_code=404, detail="Item line not found")

@app.put("/item_lines/{line_id}")
async def update_item_line(line_id: int, updated_line: dict):
    for index, line in enumerate(item_lines_data):
        if line["id"] == line_id:
            item_lines_data[index].update(updated_line)
            return item_lines_data[index]
    raise HTTPException(status_code=404, detail="Item line not found")

@app.delete("/item_lines/{line_id}")
async def delete_item_line(line_id: int):
    for index, line in enumerate(item_lines_data):
        if line["id"] == line_id:
            del item_lines_data[index]
            return {"detail": "Item line deleted"}
    raise HTTPException(status_code=404, detail="Item line not found")

# Fixtures for tests
@pytest.fixture
def sample_item_group():
    return {
        "id": 1,
        "name": "Premium",
        "description": "Premium item group"
    }

@pytest.fixture
def sample_item_line():
    return {
        "id": 1,
        "name": "Smartphones",
        "description": "Line for smartphones"
    }

def test_update_multiple_fields_item_group(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    updated_data = {"name": "Group Updated", "description": "Updated description"}
    response = client.put("/item_groups/1", json=updated_data)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Group Updated"
    assert response.json()["description"] == "Updated description"

def test_update_multiple_fields_item_line(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    updated_data = {"name": "Line Updated", "description": "Updated description"}
    response = client.put("/item_lines/1", json=updated_data)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Line Updated"
    assert response.json()["description"] == "Updated description"

def test_create_item_group_boundary_id():
    group = {"id": 999999, "name": "Boundary Group", "description": "Boundary description"}
    response = client.post("/item_groups/", json=group)
    
    assert response.status_code == 200
    assert response.json()["id"] == 999999

def test_create_item_line_boundary_id():
    line = {"id": 999999, "name": "Boundary Line", "description": "Boundary description"}
    response = client.post("/item_lines/", json=line)
    
    assert response.status_code == 200
    assert response.json()["id"] == 999999

def test_get_item_group_after_delete(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    client.delete("/item_groups/1")
    
    response = client.get("/item_groups/1")
    assert response.status_code == 404

def test_get_item_line_after_delete(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    client.delete("/item_lines/1")
    
    response = client.get("/item_lines/1")
    assert response.status_code == 404

# Sad Flow Tests
def test_create_item_group_missing_fields():
    incomplete_group = {"name": "Incomplete Group"}  # Missing 'id' and 'description'
    response = client.post("/item_groups/", json=incomplete_group)
    
    assert response.status_code == 400
    assert "must have an 'id'" in response.json()["detail"]

def test_create_item_line_missing_fields():
    incomplete_line = {"name": "Incomplete Line"}  # Missing 'id' and 'description'
    response = client.post("/item_lines/", json=incomplete_line)
    
    assert response.status_code == 400
    assert "must have an 'id'" in response.json()["detail"]

def test_get_non_existing_item_group():
    response = client.get("/item_groups/999")
    
    assert response.status_code == 404
    assert "Item group not found" in response.json()["detail"]

def test_get_non_existing_item_line():
    response = client.get("/item_lines/999")
    
    assert response.status_code == 404
    assert "Item line not found" in response.json()["detail"]

def test_delete_non_existing_item_group():
    response = client.delete("/item_groups/999")
    
    assert response.status_code == 404
    assert "Item group not found" in response.json()["detail"]

def test_delete_non_existing_item_line():
    response = client.delete("/item_lines/999")
    
    assert response.status_code == 404
    assert "Item line not found" in response.json()["detail"]

def test_create_duplicate_item_group(sample_item_group):
    client.post("/item_groups/", json=sample_item_group)
    response = client.post("/item_groups/", json=sample_item_group)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_create_duplicate_item_line(sample_item_line):
    client.post("/item_lines/", json=sample_item_line)
    response = client.post("/item_lines/", json=sample_item_line)
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_update_non_existing_item_group():
    updated_data = {"name": "Updated Group"}
    response = client.put("/item_groups/999", json=updated_data)
    
    assert response.status_code == 404
    assert "Item group not found" in response.json()["detail"]

def test_update_non_existing_item_line():
    updated_data = {"name": "Updated Line"}
    response = client.put("/item_lines/999", json=updated_data)
    
    assert response.status_code == 404
    assert "Item line not found" in response.json()["detail"]