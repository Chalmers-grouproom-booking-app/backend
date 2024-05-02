from database.pb import client

# get the test value from the encryption_test collection
def get_encryption_test():
    return client.collection("encryption_test").get_full_list()[0].value


if __name__ == '__main__':
    test = get_encryption_test()
    print(test)