import unittest
from functions.get_file_content import get_file_content
from config import MAX_CHARS


class TestGetFileContent(unittest.TestCase):
    def test_truncation(self):
        result = get_file_content("calculator", "lorem.txt")
        assert len(result) >= MAX_CHARS
        assert "truncated at" in result

    # test functionality expected by bootdev
    def test_calculator(self):
        result = get_file_content("calculator", "main.py")
        print(result)
        result = get_file_content("calculator", "pkg/calculator.py")
        print(result)
        result = get_file_content("calculator", "/bin/cat")
        print(result)
        result = get_file_content("calculator", "pkg/does_not_exist.py")
        print(result)


if __name__ == "__main__":
    unittest.main()
