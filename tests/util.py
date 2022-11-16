def get_chrs(length):
    s = ''.join([chr(x % 128 + 64) for x in range(length)])
    return s.encode('latin1') if not isinstance(s, bytes) else s
