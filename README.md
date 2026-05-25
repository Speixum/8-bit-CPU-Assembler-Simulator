# 8-bit-CPU-Assembler-Simulator
一个基于 Python 实现的极简 8 位 CPU 模拟器 + 汇编器，支持汇编代码编译、指令执行、数据输出，可运行斐波那契数列等基础程序。
🌟 项目特性
完整 8 位 CPU 硬件模拟（寄存器、内存、标志位、指令执行）
专用汇编器，支持标签、立即数、注释解析
256 字节内存空间，0xFF 端口为输出打印
开箱即用，无第三方依赖
包含斐波那契数列示例程序
📁 项目结构
plaintext
mini-8bit-cpu/
├── asm8.py    # 汇编器（将汇编代码转为机器码）
├── cpu8.py    # 8 位 CPU 模拟器核心
├── fib.asm    # 斐波那契数列汇编程序
└── README.md  # 项目说明
🚀 快速开始
环境要求
Python 3.6 及以上版本
运行程序
克隆 / 下载项目到本地
直接运行主程序：
bash
运行
python asm8.py
程序会自动加载 fib.asm，编译并执行，输出完整斐波那契数列
📋 支持指令集
表格
指令	功能说明
NOP	空操作
LDA	从内存加载数据到累加器 A
STA	将 A 存入内存（0xFF 为输出）
LDI	加载立即数到 A
TAB/TBA	A/B 寄存器数据互传
ADD	加法运算（设置进位标志）
SUB	减法运算
AND/OR/XOR	位运算
JMP	无条件跳转
JZ/JNZ	零标志跳转
JC/JNC	进位标志跳转
HLT	停机
🧪 示例程序：斐波那契数列
fib.asm 代码：
asm
; 8位CPU斐波那契数列
; 输出 0,1,1,2,3,5...233 后自动停机
LDI  0
STA  0xFF
LDI  1
STA  0x80
STA  0xFF
LDI  0
STA  0x81

loop:
LDA  0x80
TAB
ADD  0x81
JC   done
STA  0xFF
STA  0x80
TBA
STA  0x81
JMP  loop

done:
HLT
运行效果
plaintext
加载汇编源文件: fib.asm
==================================================
→ OUTPUT: 0  (dec)  /  0x00
→ OUTPUT: 1  (dec)  /  0x01
→ OUTPUT: 1  (dec)  /  0x01
→ OUTPUT: 2  (dec)  /  0x02
...
→ OUTPUT: 233 (dec) /  0xE9

执行结果:
输出序列: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
🛠 扩展功能
新增汇编程序：新建 .asm 文件即可运行
扩展指令集：在 asm8.py 和 cpu8.py 中添加指令定义与逻辑
自定义功能：累加计算、循环计数、数值比较等
📄 许可证
MIT License，自由使用与修改
