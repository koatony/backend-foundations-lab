import pytest
from app.log_utils import append_log_safely
import app.log_utils



def test_log(tmp_path):
    test_file = tmp_path / "test.log"
    initial_counter = app.log_utils.CLEANUP_COUNTER
    append_log_safely(test_file,"hello")
    assert app.log_utils.CLEANUP_COUNTER == initial_counter + 1
    assert test_file.read_text("utf-8") == "hello\n"

def test_append_log_failure_bubbling():
    invalid_path = "/invalid_directory_12345/test.log"
    initial_counter = app.log_utils.CLEANUP_COUNTER
    
    with pytest.raises(FileNotFoundError):
        append_log_safely(invalid_path, 'test')

    assert app.log_utils.CLEANUP_COUNTER == initial_counter + 1




