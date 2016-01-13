Authex Decode
=============

This program decodes the binary record files produced by the Authex indexing
software. The decoding was reversed engineered from the binary files, and no
guarantees are made as to its correctness in all situations. I doubt this code
will be useful to anyone else.

# Usage

The program will try to open the file `AV03.bff` in the current directory. It will
then dump each record to standard out. Records are separated by blank lines.
Sample command line:

    python decode.py > records.txt

The program only dumps the records. It doesn't recover the index.

# File Format

Files begin with a magic string of `\x1a\x20\x30\x00\x00` followed by 512 bytes of a space character `\x20`. Afterward is a sequence of offset tables and records, see the file for more information.
