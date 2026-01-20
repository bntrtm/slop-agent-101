from functions.write_file import write_file


# test functionality expected by bootdev
def test():
    print("Result for 'lorem.txt':")
    info = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(info)

    print("Result for 'pkg/morelorem.txt':")
    info = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(info)

    print("Result for '/tmp/temp.txt':")
    info = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(info)


if __name__ == "__main__":
    test()
