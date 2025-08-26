class SAP1Simulator:
    def __init__(self, interactive=True):
        self.PC = 0
        self.MAR = 0
        self.ACC = 0
        self.IR = 0
        self.TMP = 0
        self.OUT = 0

        self.memory = [0] * 16

        self.control_signals = {
            'Cp': 0, 'Ep': 0, 'Lm': 0, 'Ce': 0, 'Li': 0, 'Ei': 0,
            'La': 0, 'Ea': 0, 'Su': 0, 'Eu': 0, 'Lb': 0, 'Lo': 0
        }

        self.t_state = 0

        self.instructions = {
            0x0: 'NOP',
            0x1: 'LDA',
            0x2: 'ADD',
            0x3: 'SUB',
            0xE: 'OUT',
            0xF: 'HLT'
        }

        self.last_alu_result = None

        if interactive:
            self.initialize_memory_with_user_input()

    def get_user_input(self):
        """Get program instructions and data from user"""
        print("SAP-1 PROGRAM INPUT")
        print("=" * 50)
        print("Available instructions:")
        print("LDA addr - Load from memory address")
        print("ADD addr - Add value from memory address")
        print("SUB addr - Subtract value from memory address")
        print("OUT      - Output accumulator value")
        print("HLT      - Halt execution")
        print("\nEnter your program (enter 'done' when finished):")

        program = []
        data_values = {}
        address_counter = 0

        while True:
            user_input = input(f"Address {address_counter:02X}: ").strip()
            if user_input.upper() == 'DONE':
                break

            if not user_input:
                address_counter += 1
                continue

            parts = user_input.split()
            if len(parts) == 0:
                continue

            instruction = parts[0].upper()

            if instruction in ('LDA', 'ADD', 'SUB') and len(parts) == 2:
                try:
                    addr = int(parts[1], 0)
                    if addr < 0 or addr > 0x0F:
                        print("Address must be 0-15 (0x0-0xF).")
                        continue
                    program.append((instruction, addr, address_counter))
                    address_counter += 1
                except ValueError:
                    print("Invalid address format. Use decimal or hex (0xNN).")

            elif instruction == 'OUT':
                program.append(('OUT', None, address_counter))
                address_counter += 1

            elif instruction == 'HLT':
                program.append(('HLT', None, address_counter))
                address_counter += 1

            else:
                print("Invalid instruction. Use: LDA addr, ADD addr, SUB addr, OUT, HLT")

        print("\nEnter data values (enter 'done' when finished):")
        while True:
            user_input = input("Enter 'address value' (e.g., '9 10'): ").strip()
            if user_input.upper() == 'DONE':
                break
            parts = user_input.split()
            if len(parts) == 2:
                try:
                    addr = int(parts[0], 0)
                    value = int(parts[1], 0)
                    if not (0 <= addr < 16):
                        print("Address out of range (0-15).")
                        continue
                    data_values[addr] = value & 0xFF
                except ValueError:
                    print("Invalid format. Use: address value (decimal or 0x hex)")
            else:
                print("Invalid format. Use: address value")

        return program, data_values

    def initialize_memory_with_user_input(self):
        """Load user program into memory"""
        program, data_values = self.get_user_input()

        self.memory = [0] * 16

        opcode_map = {'LDA': 0x1, 'ADD': 0x2, 'SUB': 0x3, 'OUT': 0xE, 'HLT': 0xF}

        for instruction, addr, mem_addr in program:
            if mem_addr >= len(self.memory):
                print(f"Warning: Address {mem_addr} out of memory range!")
                continue

            if instruction in ['LDA', 'ADD', 'SUB']:
                opcode = opcode_map[instruction]
                if addr < 0 or addr > 0x0F:
                    print(f"Warning: operand address {addr} out of 4-bit range; masking to low 4 bits.")
                operand = addr & 0x0F
                self.memory[mem_addr] = ((opcode & 0x0F) << 4) | operand
            else:
                self.memory[mem_addr] = (opcode_map[instruction] & 0x0F) << 4

        for addr, value in data_values.items():
            if addr >= len(self.memory):
                print(f"Warning: Address {addr} out of memory range!")
                continue
            self.memory[addr] = value & 0xFF

    def reset_control_signals(self):
        """Turn off all control signals"""
        for signal in self.control_signals:
            self.control_signals[signal] = 0
        self.last_alu_result = None

    def print_control_sequence(self):
        """Display the current control sequence in CON format"""
        signals = ['Cp', 'Ep', 'Lm', 'Ce', 'Li', 'Ei', 'La', 'Ea', 'Su', 'Eu', 'Lb', 'Lo']
        con_sequence = []

        for signal in signals:
            if self.control_signals.get(signal, 0):
                con_sequence.append(signal)
            else:
                con_sequence.append(f"~{signal}")

        print(f"CON = {' '.join(con_sequence)}")

    def print_state(self, step_description):
        """Display the current state of the simulation"""
        opcode = self.IR >> 4
        address = self.IR & 0x0F

        print(f"\n{step_description}")
        print(f"T-state: T{self.t_state}")
        print(f"PC: {self.PC:02X}, MAR: {self.MAR:02X}, IR: {self.IR:02X} ({self.instructions.get(opcode, 'UNK')} {address}), ACC: {self.ACC:02X}, TMP: {self.TMP:02X}, OUT: {self.OUT:02X}")

        active_signals = [signal for signal, value in self.control_signals.items() if value]
        print("Control signals: " + (" ".join(active_signals) if active_signals else "None"))

        self.print_control_sequence()

        if self.control_signals['Ep']:
            print(f"Bus: PC -> {self.PC:02X}")
        elif self.control_signals['Ei']:
            print(f"Bus: IR -> {self.IR:02X}")
        elif self.control_signals['Ea'] and not self.control_signals['Eu']:
            print(f"Bus: ACC -> {self.ACC:02X}")
        elif self.control_signals['Eu']:
            if self.last_alu_result is not None:
                result = self.last_alu_result & 0xFF
            else:
                result = (self.ACC - self.TMP) & 0xFF if self.control_signals['Su'] else (self.ACC + self.TMP) & 0xFF
            print(f"Bus: ALU -> {result:02X}")

        print("-" * 60)

    def fetch_cycle(self):
        """Execute the fetch cycle (T1-T3)"""
        self.t_state = 1
        self.reset_control_signals()
        self.control_signals['Ep'] = 1
        self.control_signals['Lm'] = 1
        self.MAR = self.PC
        self.print_state("FETCH T1: MAR <- PC")

        self.t_state = 2
        self.reset_control_signals()
        self.control_signals['Ce'] = 1
        self.control_signals['Li'] = 1
        self.IR = self.memory[self.MAR] & 0xFF
        self.PC += 1
        self.print_state("FETCH T2: IR <- Memory[MAR], PC <- PC+1")

        self.t_state = 3
        self.reset_control_signals()
        self.print_state("FETCH T3: Decode Instruction")

    def execute_cycle(self):
        """Execute the appropriate instruction (T4-T6)"""
        opcode = self.IR >> 4
        address = self.IR & 0x0F

        if opcode == 0x1:
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1
            self.control_signals['Lm'] = 1
            self.MAR = address
            self.print_state("EXECUTE LDA T4: MAR <- address from IR")

            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['La'] = 1
            self.ACC = self.memory[self.MAR] & 0xFF
            self.print_state("EXECUTE LDA T5: ACC <- Memory[MAR]")

            self.t_state = 6
            self.reset_control_signals()
            self.print_state("EXECUTE LDA T6: No operation")

        elif opcode == 0x2:
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1
            self.control_signals['Lm'] = 1
            self.MAR = address
            self.print_state("EXECUTE ADD T4: MAR <- address from IR")

            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1
            self.TMP = self.memory[self.MAR] & 0xFF
            self.print_state("EXECUTE ADD T5: TMP <- Memory[MAR]")

            self.t_state = 6
            self.reset_control_signals()
            alu_result = (self.ACC + self.TMP) & 0xFF
            self.last_alu_result = alu_result
            self.control_signals['Eu'] = 1
            self.control_signals['La'] = 1
            self.ACC = alu_result
            self.print_state("EXECUTE ADD T6: ACC <- ACC + TMP")

        elif opcode == 0x3:
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1
            self.control_signals['Lm'] = 1
            self.MAR = address
            self.print_state("EXECUTE SUB T4: MAR <- address from IR")

            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1
            self.TMP = self.memory[self.MAR] & 0xFF
            self.print_state("EXECUTE SUB T5: TMP <- Memory[MAR]")

            self.t_state = 6
            self.reset_control_signals()
            alu_result = (self.ACC - self.TMP) & 0xFF
            self.last_alu_result = alu_result
            self.control_signals['Eu'] = 1
            self.control_signals['La'] = 1
            self.control_signals['Su'] = 1
            self.ACC = alu_result
            self.print_state("EXECUTE SUB T6: ACC <- ACC - TMP")

        elif opcode == 0xE:
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ea'] = 1
            self.control_signals['Lo'] = 1
            self.OUT = self.ACC
            self.print_state("EXECUTE OUT T4: OUT <- ACC")

            self.t_state = 5
            self.reset_control_signals()
            self.print_state("EXECUTE OUT T5: No operation")

            self.t_state = 6
            self.reset_control_signals()
            self.print_state("EXECUTE OUT T6: No operation")

        elif opcode == 0xF:
            self.t_state = 4
            self.reset_control_signals()
            self.print_state("EXECUTE HLT T4: HALT")
            return True

        return False

    def run(self):
        """Run the complete simulation"""
        print("\nSAP-1 SIMULATION")
        print("=" * 60)

        print("\nInitial Memory Contents:")
        for i in range(0, 16, 4):
            mem_values = [f"{self.memory[j]:02X}" for j in range(i, min(i+4, 16))]
            print(f"Address {i:02X}-{min(i+3, 15):02X}: {' '.join(mem_values)}")

        print("\nDetailed Memory Contents:")
        for i in range(16):
            val = self.memory[i]
            binv = f"{val:08b}"
            hexv = f"{val:02X}"
            decv = val
            opcode = val >> 4
            mnemonic = self.instructions.get(opcode, 'DATA')
            print(f"Address {i:02X}: binary {binv} = hex {hexv} = dec {decv} | opcode {opcode:01X} = {mnemonic}")

        print("\nStarting Execution:")
        print("=" * 60)

        halt = False
        instruction_count = 0

        while not halt and self.PC < len(self.memory) and instruction_count < 20:
            self.fetch_cycle()
            halt = self.execute_cycle()
            instruction_count += 1

        print("\nFINAL RESULTS:")
        print("=" * 60)
        print(f"Output register: {self.OUT:02X} (Decimal: {self.OUT})")
        print(f"Program completed: {'Yes' if halt else 'No'}")
        # Run the simulation
if __name__ == "__main__":
    simulator = SAP1Simulator()
    simulator.run()