# filemaker.py
# for making files to read. using generators and Faker
# aims to create files at around the specified filesize

from faker import Faker

# size units
# i.e. 2 MB = 2 * 1024 * 1024 B
KB = 1024
MB = 1024 * 1024
GB = 1024 * 1024 * 1024

new_file_name = "filemaker_example.txt"


def inf_profiles():
    """
    Infinite generator that yields 1 dict of fake profile data when accessed
    """
    fake = Faker()
    while True:
        yield fake.simple_profile()


def generate_file(filename: str, min_size: int, size_unit: int, gen: callable):
    """
    Generates a text file at (filename) with the size (min_size) (size_unit) using the passed generator (gen)
    """
    try:
        with open(filename, "w") as f:
            while f.tell() < min_size * size_unit:
                f.write(str(next(gen)) + "\n")
    except PermissionError:
        print(f"Program doesn't have permission to write to file \"{filename}\". Obtain permission or choose another file.")
        exit(1)
    except KeyboardInterrupt:
        print(f"Program was interrupted, file \"{filename}\" may not be at desired size or well-formed.")
        exit(1)



generate_file(new_file_name, 10, KB, inf_profiles())