from functions.get_files_info import get_files_info


def test():
    print("Result for current directory:")
    info = get_files_info("calculator", ".")
    print(info)

    print("Result for 'pkg' directory:")
    info = get_files_info("calculator", "pkg")
    print(info)

    print("Result for '/bin' directory:")
    info = get_files_info("calculator", "/bin")
    print(info)

    print("Result for '../' directory:")
    info = get_files_info("calculator", "../")
    print(info)


if __name__ == "__main__":
    test()
