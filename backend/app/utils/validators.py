from typing import Optional
import re

def validate_task_title(title: str) -> bool:
    """
    Validates that the task title is between 1 and 255 characters
    """
    if not isinstance(title, str):
        return False
    
    if len(title) < 1 or len(title) > 255:
        return False
    
    return True

def validate_task_description(description: Optional[str]) -> bool:
    """
    Validates that the task description is 1000 characters or less if provided
    """
    if description is None:
        return True
    
    if not isinstance(description, str):
        return False
    
    if len(description) > 1000:
        return False
    
    return True

def validate_user_id(user_id: str) -> bool:
    """
    Validates that the user_id is a valid string
    """
    if not isinstance(user_id, str):
        return False
    
    # Basic validation - adjust as needed based on your requirements
    if len(user_id) < 1 or len(user_id) > 255:
        return False
    
    return True