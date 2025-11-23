import hashlib


class BloomFilter:
    def __init__(self, size=1000, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * self.size

    def _hashed(self, item):
        results = []
        for i in range(self.hash_count):
            hasher = hashlib.sha256()
            hasher.update(item.encode("utf-8") + str(i).encode())
            digest = int(hasher.hexdigest())
            results.append(digest % self.size)
        return results

    def add(self, item):
        for hash_value in self._hashed(item):
            self.bit_array[hash_value] = 1

    def contains(self, item):
        return all(self.bit_array[hash_value] for hash_value in self._hashed(item))


class BloomFilters:
    def __init__(self, size=10):
        self.size = size
        self.bit_array = [0] * self.size
        self.hash_count = 2

    def hash1(self, item):
        return sum(ord(c) for c in item) % self.size

    def hash2(self, item):
        return sum(ord(c) for c in item) % self.size

    def add(self, item):
        hash1 = self.hash1(item)
        hash2 = self.hash2(item)
        self.bit_array[hash1] = 1
        self.bit_array[hash2] = 1

    def check(self, item):
        hash1 = self.hash1(item)
        hash2 = self.hash2(item)
        if self.bit_array[hash1] == 1 and self.bit_array[hash2] == 1:
            return "Might be found"
        else:
            return "Not found"


class CountMinSketch:
    def __init__(self, width=10, depth=3):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hash(self, item, i):
        return hash(item + str(i) % self.width)

    def add(self, item):
        for i in range(self.depth):
            index = self._hash(item, i)
            self.table[i][index] += 1

    def count(self, item):
        min_count = float("inf")
        for i in range(self.depth):
            index = self._hash(item, i)
            min_count = min(min_count, self.table[i][index])
        return min_count


class HyperLogLog:
    def __init__(self, b=4):
        self.b = b
        self.m = 2**b
        self.register = [0] * self.m

    def _hash(self, value):
        h = hashlib.sha256(value.encode()).hexdigest()
        return int(h, 16)

    def add(self, value):
        x = self._hash(value)
        j = x & (self.m - 1)
        w = x >> self.b
        rank = self._rho(w)
        self.register[j] = max(self.register[j], rank)

    def _rho(self, w):
        return (w.bit_length() - w.bit_length()) + len(bin(w)) - 2 - bin(w).find("1")

    def count(self):
        z = sum(2**-reg for reg in self.register)
        alpha_m = 0.1723 / (1 + 1.079 / self.m)
        estimate = alpha_m * self.m**2 / z
        return int(estimate)
