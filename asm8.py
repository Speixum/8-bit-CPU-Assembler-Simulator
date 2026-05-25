# ============================================
# 8-bit CPU Assembler (asm8.py)
# 汇编器：将汇编代码转为机器码
# ============================================

class Assembler:
    def __init__(self):
        # 指令集 (指令名 -> 操作码)
        self.OPCODES = {
            'NOP': 0x00,
            'LDA': 0x01,
            'STA': 0x02,
            'LDI': 0x03,
            'TAB': 0x04,
            'TBA': 0x05,
            'ADD': 0x06,
            'SUB': 0x07,
            'AND': 0x08,
            'OR':  0x09,
            'XOR': 0x0A,
            'ADDB':0x0B,
            'SUBB':0x0C,
            'JMP': 0x10,
            'JZ':  0x11,
            'JNZ': 0x12,
            'JC':  0x13,
            'JNC': 0x14,
            'PSHA':0x15,
            'POPA':0x16,
            'CALL':0x17,
            'RET': 0x18,
            'RTS': 0x18,
            'HLT': 0x1A,
        }

        # 双字节指令 (操作码 + 操作数)
        self.TWO_BYTE = {
            'LDA', 'STA', 'LDI', 'ADD', 'SUB', 'AND', 'OR', 'XOR',
            'JMP', 'JZ', 'JNZ', 'JC', 'JNC', 'CALL'
        }

        self.labels = {}  # 标签地址表
        self.machine_code = []

    def preprocess(self, source):
        """预处理：去除注释、空行、分割token"""
        lines = source.split('\n')
        processed = []
        address = 0

        for line_num, line in enumerate(lines):
            line = line.strip()
            if not line or line.startswith(';'):
                continue

            # 去除注释
            if ';' in line:
                line = line.split(';')[0].strip()

            if not line:
                continue

            # 处理标签 (label:)
            if ':' in line:
                label, rest = line.split(':', 1)
                label = label.strip()
                rest = rest.strip()
                self.labels[label] = address
                if rest:
                    tokens = rest.split()
                    processed.append((address, tokens))
                    address += self._get_instr_size(tokens[0])
            else:
                tokens = line.split()
                processed.append((address, tokens))
                address += self._get_instr_size(tokens[0])

        return processed

    def _get_instr_size(self, instr):
        """获取指令长度（1/2字节）"""
        return 2 if instr in self.TWO_BYTE else 1

    def assemble(self, source):
        """两遍汇编：生成机器码"""
        self.labels.clear()
        self.machine_code.clear()

        # 第一遍：收集标签
        processed = self.preprocess(source)

        # 第二遍：生成机器码
        for addr, tokens in processed:
            instr = tokens[0].upper()
            if instr not in self.OPCODES:
                raise SyntaxError(f"未知指令: {instr} @ 地址 {addr}")

            opcode = self.OPCODES[instr]
            self.machine_code.append(opcode)

            # 处理操作数
            if instr in self.TWO_BYTE:
                if len(tokens) < 2:
                    raise SyntaxError(f"指令 {instr} 需要操作数 @ 地址 {addr}")

                operand = tokens[1]
                # 处理标签/立即数
                if operand in self.labels:
                    val = self.labels[operand]
                elif operand.startswith('0x'):
                    val = int(operand, 16)
                else:
                    val = int(operand)

                if not (0 <= val <= 255):
                    raise ValueError(f"操作数越界 (0-255): {val} @ 地址 {addr}")

                self.machine_code.append(val)

        return self.machine_code

    def print_code(self):
        """打印机器码"""
        print("\n机器码 (%d 字节):" % len(self.machine_code))
        hex_str = ' '.join(f'{b:02X}' for b in self.machine_code)
        print(f"  {hex_str}")
        print(f"标签表: {self.labels}")


# ============================================
# 主程序：汇编 + 运行
# ============================================
if __name__ == "__main__":
    from cpu8 import CPU8

    # 汇编文件
    asm_file = "fib.asm"

    # 修复：指定 UTF-8 编码读取文件
    print(f"加载汇编源文件: {asm_file}")
    with open(asm_file, 'r', encoding='utf-8') as f:
        source = f.read()

    # 汇编
    asm = Assembler()
    try:
        machine_code = asm.assemble(source)
        asm.print_code()
    except Exception as e:
        print(f"汇编错误: {e}")
        exit(1)

    # 加载并运行
    print("\n" + "="*50)
    cpu = CPU8()
    cpu.load(machine_code, 0x00)
    cpu.run()

    # 输出结果 ✅ 修复：output 改为 outputs
    print("\n执行结果:")
    print(f"输出序列: {cpu.outputs}")