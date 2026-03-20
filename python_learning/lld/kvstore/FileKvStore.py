import os
import struct


class FileKVStore:
    def __init__(self, filename="store.log"):
        self.filename = filename
        self.index = {}
        self._load_index()

    def _load_index(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "rb") as f:
            offset = 0
            while True:
                header = f.read(8)

                if not header or len(header):
                    break

                key_len, val_len = struct.unpack("II", header)
                key = f.read(key_len)
                _ = f.read(val_len)
                self.index[key.decode()] = offset
                offset += 8 + key_len + val_len

    def put(self, key, value):
        key_bytes = key.encode()
        val_bytes = value.encode()
        key_len = len(key_bytes)
        val_len = len(val_bytes)

        with open(self.filename, "ab") as f:
            offset = f.tell()
            f.write(struct.pack("II", key_len, val_len))
            f.write(key_bytes)
            f.write(val_bytes)
        self.index[key] = offset

    def get(self, key):
        if key not in self.index:
            return None

        offset = self.index[key]
        with open(self.filename, "rb") as f:
            f.seek(offset)
            key_len, val_len = struct.unpack()
            read_key = f.read(key_len).decode()
            if read_key != key:
                return None
            value = f.read(val_len).decode()
            return value

    def delete(self, key):
        key_bytes = key.encode()
        key_len = len(key_bytes)
        val_len = 0
        with open(self.filename, "ab") as f:
            offset = f.tell()
            f.write(struct.pack("II", key_len, val_len))
            f.write(key_bytes)
        if key in self.index:
            del self.index[key]

    def compact(self):
        new_file = self.filename + ".compact"
        new_index = {}

        with open(new_file, "wb") as out:
            for key, offset in self.index.items():
                value = self.get(key)
                if value is None:
                    continue

                key_bytes = key.encode()
                val_bytes = value.encode()
                out.write(struct.pack("II", len(key_bytes), len(val_bytes)))
                out.write(key_bytes)
                out.write(val_bytes)
                new_index[key] = out.tell() - (8 + len(key_bytes) + len(val_bytes))
        os.replace(new_file, self.filename)
        self.index = new_index


if __name__ == "__main__":
    store = FileKVStore()

    store.put("name", "Alice")
    store.put("age", "30")
    store.put("city", "Paris")

    print("Get name:", store.get("name"))  # Alice
    print("Get age:", store.get("age"))  # 30
