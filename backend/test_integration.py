"""
Integration test script to verify the frontend-backend integration
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_backend_health():
    """Test if the backend is running and accessible"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("+ Backend is running and accessible")
            print(f"Health check response: {response.json()}")
            return True
        else:
            print(f"- Backend health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("- Cannot connect to backend. Is it running on http://127.0.0.1:8000?")
        return False

def test_task_creation():
    """Test task creation functionality with mock-user-id"""
    try:
        # Test creating a task
        task_data = {
            "title": "Test task from integration test",
            "description": "This is a test task created during integration testing",
            "completed": False
        }

        response = requests.post(f"{BASE_URL}/api/mock-user-id/tasks", json=task_data)

        if response.status_code in [200, 201]:
            print("+ Task creation successful")
            print(f"Response: {response.json()}")

            # Extract task ID from response for further testing
            response_data = response.json()
            if 'data' in response_data and 'id' in response_data['data']:
                task_id = response_data['data']['id']
                return True, task_id
            else:
                print("- Task ID not found in response")
                return False, None
        else:
            print(f"- Task creation failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
    except requests.exceptions.ConnectionError:
        print("- Cannot connect to backend for task creation test")
        return False, None

def test_task_retrieval(task_id):
    """Test retrieving the created task"""
    try:
        response = requests.get(f"{BASE_URL}/api/mock-user-id/tasks")

        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])

            # Look for our test task
            found_task = None
            for task in tasks:
                if str(task.get('id')) == str(task_id):
                    found_task = task
                    break

            if found_task:
                print(f"+ Task retrieval successful - found task with ID {task_id}")
                print(f"Task: {found_task['title']}")
                return True
            else:
                print(f"- Task with ID {task_id} not found in retrieved tasks")
                print(f"All tasks: {[t['title'] for t in tasks]}")
                return False
        else:
            print(f"- Task retrieval failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("- Cannot connect to backend for task retrieval test")
        return False

def main():
    print("Starting frontend-backend integration test...\n")

    # Test 1: Check if backend is running
    if not test_backend_health():
        print("\nIntegration test aborted: Backend is not accessible.")
        return

    print()

    # Test 2: Create a task
    success, task_id = test_task_creation()
    if not success:
        print("\nIntegration test failed: Could not create task.")
        return

    print()

    # Test 3: Retrieve the created task
    if task_id:
        success = test_task_retrieval(task_id)
        if not success:
            print("\nIntegration test failed: Could not retrieve created task.")
            return

    print("\n+ All integration tests passed!")

if __name__ == "__main__":
    main()