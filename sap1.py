class SAP1Simulator:
    def __init__(self):
        # Initialize all registers to zero
        self.PC = 0    # Program Counter
        self.MAR = 0   # Memory Address Register
        self.ACC = 0   # Accumulator
        self.IR = 0    # Instruction Register
        self.TMP = 0   # Temporary Register
        self.OUT = 0   # Output Register
        
        # 16-byte memory
        self.memory = [0] * 16
        
        # Control signals (all initially off)
        self.control_signals = {
            'Cp': 0, 'Ep': 0, 'Lm': 0, 'Ce': 0, 'Li': 0, 'Ei': 0,
            'La': 0, 'Ea': 0, 'Su': 0, 'Eu': 0, 'Lb': 0, 'Lo': 0
        }
        
        # Current T-state
        self.t_state = 0
        
        # Instruction mapping (opcode to mnemonic)
        self.instructions = {
            0x0: 'NOP', # NOP
            0x1: 'LDA', # Load Accumulator
            0x2: 'ADD', # Add
            0x3: 'SUB', # Subtract
            0xE: 'OUT', # Output
            0xF: 'HLT'  # Halt
        }
        
        # Initialize memory with our program
        self.initialize_memory()
    
    def initialize_memory(self):
        """Initialize memory with a simple program"""
        # instruction sets for LDA ADD SUB OUT and HLT 
        # Instructions (first nibble = opcode, second = address)
        self.memory[0] = 0x19   # LDA 9  (0001 1001)
        self.memory[1] = 0x2A   # ADD 10 (0010 1010)
        self.memory[2] = 0x3B   # SUB 11 (0011 1011)
        self.memory[3] = 0xE0   # OUT    (1110 0000)
        self.memory[4] = 0xF0   # HLT    (1111 0000)
        
        # Data pang input
        self.memory[9] = 45     # Value 45
        self.memory[10] = 25     # Value 25
        self.memory[11] = 100     # Value 100
    
    def reset_control_signals(self):
        """Turn off all control signals"""
        for signal in self.control_signals:
            self.control_signals[signal] = 0
    
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
        
        # Show active control signals
        active_signals = [signal for signal, value in self.control_signals.items() if value]
        print("Control signals: " + (" ".join(active_signals) if active_signals else "None"))
        
        # Show control sequence in CON format
        self.print_control_sequence()
        
        # Show bus activity if any
        if self.control_signals['Ep']:
            print(f"Bus: PC -> {self.PC:02X}")
        elif self.control_signals['Ei']:
            print(f"Bus: IR -> {self.IR:02X}")
        elif self.control_signals['Ea']:
            print(f"Bus: ACC -> {self.ACC:02X}")
        elif self.control_signals['Eu']:
            result = self.ACC - self.TMP if self.control_signals['Su'] else self.ACC + self.TMP
            print(f"Bus: ALU -> {result:02X}")
        
        print("-" * 60)
    
    def fetch_cycle(self):
        """Execute the fetch cycle (T1-T3)"""
        # T1: MAR <- PC
        self.t_state = 1
        self.reset_control_signals()
        self.control_signals['Ep'] = 1  # Put PC on bus
        self.control_signals['Lm'] = 1  # Load MAR from bus
        self.MAR = self.PC  # This happens in hardware
        self.print_state("FETCH T1: MAR <- PC")
        
        # T2: IR <- Memory[MAR], PC <- PC + 1
        self.t_state = 2
        self.reset_control_signals()
        self.control_signals['Ce'] = 1  # Enable PC increment
        self.control_signals['Li'] = 1  # Load IR from bus
        self.IR = self.memory[self.MAR]  # Memory puts value on bus, IR loads it
        self.PC += 1  # PC increments
        self.print_state("FETCH T2: IR <- Memory[MAR], PC <- PC+1")
        
        # T3: Decode instruction (no control signals needed)
        self.t_state = 3
        self.reset_control_signals()
        self.print_state("FETCH T3: Decode Instruction")
    
    def execute_cycle(self):
        """Execute the appropriate instruction (T4-T6)"""
        opcode = self.IR >> 4
        address = self.IR & 0x0F
        
        if opcode == 0x1:  # LDA - Load Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.MAR = address
            self.print_state("EXECUTE LDA T4: MAR <- address from IR")
            
            # T5: ACC <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['La'] = 1  # Load ACC from bus
            self.ACC = self.memory[self.MAR]  # Memory puts value on bus
            self.print_state("EXECUTE LDA T5: ACC <- Memory[MAR]")
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            self.print_state("EXECUTE LDA T6: No operation")
            
        elif opcode == 0x2:  # ADD - Add to Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.MAR = address
            self.print_state("EXECUTE ADD T4: MAR <- address from IR")
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.TMP = self.memory[self.MAR]  # Memory puts value on bus
            self.print_state("EXECUTE ADD T5: TMP <- Memory[MAR]")
            
            # T6: ACC <- ACC + TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.ACC += self.TMP  # ALU performs addition
            self.print_state("EXECUTE ADD T6: ACC <- ACC + TMP")
            
        elif opcode == 0x3:  # SUB - Subtract from Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.MAR = address
            self.print_state("EXECUTE SUB T4: MAR <- address from IR")
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.TMP = self.memory[self.MAR]  # Memory puts value on bus
            self.print_state("EXECUTE SUB T5: TMP <- Memory[MAR]")
            
            # T6: ACC <- ACC - TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.control_signals['Su'] = 1  # Set ALU to subtract mode
            self.ACC -= self.TMP  # ALU performs subtraction
            self.print_state("EXECUTE SUB T6: ACC <- ACC - TMP")
            
        elif opcode == 0xE:  # OUT - Output Accumulator
            # T4: OUT <- ACC
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Lo'] = 1  # Load OUT from bus
            self.OUT = self.ACC
            self.print_state("EXECUTE OUT T4: OUT <- ACC")
            
            # T5: No operation
            self.t_state = 5
            self.reset_control_signals()
            self.print_state("EXECUTE OUT T5: No operation")
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            self.print_state("EXECUTE OUT T6: No operation")
            
        elif opcode == 0xF:  # HLT - Halt execution
            # T4: Halt
            self.t_state = 4
            self.reset_control_signals()
            self.print_state("EXECUTE HLT T4: HALT")
            return True  # Signal to stop execution
            
        return False
    
    def run(self):
        """Run the complete simulation"""
        print("SAP-1 SIMULATION: 10 + 5 - 2")
        print("=" * 60)
        
        # Display initial memory contents
        print("\nInitial Memory Contents:")
        for i in range(0, 16, 4):
            mem_values = [f"{self.memory[j]:02X}" for j in range(i, min(i+4, 16))]
            print(f"Address {i:02X}-{min(i+3, 15):02X}: {' '.join(mem_values)}")
        
        print("\nStarting Execution:")
        print("=" * 60)
        
        # Execute program until HLT or end of memory
        halt = False
        instruction_count = 0
        
        while not halt and self.PC < len(self.memory) and instruction_count < 10:
            self.fetch_cycle()
            halt = self.execute_cycle()
            instruction_count += 1
        
        # Display final results
        print("\nFINAL RESULTS:")
        print("=" * 60)
        print(f"Output register: {self.OUT} (Decimal: {self.OUT})")
        # ignore print expected result
        # print(f"Expected result: {10+5-2}")
        print(f"Program completed: {'Yes' if halt else 'No'}")

# Run the simulation
if __name__ == "__main__":
    simulator = SAP1Simulator()
    simulator.run()