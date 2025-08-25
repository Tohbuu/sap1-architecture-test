# SAP-1 Architecture Overview(Python-translated)

### &nbsp;	Program Layout



SAMPLE PROBLEM

Simulate this problem in the terminal

1. 10+5-2



**SAP-1 PROGRAM INPUT**

==================================================

Available instructions:

LDA addr - Load from memory address

ADD addr - Add value from memory address

SUB addr - Subtract value from memory address

OUT      - Output accumulator value

HLT      - Halt execution



**Enter your program (enter 'done' when finished):**

Address 00: LDA 9

Address 01: ADD 10

Address 02: SUB 11

Address 03: OUT

Address 04: HLT

Address 05: done



**Addr (Hex)	Machine Code (Hex)	Machine Code (Binary)	Instruction**

0		19			0001 1001		LDA 9

1		2A			0010 1010		ADD 10

2		3B			0011 1011		SUB 11

3		E0			1110 0000		OUT

4		F0			1111 0000		HLT



**Enter data values (enter 'done' when finished):**

Enter 'address value' (e.g., '9 10'): 9 10

Enter 'address value' (e.g., '9 10'): 10 5

Enter 'address value' (e.g., '9 10'): 11 2

Enter 'address value' (e.g., '9 10'): done





**Addr (Hex)	Value (Hex)	Value (Binary)	Value (Dec)**

9		0A		0000 1010	10

A		05		0000 0101	5

B		02		0000 0010	2





**SAP-1 SIMULATION**

============================================================



Initial Memory Contents:

Address 00-03: 19 2A 3B E0

Address 04-07: F0 00 00 00

Address 08-0B: 00 0A 05 02

Address 0C-0F: 00 00 00 00







**Starting Execution:**

============================================================

**1**

FETCH T1: MAR <- PC

T-state: T1

PC: 00, MAR: 00, IR: 00 (NOP 0), ACC: 00, TMP: 00, OUT: 00

Control signals: Ep Lm

CON = ~Cp Ep Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: PC -> 00

---

**2**

FETCH T2: IR <- Memory\[MAR], PC <- PC+1

T-state: T2

PC: 01, MAR: 00, IR: 19 (LDA 9), ACC: 00, TMP: 00, OUT: 00

Control signals: Ce Li

CON = ~Cp ~Ep ~Lm Ce Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**3**

FETCH T3: Decode Instruction

T-state: T3

PC: 01, MAR: 00, IR: 19 (LDA 9), ACC: 00, TMP: 00, OUT: 00

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**4**

EXECUTE LDA T4: MAR <- address from IR

T-state: T4

PC: 01, MAR: 09, IR: 19 (LDA 9), ACC: 00, TMP: 00, OUT: 00

Control signals: Lm Ei

CON = ~Cp ~Ep Lm ~Ce ~Li Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: IR -> 19

---

**5**

EXECUTE LDA T5: ACC <- Memory\[MAR]

T-state: T5

PC: 01, MAR: 09, IR: 19 (LDA 9), ACC: 0A, TMP: 00, OUT: 00

Control signals: La

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei La ~Ea ~Su ~Eu ~Lb ~Lo

---

**6**

EXECUTE LDA T6: No operation

T-state: T6

PC: 01, MAR: 09, IR: 19 (LDA 9), ACC: 0A, TMP: 00, OUT: 00

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**7**

FETCH T1: MAR <- PC

T-state: T1

PC: 01, MAR: 01, IR: 19 (LDA 9), ACC: 0A, TMP: 00, OUT: 00

Control signals: Ep Lm

CON = ~Cp Ep Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: PC -> 01

---

**8**

FETCH T2: IR <- Memory\[MAR], PC <- PC+1

T-state: T2

PC: 02, MAR: 01, IR: 2A (ADD 10), ACC: 0A, TMP: 00, OUT: 00

Control signals: Ce Li

CON = ~Cp ~Ep ~Lm Ce Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**9**

FETCH T3: Decode Instruction

T-state: T3

