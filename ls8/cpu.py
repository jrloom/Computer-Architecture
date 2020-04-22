"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256  # ? memory
        self.reg = [0] * 8  # ? registers
        self.pc = 0  # ? program counter
        self.sp = 7  # ? stack pointer
        self.running = False
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[HLT] = self.handle_HLT

    def load(self):
        prog = sys.argv[1]
        addr = 0

        with open(prog) as file:
            for line in file:
                # print(line, end="")

                line = line.split("#")  # ? removes #'s
                line = line[0].strip()  # ? grabs first index, removes formatting
                if line == "":  # ? removes blank lines
                    continue
                line = int(line, 2)  # ? converts str to binary int
                self.ram[addr] = line  # ? add to memory
                addr += 1  # ? iterate

        # sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    # ? takes RAM address, returns stored value
    def ram_read(self, addr):
        return self.ram[addr]

    # ? takes address & value, writes value to address in RAM
    def ram_write(self, addr, val):
        self.ram[addr] = val

    def handle_LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def handle_PRN(self, operand_a, operand_b):
        print(f"prints {self.reg[operand_a]}")

    def handle_MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def handle_HLT(self, operand_a, operand_b):
        self.running = False

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:
            instruction = self.ram_read(self.pc)
            inst_len = ((instruction & 0b11000000) >> 6) + 1

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            try:
                self.branchtable[instruction](operand_a, operand_b)

            except:
                print(f"something went wrong with {instruction}")

            self.pc += inst_len
