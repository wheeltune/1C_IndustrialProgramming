import dis
import builtins
from virtual_machine import VirtualMachine

vm_locals = {}
vm = VirtualMachine(local_names=vm_locals)

exec_locals = {}
program = """
b = []
b.append(10)
b
"""

if __name__ == "__main__":
    print(dis.dis(program))
    print()
    for inst in dis.get_instructions(program):
        print(inst)
    exec(program, {}, exec_locals)
    print("Exec:", exec_locals)

    vm.run_code(program)
    print("Vm:", vm_locals)
