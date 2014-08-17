def myreadlines(f, newline):
    buf = ""
    while True:
        while newline in buf:
            pos = buf.index(newline)
            yield buf[:pos]
            buf = buf[pos + len(newline):]
        chunk = f.read(4096)
        if not chunk:
            yield buf
            break
        buf += chunk


with open('test_good_posts.txt') as f:
    l = [x for x in myreadlines(f, "<END>\n")]
    for i in l:
        raw_input("Enter for next entry")
        print "\n" + i + "\n\n"