# This script will compute SHA256 hash of a downloaded file and compare it with its original hash.
# This allows the user to verify whether the downloaded file has been changed or altered in any way.
# It is particularly useful to verify downloaded ISOs of various Linux distributions.
#
# This script is written by AMEYA KAMAT and is licensed under GNU GPL v3.
#
# You can freely download, use, modify and/or distribute this code.

import hashlib


def main():
    print("This program will check and verify the SHA256 hash of a downloaded file.")
    print("Please ensure the file is in the same directory as this program.")
    while True:
        print("")
        file_name = input("Please enter the name of the file you want to verify: ")
        file_hash = hashlib.sha256()
        try:
            with open(file_name, "rb") as f:
                print("Computing SHA256 hash of the file. Please wait...")
                for byte_block in iter(lambda: f.read(4096), b""):
                    file_hash.update(byte_block)
                file_hash = file_hash.hexdigest()
                print("The SHA256 hash of the given file is", file_hash)
                break
        except FileNotFoundError:
            print("Cannot find the file. Please check if the filename is correct and try again.")

    expected_hash = input("Please enter/paste the SHA256 hash of the file: ")
    if file_hash == expected_hash:
        print("The hashes match. The file is safe to use.")
    else:
        print("The hashes do not match. Do not use the file. It may have been altered.")


if __name__ == '__main__':
    main()
