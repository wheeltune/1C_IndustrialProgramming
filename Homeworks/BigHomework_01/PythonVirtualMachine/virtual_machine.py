import builtins
import dis
import inspect
import operator


class Stack(object):
    def __init__(self, *args):
        self.__data = []
        self.__data.extend(args)

    def pop(self):
        return self.__data.pop()

    def pop_n(self, n):
        return_elements = self.__data[-n:]
        self.__data = self.__data[:-n]
        return return_elements

    def push(self, *items):
        self.__data.extend(items)

    def peak(self):
        return self.__data[-1]


class BlockStack(object):
    def __init__(self):
        self.__blocks = [Stack()]

    def push_block(self):
        self.__blocks.append(Stack())

    def pop_block(self):
        self.__blocks.pop()

    def pop(self, from_block=-1):
        return self.__blocks[from_block].pop()

    def pop_n(self, n):
        return self.__blocks[-1].pop_n(n)

    def push(self, *items):
        return self.__blocks[-1].push(*items)

    def peak(self):
        return self.__blocks[-1].peak()


class Frame(object):
    def __init__(self, code, global_names, local_names):
        if isinstance(code, str):
            code = compile(code, '', 'exec')

        self.code = code
        self.global_names = global_names
        self.local_names = local_names
        self.stack = Stack()


