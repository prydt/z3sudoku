# z3sudoku
A sudoku solver written with the Z3 SMT solver! Honestly, I just wanted an excuse to learn how to use Z3's python API.

Here's what it looks like in practice!
```sh
(venv) pry@apollo:~/repos/z3sudoku$ time python sudoku.py 
[4, 7, 8, 1, 6, 2, 3, 5, 9]
[3, 5, 1, 4, 9, 7, 6, 8, 2]
[2, 9, 6, 3, 8, 5, 1, 7, 4]
[1, 6, 5, 8, 3, 9, 4, 2, 7]
[7, 4, 9, 5, 2, 1, 8, 3, 6]
[8, 3, 2, 6, 7, 4, 5, 9, 1]
[6, 8, 7, 2, 4, 3, 9, 1, 5]
[5, 2, 4, 9, 1, 8, 7, 6, 3]
[9, 1, 3, 7, 5, 6, 2, 4, 8]

real    0m2.660s
user    0m2.630s
sys     0m0.031s

```

## Requirements
Install the amazing Z3 solver wiiiith:
```sh
pip install z3-solver
```