from functions.run_python_file import run_python_file


# test functionality expected by bootdev
def test():
    info = run_python_file("calculator", "main.py")
    print(info)

    info = run_python_file("calculator", "main.py", ["3 + 5"])
    print(info)

    info = run_python_file("calculator", "tests.py")
    print(info)

    info = run_python_file("calculator", "../main.py")
    print(info)

    info = run_python_file("calculator", "nonexistent.py")
    print(info)

    info = run_python_file("calculator", "lorem.txt")
    print(info)


if __name__ == "__main__":
    test()