class VirtualMachine(object):
    def __init__(self, global_names=None, local_names=None):
        if global_names is None:
            self.global_names = {}
        else:
            self.global_names = global_names

        if local_names is None:
            self.local_names = {}
        else:
            self.local_names = local_names

        self.frame_stack = Stack()
        self.stack = BlockStack()

    def run_code(self, code, global_names=None, local_names=None):
        if global_names is not None:
            self.global_names, global_names = global_names, self.global_names
        if local_names is not None:
            self.local_names, local_names = local_names, self.local_names

        try:
            if isinstance(code, str):
                code = compile(code, '', 'exec')

            instructions = []
            instruction_history = {}
            for index, instruction in enumerate(dis.get_instructions(code)):
                instructions.append(instruction)
                instruction_history[instruction.offset] = index

            pos = 0
            while pos < len(instructions):
                jump_offset = self.execute(instructions[pos])
                if jump_offset is not None:
                    if jump_offset == -1:
                        return
                    pos = instruction_history[jump_offset]
                else:
                    pos += 1
        finally:
            if global_names is not None:
                self.global_names, global_names = global_names, self.global_names
            if local_names is not None:
                self.local_names, local_names = local_names, self.local_names

    def execute(self, instruction):
        return getattr(self, instruction.opname)(instruction.argval)

    # ----
    def STOP_CODE(self, argval):
        return -1

    def NOP(self, argval):
        pass

    def POP_TOP(self, argval):
        self.stack.pop()

    # ----
    def rot(self, count):
        tops = self.stack.pop_n(count)
        self.stack.push(tops[-1], *tops[:-1])

    def ROT_TWO(self, argval):
        self.rot(2)

    def ROT_THREE(self, argval):
        self.rot(3)

    def ROT_FOUR(self, argval):
        self.rot(4)

    def DUP_TOP(self, argval):
        self.stack.push(self.stack.peak())

    # ----
    def unary(self, operation):
        self.stack.push(operation(self.stack.pop()))

    def UNARY_POSITIVE(self, argval):
        self.unary(operator.pos)

    def UNARY_NEGATIVE(self, argval):
        self.unary(operator.neg)

    def UNARY_NOT(self, argval):
        self.unary(operator.not_)

    def UNARY_CONVERT(self, argval):
        self.unary(repr)

    def UNARY_INVERT(self, argval):
        self.unary(lambda a: ~a)

    def GET_ITER(self, argval):
        self.unary(iter)

    # -----
    def binary(self, operation):
        tops = self.stack.pop_n(2)
        self.stack.push(operation(*tops))

    def BINARY_POWER(self, argval):
        self.binary(operator.pow)

    def BINARY_MULTIPLY(self, argval):
        self.binary(operator.mul)

    def BINARY_DIVIDE(self, argval):
        self.binary(operator.truediv)

    def BINARY_FLOOR_DIVIDE(self, argval):
        self.binary(operator.floordiv)

    def BINARY_TRUE_DIVIDE(self, argval):
        self.binary(operator.truediv)

    def BINARY_MODULO(self, argval):
        self.binary(operator.mod)

    def BINARY_ADD(self, argval):
        self.binary(operator.add)

    def BINARY_SUBTRACT(self, argval):
        self.binary(operator.sub)

    def BINARY_SUBSCR(self, argval):
        self.binary(operator.getitem)

    def BINARY_LSHIFT(self, argval):
        self.binary(operator.lshift)

    def BINARY_RSHIFT(self, argval):
        self.binary(operator.rshift)

    def BINARY_AND(self, argval):
        self.binary(operator.and_)

    def BINARY_XOR(self, argval):
        self.binary(operator.xor)

    def BINARY_OR(self, argval):
        self.binary(operator.or_)

    # ----
    def INPLACE_POWER(self, argval):
        self.binary(operator.ipow)

    def INPLACE_MULTIPLY(self, argval):
        self.binary(operator.imul)

    def INPLACE_DIVIDE(self, argval):
        self.binary(operator.itruediv)

    def INPLACE_FLOOR_DIVIDE(self, argval):
        self.binary(operator.ifloordiv)

    def INPLACE_TRUE_DIVIDE(self, argval):
        self.binary(operator.itruediv)

    def INPLACE_MODULO(self, argval):
        self.binary(operator.imod)

    def INPLACE_ADD(self, argval):
        self.binary(operator.iadd)

    def INPLACE_SUBTRACT(self, argval):
        self.binary(operator.isub)

    def INPLACE_LSHIFT(self, argval):
        self.binary(operator.ilshift)

    def INPLACE_RSHIFT(self, argval):
        self.binary(operator.irshift)

    def INPLACE_AND(self, argval):
        self.binary(operator.iand)

    def INPLACE_XOR(self, argval):
        self.binary(operator.ixor)

    def INPLACE_OR(self, argval):
        self.binary(operator.ior)

    # ----
    def SLICE_0(self, argval):
        pass

    def SLICE_1(self, argval):
        pass

    def SLICE_2(self, argval):
        pass

    def SLICE_3(self, argval):
        pass

    # ----
    def STORE_SLICE_0(self, argval):
        pass

    def STORE_SLICE_1(self, argval):
        pass

    def STORE_SLICE_2(self, argval):
        pass

    def STORE_SLICE_3(self, argval):
        pass

    def DELETE_SLICE_0(self, argval):
        pass

    def DELETE_SLICE_1(self, argval):
        pass

    def DELETE_SLICE_2(self, argval):
        pass

    def DELETE_SLICE_3(self, argval):
        pass

    def STORE_SUBSCR(self, argval):
        pass

    def DELETE_SUBSCR(self, argval):
        pass

    # ----
    def PRINT_EXPR(self, argval):
        print(self.stack.pop())

    def PRINT_ITEM(self, argval):
        print(self.stack.pop())

    def PRINT_ITEM_TO(self, argval):
        data = self.stack.pop_n(2)
        print(data[0], file=data[1])

    def PRINT_NEWLINE(self, argval):
        print()

    def PRINT_NEWLINE_TO(self, argval):
        print(file=self.stack.pop())

    def BREAK_LOOP(self, argval):
        return self.stack.pop(from_block=-2)

    def CONTINUE_LOOP(self, argval):
        return argval

    def LIST_APPEND(self, argval):
        pass

    def LOAD_LOCALS(self, argval):
        pass

    def RETURN_VALUE(self, argval):
        pass

    def YIELD_VALUE(self, argval):
        pass

    def IMPORT_STAR(self, argval):
        pass

    def EXEC_STMT(self, argval):
        pass

    def POP_BLOCK(self, argval):
        self.stack.pop_block()

    def END_FINALLY(self, argval):
        pass

    def BUILD_CLASS(self, argval):
        pass

    def SETUP_WITH(self, argval):
        pass

    def WITH_CLEANUP(self, argval):
        pass

    def STORE_NAME(self, argval):
        self.local_names[argval] = self.stack.pop()

    def DELETE_NAME(self, argval):
        pass

    def UNPACK_SEQUENCE(self, argval):
        pass

    def DUP_TOPX(self, argval):
        pass

    def STORE_ATTR(self, argval):
        pass

    def DELETE_ATTR(self, argval):
        pass

    def STORE_GLOBAL(self, argval):
        pass

    def DELETE_GLOBAL(self, argval):
        pass

    def LOAD_CONST(self, argval):
        self.stack.push(argval)

    def LOAD_NAME(self, argval):
        if argval in self.local_names:
            self.stack.push(self.local_names[argval])
        elif argval in self.global_names:
            self.stack.push(self.global_names[argval])
        elif argval in dir(builtins):
            self.stack.push(getattr(builtins, argval))
        else:
            raise NameError(f"name '{argval}' is not defined")

    def BUILD_TUPLE(self, argval):
        data = self.stack.pop_n(argval)
        self.stack.push(tuple(data))

    def BUILD_LIST(self, argval):
        data = self.stack.pop_n(argval)
        self.stack.push(data)

    def BUILD_SET(self, argval):
        data = self.stack.pop_n(argval)
        self.stack.push(set(data))

    def BUILD_MAP(self, argval):
        data = self.stack.pop_n(2 * argval)
        self.stack.push(map(data[::2], data[1::2]))

    def LOAD_ATTR(self, argval):
        self.stack.push(getattr(self.stack.pop(), argval))

    def COMPARE_OP(self, argval):
        pass

    def IMPORT_NAME(self, argval):
        pass

    def IMPORT_FROM(self, argval):
        pass

    def JUMP_FORWARD(self, argval):
        pass

    def POP_JUMP_IF_TRUE(self, argval):
        pass

    def POP_JUMP_IF_FALSE(self, argval):
        pass

    def JUMP_IF_TRUE_OR_POP(self, argval):
        pass

    def JUMP_IF_FALSE_OR_POP(self, argval):
        pass

    def JUMP_ABSOLUTE(self, argval):
        return argval

    def FOR_ITER(self, argval):
        for_iterator = self.stack.peak()
        try:
            val = next(for_iterator)
            self.stack.push(val)
        except StopIteration:
            self.stack.pop()
            return argval

    def LOAD_GLOBAL(self, argval):
        pass

    def SETUP_LOOP(self, argval):
        self.stack.push(argval)
        self.stack.push_block()

    def SETUP_EXCEPT(self, argval):
        pass

    def SETUP_FINALLY(self, argval):
        pass

    def STORE_MAP(self, argval):
        pass

    def LOAD_FAST(self, argval):
        if argval in self.local_names:
            self.stack.push(self.local_names[argval])
        else:
            raise UnboundLocalError(f"Local variable '{argval}' used before assignment")

    def STORE_FAST(self, argval):
        self.local_names[argval] = self.stack.pop()

    def DELETE_FAST(self, argval):
        if argval in self.local_names:
            del self.local_names[argval]
        else:
            raise NameError(f"name '{argval}' is not defined")

    def LOAD_CLOSURE(self, argval):
        pass

    def LOAD_DEREF(self, argval):
        pass

    def STORE_DEREF(self, argval):
        pass

    def SET_LINENO(self, argval):
        pass

    def RAISE_VARARGS(self, argval):
        pass

    def CALL_FUNCTION(self, argval):
        function_args = self.stack.pop_n(argval)
        func = self.stack.pop()
        self.stack.push(func(*function_args))

    def MAKE_FUNCTION(self, argval):
        pass

    def MAKE_CLOSURE(self, argval):
        pass

    def BUILD_SLICE(self, argval):
        pass

    def EXTENDED_ARG(self, argval):
        pass

    def CALL_FUNCTION_VAR(self, argval):
        pass

    def CALL_FUNCTION_KW(self, argval):
        pass

    def CALL_FUNCTION_VAR_KW(self, argval):
        pass

    def HAVE_ARGUMENT(self, argval):
        pass


