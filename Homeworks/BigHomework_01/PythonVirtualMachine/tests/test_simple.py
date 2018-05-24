from virtual_machine import VirtualMachine
import dis


class TestSimple:
    def setup(self):
        self.vm = VirtualMachine()
        self.program = ""

    def teardown(self):
        exec_globals, exec_locals = {}, {}
        vm_globals, vm_locals = {}, {}

        assert(exec(self.program, exec_locals, exec_locals) == self.vm.run_code(self.program, vm_globals, vm_locals))
        assert(exec_globals == vm_globals)

        exec_keys = list(exec_locals.keys())
        for key in exec_keys:
            if key.startswith("__"):
                exec_locals.pop(key)

        assert(exec_locals == vm_locals)



    def test_operations(self):
        self.program = """
a = 10
b = 20
c = a - b
d = a + b
e = a / b
f = a * b
g = f / c - (a + b * d) / e + b / e"""

    def test_append(self):
        self.program = """
l = []
for i in range(100):
    l.append(i)"""

    def test_loop(self):
        self.program = """
a = 0
for i in range(100):
    a += 1"""

    def test_add(self):
        self.program = """
a = 10
b = 20
c = a + b"""

    def test_mul(self):
        self.program = """
a=2"""