PC: 02, MAR: 01, IR: 2A (ADD 10), ACC: 0A, TMP: 00, OUT: 00

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**10**

EXECUTE ADD T4: MAR <- address from IR

T-state: T4

PC: 02, MAR: 0A, IR: 2A (ADD 10), ACC: 0A, TMP: 00, OUT: 00

Control signals: Lm Ei

CON = ~Cp ~Ep Lm ~Ce ~Li Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: IR -> 2A

---

**11**

EXECUTE ADD T5: TMP <- Memory\[MAR]

T-state: T5

PC: 02, MAR: 0A, IR: 2A (ADD 10), ACC: 0A, TMP: 05, OUT: 00

Control signals: Lb

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu Lb ~Lo

---

**12**

EXECUTE ADD T6: ACC <- ACC + TMP

T-state: T6

PC: 02, MAR: 0A, IR: 2A (ADD 10), ACC: 0F, TMP: 05, OUT: 00

Control signals: La Ea Eu

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei La Ea ~Su Eu ~Lb ~Lo

Bus: ACC -> 0F

---

**13**

FETCH T1: MAR <- PC

T-state: T1

PC: 02, MAR: 02, IR: 2A (ADD 10), ACC: 0F, TMP: 05, OUT: 00

Control signals: Ep Lm

CON = ~Cp Ep Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: PC -> 02

---

**14**

FETCH T2: IR <- Memory\[MAR], PC <- PC+1

T-state: T2

PC: 03, MAR: 02, IR: 3B (SUB 11), ACC: 0F, TMP: 05, OUT: 00

Control signals: Ce Li

CON = ~Cp ~Ep ~Lm Ce Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**15**

FETCH T3: Decode Instruction

T-state: T3

PC: 03, MAR: 02, IR: 3B (SUB 11), ACC: 0F, TMP: 05, OUT: 00

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**16**

EXECUTE SUB T4: MAR <- address from IR

T-state: T4

PC: 03, MAR: 0B, IR: 3B (SUB 11), ACC: 0F, TMP: 05, OUT: 00

Control signals: Lm Ei

CON = ~Cp ~Ep Lm ~Ce ~Li Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: IR -> 3B

---

**17**

EXECUTE SUB T5: TMP <- Memory\[MAR]

T-state: T5

PC: 03, MAR: 0B, IR: 3B (SUB 11), ACC: 0F, TMP: 02, OUT: 00

Control signals: Lb

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu Lb ~Lo

---

**18**

EXECUTE SUB T6: ACC <- ACC - TMP

T-state: T6

PC: 03, MAR: 0B, IR: 3B (SUB 11), ACC: 0D, TMP: 02, OUT: 00

Control signals: La Ea Su Eu

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei La Ea Su Eu ~Lb ~Lo

Bus: ACC -> 0D

---

**19**

FETCH T1: MAR <- PC

T-state: T1

PC: 03, MAR: 03, IR: 3B (SUB 11), ACC: 0D, TMP: 02, OUT: 00

Control signals: Ep Lm

CON = ~Cp Ep Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: PC -> 03

---

**20**

FETCH T2: IR <- Memory\[MAR], PC <- PC+1

T-state: T2

PC: 04, MAR: 03, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 00

Control signals: Ce Li

CON = ~Cp ~Ep ~Lm Ce Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**21**

FETCH T3: Decode Instruction

T-state: T3

PC: 04, MAR: 03, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 00

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**22**

EXECUTE OUT T4: OUT <- ACC

T-state: T4

PC: 04, MAR: 03, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: Ea Lo

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La Ea ~Su ~Eu ~Lb Lo

Bus: ACC -> 0D

---

**23**

EXECUTE OUT T5: No operation

T-state: T5

PC: 04, MAR: 03, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**24**

EXECUTE OUT T6: No operation

T-state: T6

PC: 04, MAR: 03, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**25**

FETCH T1: MAR <- PC

T-state: T1