# class InstructionExecutor(object):
#     def __init__(self, frame, instruction, instructions):
#         self.stack = frame.data_stack
#         self.frame = frame
#         self.argval = instruction.argval
#         self.locals = frame.locals
#         self.block_stack = frame.block_stack
#         self.instructions = instructions
#
#     # STACK MANIPULATION SECTION
#     def popn(self, n: int) -> list:
#         if n:
#             elems = self.stack[-n:]
#             self.stack[-n:] = []
#             return elems
#         else:
#             return []
#
#     def NOP(self):
#         return
#
#     def POP_TOP(self):
#         self.stack.pop()
#
#     def ROT_TWO(self):
#         a, b = self.popn(2)
#         self.stack.append(b, a)
#
#     def ROT_THREE(self):
#         a, b, c = self.popn(3)
#         self.stack.append(c, a, b)
#
#     def DUP_TOP(self):
#         self.stack.append(self.stack[-1])
#
#     def DUP_TOP_TWO(self):
#         a, b = self.popn(2)
#         self.stack.append(a, b, a, b)
#
#     def PRINT_EXPR(self):
#         print(self.stack.pop())
#
#     def UNPACK_SEQUENCE(self):
#         TOS = self.popn(1)
#         for elem in reversed(TOS):
#             self.stack.append(elem)
#
#     def POP_BLOCK(self):
#         self.block_stack.pop()
#
#     # LOAD SECTION
#     def LOAD_CONST(self):
#         self.stack.append(self.argval)
#
#     def LOAD_GLOBAL(self):
#         if self.argval in globals():
#             self.stack.append(globals()[self.argval])
#         else:
#             self.stack.append(getattr(builtins, self.argval))
#
#     def LOAD_NAME(self):
#         if self.argval in self.locals_:
#             self.stack.append(self.locals_[self.argval])
#         elif self.argval in globals():
#             self.stack.append(globals()[self.argval])
#         elif self.argval in dir(builtins):
#             self.stack.append(getattr(builtins, self.argval))
#         else:
#             raise NameError()
#
#     def LOAD_FAST(self):
#         if self.argval in self.locals_:
#             self.stack.append(self.locals_[self.argval])
#         else:
#             raise UnboundLocalError(
#                 "Local variabale {} used before assignment".format(
#                     self.argval))
#
#     def LOAD_ATTR(self):
#         self.stack[-1] = getattr(self.stack[-1], self.argval)
#
#     def LOAD_BUILD_CLASS(self):
#         self.stack.append(builtins.__build_class__())
#
#     # UNARY SECTION
#     def UNARY_POSITIVE(self):
#         self.stack[-1] = +self.stack[-1]
#
#     def UNARY_NEGATIVE(self):
#         self.stack[-1] = -self.stack[-1]
#
#     def UNARY_NOT(self):
#         self.stack[-1] = not self.stack[-1]
#
#     def UNARY_INVERT(self):
#         self.stack[-1] = ~self.stack[-1]
#
#     def GET_ITER(self):
#         self.stack[-1] = iter(self.stack[-1])
#
#     def GET_YIELD_FROM_ITER(self):
#         if inspect.isgeneratorfunction(self.stack[-1]) \
#                 or inspect.iscoroutine(self.stack[-1]):
#             return
#         self.stack[-1] = iter(self.stack[-1])
#
#     # COMPARE SECTION
#     def COMPARE_OP(self):  # exception match and BAD?
#         b, a = self.popn(2)
#         COMPARE_OPERATIONS = {
#             '<': operator.lt,
#             '<=': operator.le,
#             '>': operator.gt,
#             '>=': operator.ge,
#             '==': operator.eq,
#             '!=': operator.ne,
#             'is': operator.is_,
#             'is not': operator.is_not,
#             'in': lambda x, y: x in y,
#             'not in': lambda x, y: x not in y
#         }
#         self.stack.append(COMPARE_OPERATIONS[self.argval](b, a))
#
#     # STORE SECTION
#     def STORE_SUBSCR(self):
#         tos2, tos1, tos = self.popn(3)
#         tos1[tos] = tos2
#
#     def STORE_NAME(self):
#         self.locals_[self.argval] = self.stack[-1]
#         self.stack.pop()
#
#     def STORE_ATTR(self):
#         value, object_ = self.popn(2)
#         setattr(object_, value)
#
#     def STORE_GLOBAL(self):
#         globals()[self.argval] = self.stack[-1]
#         self.stack.pop()
#
#     def STORE_FAST(self):
#         self.locals_[self.argval] = self.stack[-1]
#         self.stack.pop()
#
#     def STORE_MAP(self):
#         map_, value, key = self.popn(3)
#         map_[key] = value
#         self.stack.append(map_)
#
#     # DELETE SECTION
#     def DELETE_SUBSCR(self):
#         tos1, tos = self.popn(2)
#         del tos1[tos]
#
#     def DELETE_NAME(self):
#         del self.locals_[self.argval]
#
#     def DELETE_FAST(self):
#         del self.locals_[self.argval]
#
#     def DELETE_GLOBAL(self):
#         del globals()[self.argval]
#
#     def DELETE_ATTR(self):
#         object_ = self.popn(1)
#         delattr(object, self.argval)
#
#     # BUILD SECTION
#     def BUILD_SLICE(self):
#         if self.argval == 2:
#             a, b = self.popn(2)
#             self.stack.append(slice(a, b))
#         elif self.argval == 3:
#             a, b, c = self.popn(3)
#             self.stack.append(slice(a, b, c))
#
#     def BUILD_TUPLE(self):
#         elements = self.popn(self.argval)
#         self.stack.append(tuple(elements))
#
#     def BUILD_LIST(self):
#         elements = self.popn(self.argval)
#         self.stack.append(list(elements))
#
#     def LIST_APPEND(self):
#         value = self.stack.pop()
#         cur_list = self.stack[-self.argval]
#         cur_list.append(value)
#
#     def BUILD_MAP(self):
#         args = []
#         for i in range(self.argval):
#             key, value = self.popn(2)
#             args.append((key, value))
#         self.stack.append(dict(args))
#
#     def MAP_ADD(self):
#         value, key = self.popn(2)
#         cur_map = self.stack[-self.argval]
#         cur_map[key] = value
#
#     def BUILD_SET(self):
#         elements = self.popn(self.argval)
#         self.stack.append(set(elements))
#
#     def SET_ADD(self):
#         value = self.stack.pop()
#         cur_set = self.stack[-self.argval]
#         cur_set.add(value)
#
#     # LOOPS SECTION
#     def CONTINUE_LOOP(self):
#         return self.instructions[self.argval]
#
#     def RETURN_VALUE(self):
#         a = self.popn(1)
#         return (a,)
#
#     def SETUP_LOOP(self):
#         self.block_stack.append(('loop', self.argval))
#
#     def BREAK_LOOP(self):
#         index = self.instructions[self.block_stack[-1][1]]
#         self.block_stack.pop()
#         return index
#
#     def FOR_ITER(self):
#         TOS = self.stack[-1]
#         try:
#             a = next(TOS)
#             self.stack.append(a)
#         except StopIteration:
#             self.stack.pop()
#             return self.instructions[self.argval]
#
#     # JUMPS SECTION
#     def JUMP_FORWARD(self):
#         return self.instructions[self.argval]
#
#     def POP_JUMP_IF_TRUE(self):
#         value = self.stack[-1]
#         if value:
#             return self.instructions[self.argval]
#
#     def POP_JUMP_IF_FALSE(self):
#         value = self.stack[-1]
#         if not value:
#             return self.instructions[self.argval]
#
#     def JUMP_IF_TRUE_OR_POP(self):
#         value = self.stack[-1]
#         if value:
#             return self.instructions[self.argval]
#         else:
#             self.stack.pop()
#
#     def JUMP_IF_FALSE_OR_POP(self):
#         value = self.stack[-1]
#         if not value:
#             return self.instructions[self.argval]
#         else:
#             self.stack.pop()
#
#     def JUMP_ABSOLUTE(self):
#         return self.instructions[self.argval]
#
#     # FUNCTION SECTION
#     def CALL_FUNCTION(self):
#         return self.call_function_(self.argval, [], {})
#
#     def CALL_FUNCTION_VAR(self):
#         args = self.stack.pop()
#         return self.call_function_(self.argval, args, {})
#
#     def CALL_FUNCTION_KW(self):
#         kwargs = self.stack.pop()
#         return self.call_function_(self.argval, [], kwargs)
#
#     def CALL_FUNCTION_VAR_KW(self):
#         args, kwargs = self.popn(2)
#         return self.call_function_(self.argval, args, kwargs)
#
#     def call_function_(self, arg, args, kwargs):
#         _, tot_args = divmod(arg, 256)
#
#         n_kwargs = len(kwargs)
#         n_args = tot_args - n_kwargs
#         cortege_args = []
#         named_args = {}
#         arguments = self.popn(tot_args)
#
#         for i, argument in enumerate(arguments):
#             if i < n_args:
#                 cortege_args.append(argument)
#             else:
#                 named_args[kwargs[i - n_args]] = argument
#
#         func = self.stack.pop()
#         self.stack.append(func(*cortege_args, **named_args))
#
#     def MAKE_FUNCTION(self):
#         pass
#
#
# class VirtualMachine(object):
#     BINARY_OPERATIONS = {
#         'BINARY_POWER': operator.pow,
#         'BINARY_MULTIPLY': operator.mul,
#         'BINARY_FLOOR_DIVIDE': operator.floordiv,
#         'BINARY_TRUE_DIVIDE': operator.truediv,
#         'BINARY_MODULO': operator.mod,
#         'BINARY_ADD': operator.add,
#         'BINARY_SUBSTRACT': operator.sub,
#         'BINARY_AND': operator.and_,
#         'BINARY_XOR': operator.xor,
#         'BINARY_OR': operator.or_,
#         'BINARY_SUBSCR': operator.getitem,
#         'BINARY_LSHIFT': operator.lshift,
#         'BINARY_RSHIFT': operator.rshift
#     }
#
#     INPLACE_OPERATIONS = {
#         'INPLACE_POWER': operator.ipow,
#         'INPLACE_MULTIPLY': operator.imul,
#         'INPLACE_FLOOR_DIVIDE': operator.ifloordiv,
#         'INPLACE_TRUE_DIVIDE': operator.itruediv,
#         'INPLACE_MODULO': operator.imod,
#         'INPLACE_ADD': operator.iadd,
#         'INPLACE_SUBTRACT': operator.isub,
#         'INPLACE_LSHIFT': operator.ilshift,
#         'INPLACE_RSHIFT': operator.irshift,
#         'INPLACE_AND': operator.iand,
#         'INPLACE_XOR': operator.ixor,
#         'INPLACE_OR': operator.ior
#     }
#
#     def __init__(self):
#         self.stack = [Frame()]
#
#     @staticmethod
#     def get_instructions(codeobject):
#         instructions = dict()
#         instructions_list = []
#         for instruction in dis.get_instructions(codeobject):
#             instructions[instruction.offset] = len(instructions_list)
#             instructions_list.append(instruction)
#         return instructions, instructions_list
#
#     def execute(self, instruction, instructions):
#         stack = self.stack[-1].data_stack
#         executor = InstructionExecutor(self.stack[-1], instruction, instructions)
#         if 'BINARY' in instruction.opname:
#             a = stack.pop()
#             b = stack.pop()
#             stack.append(
#                 VirtualMachine.BINARY_OPERATIONS[instruction.opname](b, a))
#         elif 'INPLACE' in instruction.opname:
#             a = stack.pop()
#             stack[-1] = VirtualMachine.INPLACE_OPERATIONS[instruction.opname](
#                 stack[-1], a)
#         elif instruction.opname in dir(InstructionExecutor):
#             return getattr(executor, instruction.opname)()
#
#     def run_code(self, code):
#         if isinstance(code, str):
#             code = compile(code, '', 'exec')
#
#         instructions, instructions_list = self.get_instructions(code)
#         current_instruction = 0
#         while current_instruction != len(instructions_list):
#             _execute_return = self.execute(
#                 instructions_list[current_instruction],
#                 instructions
#             )
#             while type(_execute_return) is int:
#                 current_instruction = _execute_return
#                 _execute_return = self.execute(
#                     instructions_list[current_instruction],
#                     instructions
#                 )
#             current_instruction += 1
#
#
# if __name__ == "__main__":
#     for inst in dis.get_instructions("""
# for i in range(20):
#     if i == 2:
#         break
# print(i)
# """):
#         print(inst)
    # vm = VirtualMachine()
    # vm.run_code("""print(1+1)""")
