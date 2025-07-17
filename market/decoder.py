import io
import os
import struct
from collections import Counter
from bitstring import BitArray


class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.c = char
        self.f = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __repr__(self):
        return f'{self.c}:{self.f}'


class MinHeap:
    def __init__(self):
        self.arr = []

    def size(self):
        return len(self.arr)

    def push(self, obj):
        self.arr.append(obj)
        child_idx = self.size() - 1

        while True:
            parent_idx = (child_idx - 1) // 2
            if self.arr[parent_idx] <= self.arr[child_idx]:
                return

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]
            child_idx = parent_idx

            if child_idx <= 0:
                return

    def pop(self):
        obj = self.arr[0]

        last = self.arr.pop()
        if self.size() == 0:
            return obj
        self.arr[0] = last

        parent_idx = 0
        child_idx = 2 * parent_idx + 1
        while child_idx < self.size():
            if child_idx + 1 < self.size():
                if self.arr[child_idx + 1] < self.arr[child_idx]:
                    child_idx += 1

            if self.arr[parent_idx] <= self.arr[child_idx]:
                return obj

            self.arr[parent_idx], self.arr[child_idx] = self.arr[child_idx], self.arr[parent_idx]

            parent_idx = child_idx
            child_idx = 2 * child_idx + 1

        return obj


def make_tree(freqs):
    h = MinHeap()
    for c, f in freqs.items():
        h.push(Node(c, f))

    while h.size() > 1:
        a = h.pop()
        b = h.pop()
        n = Node(a.c + b.c, a.f + b.f, a, b)
        h.push(n)

    return h.pop()


def decode(tree, freqs, packed, bits, verbose=False, check_stats=False):
    p = BitArray(bytes=packed)
    p = p[:bits]
    if verbose:
        print(p.bin)
    unpacked = []
    pos = 0
    while pos < len(p):
        node = tree
        while True:
            if pos >= len(p):
                raise ValueError(f'invalid tree: out of message bounds, {unpacked=}')
            bit = p[pos]
            if bit:
                node = node.right
            else:
                node = node.left
            pos += 1
            if node is None:
                raise ValueError(f'invalid tree: dead end while walking, {unpacked=}')
            if node.left is None and node.right is None:
                break
        unpacked.append(node.c)

    if check_stats:
        stats = Counter(unpacked)
        for c, f in freqs.items():
            if stats[c] != f:
                raise ValueError(f"incorrect '{c}' freq: header={f} processed={stats[c]}, {unpacked=}")

    return ''.join(unpacked)


def read(file, fmt):
    i = struct.calcsize(fmt)
    ret = struct.unpack(fmt, file.read(i))
    if type(ret) == tuple and len(ret) == 1:
        return ret[0]
    return ret


def get_freqs(file):
    file_len, always0, chars_count = read(file, 'III')
    freqs = {}
    for i in range(chars_count):
        count = read(file, 'I')
        char = read(file, 'cxxx').decode('ascii')
        freqs[char] = count
    return freqs


def unpack_file(file):
    freqs = get_freqs(file)
    tree = make_tree(freqs)

    packed_bits, packed_bytes, unpacked_bytes = read(file, 'III')

    packed = file.read(packed_bytes)
    result = decode(tree, freqs, packed, packed_bits)
    return result


def unpack(data):
    if type(data) == bytes:
        data = io.BytesIO(data)

    return unpack_file(data)


if __name__ == "__main__":
    test = bytes.fromhex('81 00 00 00 00 00 00 00 0B 00 00 00 06 00 00 00 2D 00 00 00 09 00 00 00 30 00 00 00 03 00 00 00 31 00 00 00 03 00 00 00 32 00 00 00 02 00 00 00 33 00 00 00 02 00 00 00 34 00 00 00 06 00 00 00 35 00 00 00 03 00 00 00 37 00 00 00 04 00 00 00 38 00 00 00 01 00 00 00 39 00 00 00 02 00 00 00 7C 00 00 00 85 00 00 00 11 00 00 00 29 00 00 00 D3 0C 78 90 FB 1D 0E 6E 4B 4C 35 DF 17 75 BD AA 90')
    print(unpack(test))