PC: 04, MAR: 04, IR: E0 (OUT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: Ep Lm

CON = ~Cp Ep Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

Bus: PC -> 04

---

**26**

FETCH T2: IR <- Memory\[MAR], PC <- PC+1

T-state: T2

PC: 05, MAR: 04, IR: F0 (HLT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: Ce Li

CON = ~Cp ~Ep ~Lm Ce Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**27**

FETCH T3: Decode Instruction

T-state: T3

PC: 05, MAR: 04, IR: F0 (HLT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---

**28**

EXECUTE HLT T4: HALT

T-state: T4

PC: 05, MAR: 04, IR: F0 (HLT 0), ACC: 0D, TMP: 02, OUT: 0D

Control signals: None

CON = ~Cp ~Ep ~Lm ~Ce ~Li ~Ei ~La ~Ea ~Su ~Eu ~Lb ~Lo

---



FINAL RESULTS:

============================================================

Output register: 0D (Decimal: 13)

Program completed: Yes





#  	THE PROCESS



**LDA = 0001 (1h), ADD = 0010 (2h), SUB = 0011 (3h), OUT = 1110 (Eh), HLT = 1111 (Fh)**



**Addr (Dec)	Addr (Hex)	Machine Code (Hex)	Machine Code (Binary)	Instruction	Meaning**

00		0h		19			0001 1001		LDA 9		Load from address 9h

01		1h		2A			0010 1010		ADD 10		Add from address Ah

02		2h		3B			0011 1011		SUB 11		Subtract from address Bh

03		3h		E0			1110 0000		OUT		Output ACC

04		4h		F0			1111 0000		HLT		Halt





**Addr (Dec)	Addr (Hex)	Value (Hex)	Value (Binary)	Value (Dec)	Purpose**

09		9h		0A		0000 1010	10		First number to add

10		Ah		05		0000 0101	5		Second number to add

11		Bh		02		0000 0010	2		Number to subtract



**Step-by-Step Execution**



### **Cycle 1: Fetching and Executing LDA 9**



**T1 (FETCH - Step 1): MAR <- PC**

Action: The Program Counter (00h) is placed on the bus and loaded into the Memory Address Register.

Bus Value: 00h (0000 0000)

Control Word: Ep Lm (Enable PC, Load MAR)





**T2 (FETCH - Step 2): IR <- RAM\[MAR], PC <- PC + 1**

Action: The CPU reads the value from RAM address 00h, which is 19h. This value is loaded into the Instruction Register (IR). The PC increments to 01h to point to the next instruction.

IR now holds: 19h (0001 1001). The Control Unit decodes this: 0001 = LDA, 1001 = address 9.

Control Word: Ce Li (Counter Enable, Load IR)





**T3 (FETCH - Step 3): Decode**

Action: The Control Unit decodes the opcode (LDA) and prepares the signals for the next T-states.

Control Word: All signals low (no operation).





**T4 (EXECUTE LDA - Step 1): MAR <- IR\[address]**

Action: The address part of the IR (9h) is placed on the bus and loaded into the MAR.

Bus Value: 09h (0000 1001)

Control Word: Lm Ei (Load MAR, Enable IR)





**T5 (EXECUTE LDA - Step 2): ACC <- RAM\[MAR]**

Action: The CPU reads the value from RAM address 09h, which is 0Ah (decimal 10). This value is loaded directly into the Accumulator (ACC).

ACC now holds: 0Ah (0000 1010)

Control Word: La (Load ACC)





**T6 (EXECUTE LDA - Step 3): No Op**

Action: The instruction is complete. The CPU uses this state to do nothing before the next fetch cycle begins.

Result: ACC = 10



### 

### **Cycle 2: Fetching and Executing ADD 10**



**T1, T2, T3 (FETCH): Same process as before.**

PC (01h) -> MAR.

RAM\[01h] (2Ah) -> IR. PC increments to 02h.

IR decoded: 0010 = ADD, 1010 = address 10 (Ah).





**T4 (EXECUTE ADD - Step 1): MAR <- IR\[address]**

Action: The address Ah from the IR is loaded into the MAR.

Bus Value: 0Ah (0000 1010)

Control Word: Lm Ei





**T5 (EXECUTE ADD - Step 2): TMP <- RAM\[MAR]**

Action: The CPU reads the value from RAM address 0Ah, which is 05h (decimal 5). This value is loaded into the Temporary Register (TMP). The ALU needs two inputs (ACC and TMP) to perform the addition.

TMP now holds: 05h (0000 0101)

Control Word: Lb (Load TMP)





**T6 (EXECUTE ADD - Step 3): ACC <- ACC + TMP**

Action: The ALU adds the values in the ACC (0Ah) and TMP (05h). The result is placed on the bus and loaded back into the ACC.

Calculation: 0Ah (10) + 05h (5) = 0Fh (15)

Bus Value: 0Fh (0000 1111)

ACC now holds: 0Fh (0000 1111)

Control Word: La Ea Eu (Load ACC, Enable ACC, Enable ALU)

Result: ACC = 15





### **Cycle 3: Fetching and Executing SUB 11**



**T1, T2, T3 (FETCH):**

PC (02h) -> MAR.

RAM\[02h] (3Bh) -> IR. PC increments to 03h.

IR decoded: 0011 = SUB, 1011 = address 11 (Bh).





**T4 (EXECUTE SUB - Step 1): MAR <- IR\[address]**

Action: The address Bh from the IR is loaded into the MAR.

Bus Value: 0Bh (0000 1011)

Control Word: Lm Ei





**T5 (EXECUTE SUB - Step 2): TMP <- RAM\[MAR]**

Action: The CPU reads the value from RAM address 0Bh, which is 02h (decimal 2). This value is loaded into the TMP.

TMP now holds: 02h (0000 0010)

Control Word: Lb





**T6 (EXECUTE SUB - Step 3): ACC <- ACC - TMP**

Action: The ALU subtracts the TMP (02h) from the ACC (0Fh). The result is placed on the bus and loaded back into the ACC.

Calculation: 0Fh (15) - 02h (2) = 0Dh (13)

Bus Value: 0Dh (0000 1101)

ACC now holds: 0Dh (0000 1101)

Control Word: La Ea Su Eu (Load ACC, Enable ACC, Subtract, Enable ALU)

Result: ACC = 13



### **Cycle 4: Fetching and Executing OUT**



**T1, T2, T3 (FETCH):**

PC (03h) -> MAR.

RAM\[03h] (E0h) -> IR. PC increments to 04h.

IR decoded: 1110 = OUT. The address part (0000) is ignored.



**T4 (EXECUTE OUT - Step 1): OUT <- ACC**

Action: The value in the ACC (0Dh) is placed on the bus and loaded into the Output Register.

Bus Value: 0Dh (0000 1101)

OUT now holds: 0Dh (Decimal: 13)

Control Word: Ea Lo (Enable ACC, Load OUT)

This is the RESULT of our program!



**T5, T6 (EXECUTE OUT - Steps 2 \& 3): No Op**

The OUT instruction is complete.





### **Cycle 5: Fetching and Executing HLT**



**T1, T2, T3 (FETCH):**

PC (04h) -> MAR.

RAM\[04h] (F0h) -> IR. PC increments to 05h.

IR decoded: 1111 = HLT.



**T4 (EXECUTE HLT - Step 1): HALT**

Action: The Control Unit stops generating clock signals. The program execution ends.

Final Output Register Value: 0Dh (Binary: 0000 1101, Hex: 0D, Decimal: 13)







### **SUMMARY**

**Step	Instruction	Action				ACC Value (Dec)		Key Bus Activity**

1	LDA 9		Load 10 into ACC		10			Bus moves 0A from RAM to ACC

2	ADD 10		Add 5 to ACC (10+5)		15			Bus moves 05 to TMP, then 0F to ACC

3	SUB 11		Subtract 2 from ACC (15-2)	13			Bus moves 02 to TMP, then 0D to ACC

4	OUT		Display ACC value (13)		13			Bus moves 0D from ACC to OUT Register

5	HLT		Stop Program			13			-

