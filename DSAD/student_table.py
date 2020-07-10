class StudentHashRecords(object):
    def __init__(self, length=4):
        self.array = [None] * length

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        length = len(self.array)
        h2 = list()
        for index in range(length):
            if self.array[index] is not None:
                for data in self.array[index]:
                    h2.append(data)
        return iter(h2)


    def hash(self, key):
        """Get the index of our array for a specific string key"""
        length = len(self.array)
        value = hash(key) % length
        return value

    def add(self, key, value):
        """Add a value to our array by its key"""
        index = self.hash(key)
        if self.array[index] is not None:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    kvp[1] = value
                    break
            else:
                self.array[index].append([key, value])
        else:
            self.array[index] = []
            self.array[index].append([key, value])
        if self.is_full():
            self.double()

    def get(self, key):
        """Get a value by key"""
        index = self.hash(key)
        if self.array[index] is None:
            raise KeyError()
        else:
            for kvp in self.array[index]:
                if kvp[0] == key:
                    return kvp[1]
            raise KeyError()

    def delete(self):
        """Delete whole array"""
        del self.array
        return StudentHashRecords()

    def is_full(self):
        """Determines if the HashTable is too populated."""
        items = 0
        for item in self.array:
            if item is not None:
                items += 1
        return items > len(self.array) / 2

    def double(self):
        """Double the list length and re-add values"""
        ht2 = StudentHashRecords(length=len(self.array) * 2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue
            for kvp in self.array[i]:
                ht2.add(kvp[0], kvp[1])
        self.array = ht2.array