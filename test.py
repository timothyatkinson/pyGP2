# -*- coding: utf-8 -*-
from pyGP2.program import GP2_Program, parse_graph

program = GP2_Program("test2", program_code='''Main = r1

r1
(
	a, b, c : list
)
[
	(n0, a)
    (n1, b)
	|
	(e0, n0, n1, c)
]
=>
[
	(n0, a)
	(n1, b)
	|
	(e0, n0, n1, c)
	(e1, n0, n0, "NEW EDGE")
]
interface = {
	n0, n1
}
''')

my_graph = '''
[
 (0, "A")
 (1, "B")
 |
 (0, 0, 1, 3)
 (1, 1, 0, 3)
]

'''
program.compile_program()

my_graph = parse_graph(my_graph)

for i in range(1):
    if i % 10 == 0:
        print(i)
    res = program.run_on_graph(my_graph)
    print(res.to_string())
    