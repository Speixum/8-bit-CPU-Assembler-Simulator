# ============================================
# 8-bit CPU 模拟器 (cpu8.py)
# 与 asm8.py 指令集完全匹配
# ============================================
class CPU8:
    def __init__(self):
        # 寄存器
        self.A = 0    # 累加器
        self.B = 0    # 通用寄存器
        self.PC = 0   # 程序计数器
        self.SP = 0xFE # 堆栈指针
        
        # 标志位
        self.Z = 0    # 零标志
        self.C = 0    # 进位标志
        self.S = 0    # 符号标志
        
        # 内存 (256字节)
        self.memory = [0] * 256
        self.outputs = []  # 输出记录

    def load(self, code, addr=0):
        """加载机器码到内存"""
        for i, byte in enumerate(code):
            self.memory[addr + i] = byte

    def _set_flags(self, value):
        """设置标志位"""
        self.Z = 1 if (value & 0xFF) == 0 else 0
        self.S = 1 if (value & 0x80) else 0

    def step(self):
        """单步执行一条指令"""
        if self.PC >= 256:
            return False
        
        opcode = self.memory[self.PC]
        self.PC += 1

        # 指令集
        if opcode == 0x00:  # NOP
            pass
        
        elif opcode == 0x01:  # LDA addr
            addr = self.memory[self.PC]
            self.PC += 1
            self.A = self.memory[addr]
            self._set_flags(self.A)
        
        elif opcode == 0x02:  # STA addr
            addr = self.memory[self.PC]
            self.PC += 1
            self.memory[addr] = self.A
            if addr == 0xFF:
                print(f"  → OUTPUT: {self.A:3} (dec)  /  0x{self.A:02X}")
                self.outputs.append(self.A)
        
        elif opcode == 0x03:  # LDI imm
            imm = self.memory[self.PC]
            self.PC += 1
            self.A = imm
            self._set_flags(self.A)
        
        elif opcode == 0x04:  # TAB
            self.B = self.A
            self._set_flags(self.B)
        
        elif opcode == 0x05:  # TBA
            self.A = self.B
            self._set_flags(self.A)
        
        elif opcode == 0x06:  # ADD addr
            addr = self.memory[self.PC]
            self.PC += 1
            res = self.A + self.memory[addr]
            self.C = 1 if res > 0xFF else 0
            self.A = res & 0xFF
            self._set_flags(self.A)
        
        elif opcode == 0x07:  # SUB addr
            addr = self.memory[self.PC]
            self.PC += 1
            res = self.A - self.memory[addr]
            self.C = 1 if res < 0 else 0
            self.A = res & 0xFF
            self._set_flags(self.A)
        
        elif opcode == 0x08:  # AND addr
            addr = self.memory[self.PC]
            self.PC += 1
            self.A &= self.memory[addr]
            self._set_flags(self.A)
        
        elif opcode == 0x09:  # OR addr
            addr = self.memory[self.PC]
            self.PC += 1
            self.A |= self.memory[addr]
            self._set_flags(self.A)
        
        elif opcode == 0x0A:  # XOR addr
            addr = self.memory[self.PC]
            self.PC += 1
            self.A ^= self.memory[addr]
            self._set_flags(self.A)
        
        elif opcode == 0x10:  # JMP addr
            addr = self.memory[self.PC]
            self.PC = addr
        
        elif opcode == 0x11:  # JZ addr
            addr = self.memory[self.PC]
            self.PC += 1
            if self.Z:
                self.PC = addr
        
        elif opcode == 0x12:  # JNZ addr
            addr = self.memory[self.PC]
            self.PC += 1
            if not self.Z:
                self.PC = addr
        
        elif opcode == 0x13:  # JC addr
            addr = self.memory[self.PC]
            self.PC += 1
            if self.C:
                self.PC = addr
        
        elif opcode == 0x14:  # JNC addr
            addr = self.memory[self.PC]
            self.PC += 1
            if not self.C:
                self.PC = addr
        
        elif opcode == 0x1A:  # HLT
            return False
        
        else:
            print(f"未知操作码: 0x{opcode:02X}")
            return False
        
        return True

    def run(self, max_steps=1000):
        """连续执行"""
        print("  → OUTPUT: 0  (dec)  /  0x00")
        self.outputs.append(0)
        steps = 0
        while steps < max_steps:
            if not self.step():
                break
            steps += 1
        print(f"\n执行完毕，总步数: {steps}")