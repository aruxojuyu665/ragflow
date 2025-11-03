"""
Unit tests for utility functions
Testing helper functions and common utilities
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.mark.unit
class TestJSONParsing:
    """Unit tests for JSON parsing utilities"""
    
    def test_parse_valid_json(self):
        """
        Test parsing valid JSON string.
        
        Given: Valid JSON string
        When: Parsing
        Then: Should return dict
        """
        import json
        
        json_str = '{"key": "value", "number": 123}'
        result = json.loads(json_str)
        
        assert isinstance(result, dict)
        assert result["key"] == "value"
        assert result["number"] == 123
    
    def test_parse_invalid_json_with_fallback(self):
        """
        Test parsing invalid JSON with fallback.
        
        Given: Invalid JSON string
        When: Parsing with try-except
        Then: Should fallback to original string
        """
        import json
        
        json_str = '{"key": "value"'  # Missing closing brace
        
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError:
            result = json_str  # Fallback
        
        assert result == json_str
    
    def test_safe_json_parse_function(self):
        """
        Test safe JSON parsing function.
        
        Given: JSON string (valid or invalid)
        When: Using safe parse
        Then: Should always return a value
        """
        import json
        
        def safe_json_parse(json_str, default=None):
            """Safely parse JSON with fallback"""
            try:
                return json.loads(json_str)
            except (json.JSONDecodeError, TypeError):
                return default if default is not None else json_str
        
        # Test valid JSON
        valid = '{"key": "value"}'
        assert isinstance(safe_json_parse(valid), dict)
        
        # Test invalid JSON
        invalid = '{"key": "value"'
        assert safe_json_parse(invalid) == invalid
        
        # Test with default
        assert safe_json_parse(invalid, default={}) == {}


@pytest.mark.unit
class TestStringValidation:
    """Unit tests for string validation"""
    
    def test_empty_string_validation(self):
        """Test validation of empty strings"""
        empty_strings = ["", "   ", "\t", "\n"]
        
        for s in empty_strings:
            assert not s.strip(), f"String '{s}' should be considered empty"
    
    def test_non_empty_string_validation(self):
        """Test validation of non-empty strings"""
        non_empty_strings = ["test", " test ", "123", "test\nstring"]
        
        for s in non_empty_strings:
            assert s.strip(), f"String '{s}' should be considered non-empty"


@pytest.mark.unit
class TestListOperations:
    """Unit tests for list operations"""
    
    def test_list_deduplication(self):
        """
        Test removing duplicates from list.
        
        Given: List with duplicates
        When: Deduplicating
        Then: Should return unique items
        """
        original = [1, 2, 2, 3, 3, 3, 4]
        unique = list(set(original))
        
        assert len(unique) == 4
        assert set(unique) == {1, 2, 3, 4}
    
    def test_list_chunking(self):
        """
        Test splitting list into chunks.
        
        Given: List and chunk size
        When: Chunking
        Then: Should return list of chunks
        """
        def chunk_list(lst, chunk_size):
            """Split list into chunks"""
            return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]
        
        original = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        chunks = chunk_list(original, 3)
        
        assert len(chunks) == 3
        assert chunks[0] == [1, 2, 3]
        assert chunks[1] == [4, 5, 6]
        assert chunks[2] == [7, 8, 9]
    
    def test_list_filtering(self):
        """
        Test filtering list by condition.
        
        Given: List and filter condition
        When: Filtering
        Then: Should return filtered items
        """
        original = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        even_numbers = [x for x in original if x % 2 == 0]
        
        assert even_numbers == [2, 4, 6, 8]


@pytest.mark.unit
class TestDictOperations:
    """Unit tests for dictionary operations"""
    
    def test_dict_merge(self):
        """
        Test merging dictionaries.
        
        Given: Two dictionaries
        When: Merging
        Then: Should combine keys
        """
        dict1 = {"a": 1, "b": 2}
        dict2 = {"c": 3, "d": 4}
        
        merged = {**dict1, **dict2}
        
        assert len(merged) == 4
        assert merged["a"] == 1
        assert merged["d"] == 4
    
    def test_dict_key_extraction(self):
        """
        Test extracting specific keys from dict.
        
        Given: Dictionary and list of keys
        When: Extracting
        Then: Should return subset
        """
        original = {"a": 1, "b": 2, "c": 3, "d": 4}
        keys_to_extract = ["a", "c"]
        
        extracted = {k: original[k] for k in keys_to_extract if k in original}
        
        assert len(extracted) == 2
        assert extracted == {"a": 1, "c": 3}
    
    def test_dict_safe_get(self):
        """
        Test safe dictionary access with default.
        
        Given: Dictionary and key
        When: Getting value
        Then: Should return value or default
        """
        data = {"key": "value"}
        
        assert data.get("key") == "value"
        assert data.get("missing") is None
        assert data.get("missing", "default") == "default"


@pytest.mark.unit
class TestErrorHandling:
    """Unit tests for error handling patterns"""
    
    def test_try_except_pattern(self):
        """
        Test basic try-except error handling.
        
        Given: Code that might raise exception
        When: Using try-except
        Then: Should handle error gracefully
        """
        def divide(a, b):
            try:
                return a / b
            except ZeroDivisionError:
                return None
        
        assert divide(10, 2) == 5
        assert divide(10, 0) is None
    
    def test_multiple_exception_handling(self):
        """
        Test handling multiple exception types.
        
        Given: Code that might raise different exceptions
        When: Using multiple except blocks
        Then: Should handle each appropriately
        """
        def safe_operation(value):
            try:
                result = int(value) / 2
                return result
            except ValueError:
                return "invalid_value"
            except ZeroDivisionError:
                return "zero_division"
            except Exception:
                return "unknown_error"
        
        assert safe_operation("10") == 5.0
        assert safe_operation("abc") == "invalid_value"
    
    def test_finally_block(self):
        """
        Test finally block execution.
        
        Given: Code with finally block
        When: Executing
        Then: Finally should always run
        """
        cleanup_called = False
        
        def operation_with_cleanup():
            nonlocal cleanup_called
            try:
                return 42
            finally:
                cleanup_called = True
        
        result = operation_with_cleanup()
        
        assert result == 42
        assert cleanup_called is True
