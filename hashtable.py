class HashTable:
    # Table size 59 chosen because 40 unique IDs at 0.7 load factor is around 58. Then next prime is 59.
    def __init__(self, initial_capacity=59):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    def insert(self, key, item):
        # Get the bucket list where this item will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Update key if it is already in bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # Else, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        # Get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        raise KeyError(f"Key {key} not found in HashTable.")  # Error handling

    def remove(self, key):
        # Get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # Remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])
        raise KeyError(f"Key {key} not found in HashTable.")  # Error handling

    def print_all_data(self):
        # Print the entire hash table for debugging purposes.
        for bucket in self.table:
            for kv in bucket:
                print("Key: {}, Data: {}".format(kv[0], kv[1]))
