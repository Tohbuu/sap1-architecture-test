import pygame
import sys
import time

class SAP1VisualSimulator:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SAP-1 Architecture Simulator")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 120, 255)
        self.YELLOW = (255, 255, 0)
        self.GRAY = (100, 100, 100)
        self.LIGHT_BLUE = (173, 216, 230)
        
        # Fonts
        self.font_large = pygame.font.SysFont('Arial', 24)
        self.font_medium = pygame.font.SysFont('Arial', 20)
        self.font_small = pygame.font.SysFont('Arial', 16)
        
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
            0x0: 'NOP',
            0x1: 'LDA',
            0x2: 'ADD',
            0x3: 'SUB',
            0xE: 'OUT',
            0xF: 'HLT'
        }
        
        # Animation state
        self.bus_value = 0
        self.bus_source = ""
        self.bus_dest = ""
        self.animation_progress = 0
        self.current_step_description = ""
        
        # Initialize memory with user program
        self.initialize_memory_with_user_input()
        
        # Define component positions
        self.define_component_positions()
    
    def define_component_positions(self):
        # Define positions for all components in the block diagram
        self.positions = {
            'PC': (100, 150),
            'MAR': (100, 250),
            'RAM': (100, 350),
            'IR': (300, 150),
            'Controller': (300, 250),
            'ACC': (500, 150),
            'ALU': (500, 250),
            'TMP': (500, 350),
            'OUT': (700, 150),
            'Bus': (300, 450),
        }
    
    def get_user_input(self):
        # Create a simple text input interface
        input_active = True
        program = []
        data_values = {}
        address_counter = 0
        current_input = ""
        message = "Enter program instructions (LDA addr, ADD addr, SUB addr, OUT, HLT)"
        
        while input_active:
            self.screen.fill(self.BLACK)
            
            # Display instructions
            title = self.font_large.render("SAP-1 PROGRAM INPUT", True, self.WHITE)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 30))
            
            instr = self.font_medium.render("Available instructions: LDA addr, ADD addr, SUB addr, OUT, HLT", True, self.WHITE)
            self.screen.blit(instr, (self.width//2 - instr.get_width()//2, 70))
            
            msg = self.font_medium.render(message, True, self.YELLOW)
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, 110))
            
            # Display current program
            y_pos = 150
            for i, (instr, addr, mem_addr) in enumerate(program):
                text = f"Address {mem_addr:02X}: {instr} {addr if addr is not None else ''}"
                txt = self.font_small.render(text, True, self.WHITE)
                self.screen.blit(txt, (self.width//2 - 200, y_pos))
                y_pos += 25
            
            # Display input box
            pygame.draw.rect(self.screen, self.WHITE, (self.width//2 - 200, 400, 400, 40), 2)
            input_text = self.font_medium.render(current_input, True, self.WHITE)
            self.screen.blit(input_text, (self.width//2 - 190, 405))
            
            # Display instructions
            help_text = [
                "Press ENTER to submit instruction",
                "Type 'done' to finish program input",
                "Type 'data' to enter data values"
            ]
            
            y_pos = 450
            for text in help_text:
                txt = self.font_small.render(text, True, self.LIGHT_BLUE)
                self.screen.blit(txt, (self.width//2 - 200, y_pos))
                y_pos += 25
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_input.upper() == 'DONE':
                            input_active = False
                        elif current_input.upper() == 'DATA':
                            # Switch to data input mode
                            data_values = self.get_data_input()
                            message = "Enter program instructions (or 'done' to finish)"
                        else:
                            # Parse instruction
                            parts = current_input.upper().split()
                            if len(parts) > 0:
                                instruction = parts[0]
                                
                                if instruction == 'LDA' and len(parts) == 2:
                                    try:
                                        addr = int(parts[1], 16) if parts[1].startswith('0X') else int(parts[1])
                                        program.append(('LDA', addr, address_counter))
                                        address_counter += 1
                                        message = f"Added LDA {addr} at address {address_counter-1:02X}"
                                    except ValueError:
                                        message = "Invalid address format. Use decimal or hex (0x format)"
                                        
                                elif instruction == 'ADD' and len(parts) == 2:
                                    try:
                                        addr = int(parts[1], 16) if parts[1].startswith('0X') else int(parts[1])
                                        program.append(('ADD', addr, address_counter))
                                        address_counter += 1
                                        message = f"Added ADD {addr} at address {address_counter-1:02X}"
                                    except ValueError:
                                        message = "Invalid address format. Use decimal or hex (0x format)"
                                        
                                elif instruction == 'SUB' and len(parts) == 2:
                                    try:
                                        addr = int(parts[1], 16) if parts[1].startswith('0X') else int(parts[1])
                                        program.append(('SUB', addr, address_counter))
                                        address_counter += 1
                                        message = f"Added SUB {addr} at address {address_counter-1:02X}"
                                    except ValueError:
                                        message = "Invalid address format. Use decimal or hex (0x format)"
                                        
                                elif instruction == 'OUT':
                                    program.append(('OUT', None, address_counter))
                                    address_counter += 1
                                    message = f"Added OUT at address {address_counter-1:02X}"
                                    
                                elif instruction == 'HLT':
                                    program.append(('HLT', None, address_counter))
                                    address_counter += 1
                                    message = f"Added HLT at address {address_counter-1:02X}"
                                    
                                else:
                                    message = "Invalid instruction. Use: LDA addr, ADD addr, SUB addr, OUT, HLT"
                            
                            current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode
        
        return program, data_values
    
    def get_data_input(self):
        data_values = {}
        input_active = True
        current_input = ""
        message = "Enter data values as 'address value' (e.g., '9 10')"
        
        while input_active:
            self.screen.fill(self.BLACK)
            
            # Display instructions
            title = self.font_large.render("DATA INPUT", True, self.WHITE)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 30))
            
            msg = self.font_medium.render(message, True, self.YELLOW)
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, 70))
            
            # Display current data
            y_pos = 110
            for addr, value in data_values.items():
                text = f"Address {addr:02X}: {value:02X} ({value})"
                txt = self.font_small.render(text, True, self.WHITE)
                self.screen.blit(txt, (self.width//2 - 200, y_pos))
                y_pos += 25
            
            # Display input box
            pygame.draw.rect(self.screen, self.WHITE, (self.width//2 - 200, 400, 400, 40), 2)
            input_text = self.font_medium.render(current_input, True, self.WHITE)
            self.screen.blit(input_text, (self.width//2 - 190, 405))
            
            # Display instructions
            help_text = [
                "Press ENTER to submit data",
                "Type 'done' to finish data input",
            ]
            
            y_pos = 450
            for text in help_text:
                txt = self.font_small.render(text, True, self.LIGHT_BLUE)
                self.screen.blit(txt, (self.width//2 - 200, y_pos))
                y_pos += 25
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_input.upper() == 'DONE':
                            input_active = False
                        else:
                            # Parse data input
                            parts = current_input.split()
                            if len(parts) == 2:
                                try:
                                    addr = int(parts[0], 16) if parts[0].startswith('0X') else int(parts[0])
                                    value = int(parts[1], 16) if parts[1].startswith('0X') else int(parts[1])
                                    data_values[addr] = value
                                    message = f"Added value {value} at address {addr:02X}"
                                except ValueError:
                                    message = "Invalid format. Use: address value"
                            else:
                                message = "Invalid format. Use: address value"
                            
                            current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode
        
        return data_values
    
    def initialize_memory_with_user_input(self):
        """Load user program into memory"""
        program, data_values = self.get_user_input()
        
        # Clear memory
        self.memory = [0] * 16
        
        # Load program instructions
        opcode_map = {'LDA': 0x1, 'ADD': 0x2, 'SUB': 0x3, 'OUT': 0xE, 'HLT': 0xF}
        
        for instruction, addr, mem_addr in program:
            if mem_addr >= len(self.memory):
                print(f"Warning: Address {mem_addr} out of memory range!")
                continue
                
            if instruction in ['LDA', 'ADD', 'SUB']:
                opcode = opcode_map[instruction]
                self.memory[mem_addr] = (opcode << 4) | addr
            else:
                self.memory[mem_addr] = opcode_map[instruction] << 4
        
        # Load data values
        for addr, value in data_values.items():
            if addr >= len(self.memory):
                print(f"Warning: Address {addr} out of memory range!")
                continue
            self.memory[addr] = value
    
    def reset_control_signals(self):
        """Turn off all control signals"""
        for signal in self.control_signals:
            self.control_signals[signal] = 0
    
    def draw_component(self, name, value, position, active=False):
        x, y = position
        color = self.GREEN if active else self.BLUE
        
        # Draw component box
        pygame.draw.rect(self.screen, color, (x, y, 120, 60), 0, 5)
        pygame.draw.rect(self.screen, self.WHITE, (x, y, 120, 60), 2, 5)
        
        # Draw component name
        name_text = self.font_small.render(name, True, self.WHITE)
        self.screen.blit(name_text, (x + 60 - name_text.get_width()//2, y + 5))
        
        # Draw component value
        value_text = self.font_small.render(f"{value:02X}", True, self.WHITE)
        self.screen.blit(value_text, (x + 60 - value_text.get_width()//2, y + 30))
    
    def draw_bus(self):
        # Draw the data bus
        bus_x, bus_y = self.positions['Bus']
        pygame.draw.rect(self.screen, self.GRAY, (50, bus_y, self.width - 100, 40), 0, 5)
        
        # Draw bus label
        bus_text = self.font_medium.render("DATA BUS", True, self.WHITE)
        self.screen.blit(bus_text, (self.width//2 - bus_text.get_width()//2, bus_y - 25))
        
        # Draw current bus value if any
        if self.bus_value > 0:
            value_text = self.font_medium.render(f"{self.bus_value:02X}", True, self.YELLOW)
            self.screen.blit(value_text, (self.width//2 - value_text.get_width()//2, bus_y + 10))
            
            # Draw bus activity animation
            if self.bus_source and self.bus_dest:
                progress = self.animation_progress
                if progress < 100:
                    self.animation_progress += 2
                
                # Draw animation from source to destination
                src_pos = self.positions.get(self.bus_source, (0, 0))
                dst_pos = self.positions.get(self.bus_dest, (0, 0))
                
                # Calculate intermediate position
                progress_pct = progress / 100
                mid_x = src_pos[0] + (dst_pos[0] - src_pos[0]) * progress_pct
                mid_y = src_pos[1] + (dst_pos[1] - src_pos[1]) * progress_pct
                
                # Draw line
                pygame.draw.line(self.screen, self.YELLOW, (src_pos[0] + 60, src_pos[1] + 30), 
                                (mid_x + 60, mid_y + 30), 3)
                
                if progress >= 100:
                    # Animation complete, update the destination
                    if self.bus_dest == "MAR":
                        self.MAR = self.bus_value
                    elif self.bus_dest == "IR":
                        self.IR = self.bus_value
                    elif self.bus_dest == "ACC":
                        self.ACC = self.bus_value
                    elif self.bus_dest == "TMP":
                        self.TMP = self.bus_value
                    elif self.bus_dest == "OUT":
                        self.OUT = self.bus_value
                    
                    # Reset animation
                    self.bus_value = 0
                    self.bus_source = ""
                    self.bus_dest = ""
                    self.animation_progress = 0
    
    def draw_control_signals(self):
        # Draw control signals
        signals_x, signals_y = 900, 150
        title = self.font_medium.render("CONTROL SIGNALS", True, self.WHITE)
        self.screen.blit(title, (signals_x, signals_y - 30))
        
        signals = list(self.control_signals.keys())
        for i, signal in enumerate(signals):
            y_pos = signals_y + i * 30
            color = self.GREEN if self.control_signals[signal] else self.RED
            signal_text = self.font_small.render(signal, True, color)
            self.screen.blit(signal_text, (signals_x, y_pos))
    
    def draw_memory(self):
        # Draw memory contents
        mem_x, mem_y = 900, 350
        title = self.font_medium.render("MEMORY CONTENTS", True, self.WHITE)
        self.screen.blit(title, (mem_x, mem_y - 30))
        
        for i in range(0, 16, 4):
            y_pos = mem_y + (i//4) * 30
            addrs = f"{i:02X}-{i+3:02X}:"
            values = " ".join([f"{self.memory[j]:02X}" for j in range(i, i+4)])
            
            addr_text = self.font_small.render(addrs, True, self.WHITE)
            value_text = self.font_small.render(values, True, self.YELLOW)
            
            self.screen.blit(addr_text, (mem_x, y_pos))
            self.screen.blit(value_text, (mem_x + 70, y_pos))
    
    def draw_status(self):
        # Draw current status information
        status_x, status_y = 50, 550
        
        # Draw T-state
        t_text = self.font_medium.render(f"T-State: T{self.t_state}", True, self.WHITE)
        self.screen.blit(t_text, (status_x, status_y))
        
        # Draw current step description
        if self.current_step_description:
            desc_text = self.font_small.render(self.current_step_description, True, self.YELLOW)
            self.screen.blit(desc_text, (status_x, status_y + 30))
        
        # Draw register values
        regs_x = status_x + 250
        regs = [
            f"PC: {self.PC:02X}",
            f"MAR: {self.MAR:02X}", 
            f"ACC: {self.ACC:02X}",
            f"IR: {self.IR:02X}",
            f"TMP: {self.TMP:02X}",
            f"OUT: {self.OUT:02X}"
        ]
        
        for i, reg in enumerate(regs):
            y_pos = status_y + i * 25
            reg_text = self.font_small.render(reg, True, self.WHITE)
            self.screen.blit(reg_text, (regs_x, y_pos))
    
    def draw_instructions(self):
        # Draw instruction decoding
        instr_x, instr_y = 500, 550
        opcode = self.IR >> 4
        address = self.IR & 0x0F
        
        instr_name = self.instructions.get(opcode, 'UNK')
        instr_text = self.font_medium.render(f"Instruction: {instr_name} {address}", True, self.WHITE)
        self.screen.blit(instr_text, (instr_x, instr_y))
    
    def draw_buttons(self):
        # Draw control buttons
        button_y = 650
        buttons = [
            ("Step", 200, button_y),
            ("Run", 400, button_y),
            ("Reset", 600, button_y),
            ("Quit", 800, button_y)
        ]
        
        for text, x, y in buttons:
            pygame.draw.rect(self.screen, self.BLUE, (x, y, 100, 40), 0, 5)
            pygame.draw.rect(self.screen, self.WHITE, (x, y, 100, 40), 2, 5)
            btn_text = self.font_medium.render(text, True, self.WHITE)
            self.screen.blit(btn_text, (x + 50 - btn_text.get_width()//2, y + 10))
    
    def draw(self):
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw title
        title = self.font_large.render("SAP-1 ARCHITECTURE SIMULATOR", True, self.WHITE)
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 10))
        
        # Draw all components
        self.draw_component("PC", self.PC, self.positions['PC'], self.control_signals['Ep'])
        self.draw_component("MAR", self.MAR, self.positions['MAR'], self.control_signals['Lm'])
        self.draw_component("RAM", self.memory[self.MAR] if self.MAR < len(self.memory) else 0, 
                          self.positions['RAM'], False)
        self.draw_component("IR", self.IR, self.positions['IR'], self.control_signals['Li'] or self.control_signals['Ei'])
        self.draw_component("ACC", self.ACC, self.positions['ACC'], self.control_signals['La'] or self.control_signals['Ea'])
        self.draw_component("ALU", self.ACC + self.TMP if not self.control_signals['Su'] else self.ACC - self.TMP, 
                          self.positions['ALU'], self.control_signals['Eu'])
        self.draw_component("TMP", self.TMP, self.positions['TMP'], self.control_signals['Lb'])
        self.draw_component("OUT", self.OUT, self.positions['OUT'], self.control_signals['Lo'])
        
        # Draw the data bus
        self.draw_bus()
        
        # Draw control signals
        self.draw_control_signals()
        
        # Draw memory contents
        self.draw_memory()
        
        # Draw status information
        self.draw_status()
        
        # Draw instruction decoding
        self.draw_instructions()
        
        # Draw control buttons
        self.draw_buttons()
        
        pygame.display.flip()
    
    def simulate_bus_transfer(self, value, source, destination):
        """Simulate a bus transfer with animation"""
        self.bus_value = value
        self.bus_source = source
        self.bus_dest = destination
        self.animation_progress = 0
        
        # Wait for animation to complete
        while self.bus_value > 0:
            self.draw()
            time.sleep(0.01)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
    def fetch_cycle(self):
        """Execute the fetch cycle (T1-T3)"""
        # T1: MAR <- PC
        self.t_state = 1
        self.reset_control_signals()
        self.control_signals['Ep'] = 1  # Put PC on bus
        self.control_signals['Lm'] = 1  # Load MAR from bus
        self.current_step_description = "FETCH T1: MAR <- PC"
        self.draw()
        self.simulate_bus_transfer(self.PC, "PC", "MAR")
        time.sleep(0.5)
        
        # T2: IR <- Memory[MAR], PC <- PC + 1
        self.t_state = 2
        self.reset_control_signals()
        self.control_signals['Ce'] = 1  # Enable PC increment
        self.control_signals['Li'] = 1  # Load IR from bus
        self.current_step_description = "FETCH T2: IR <- Memory[MAR], PC <- PC+1"
        self.draw()
        
        # Simulate memory read
        memory_value = self.memory[self.MAR] if self.MAR < len(self.memory) else 0
        self.simulate_bus_transfer(memory_value, "RAM", "IR")
        self.PC += 1  # PC increments
        time.sleep(0.5)
        
        # T3: Decode instruction (no control signals needed)
        self.t_state = 3
        self.reset_control_signals()
        self.current_step_description = "FETCH T3: Decode Instruction"
        self.draw()
        time.sleep(0.5)
    
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
            self.current_step_description = "EXECUTE LDA T4: MAR <- address from IR"
            self.draw()
            self.simulate_bus_transfer(address, "IR", "MAR")
            time.sleep(0.5)
            
            # T5: ACC <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['La'] = 1  # Load ACC from bus
            self.current_step_description = "EXECUTE LDA T5: ACC <- Memory[MAR]"
            self.draw()
            memory_value = self.memory[self.MAR] if self.MAR < len(self.memory) else 0
            self.simulate_bus_transfer(memory_value, "RAM", "ACC")
            time.sleep(0.5)
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            self.current_step_description = "EXECUTE LDA T6: No operation"
            self.draw()
            time.sleep(0.5)
            
        elif opcode == 0x2:  # ADD - Add to Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.current_step_description = "EXECUTE ADD T4: MAR <- address from IR"
            self.draw()
            self.simulate_bus_transfer(address, "IR", "MAR")
            time.sleep(0.5)
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.current_step_description = "EXECUTE ADD T5: TMP <- Memory[MAR]"
            self.draw()
            memory_value = self.memory[self.MAR] if self.MAR < len(self.memory) else 0
            self.simulate_bus_transfer(memory_value, "RAM", "TMP")
            time.sleep(0.5)
            
            # T6: ACC <- ACC + TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.current_step_description = "EXECUTE ADD T6: ACC <- ACC + TMP"
            self.draw()
            alu_result = self.ACC + self.TMP
            self.simulate_bus_transfer(alu_result, "ALU", "ACC")
            time.sleep(0.5)
            
        elif opcode == 0x3:  # SUB - Subtract from Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.current_step_description = "EXECUTE SUB T4: MAR <- address from IR"
            self.draw()
            self.simulate_bus_transfer(address, "IR", "MAR")
            time.sleep(0.5)
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.current_step_description = "EXECUTE SUB T5: TMP <- Memory[MAR]"
            self.draw()
            memory_value = self.memory[self.MAR] if self.MAR < len(self.memory) else 0
            self.simulate_bus_transfer(memory_value, "RAM", "TMP")
            time.sleep(0.5)
            
            # T6: ACC <- ACC - TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.control_signals['Su'] = 1  # Set ALU to subtract mode
            self.current_step_description = "EXECUTE SUB T6: ACC <- ACC - TMP"
            self.draw()
            alu_result = self.ACC - self.TMP
            self.simulate_bus_transfer(alu_result, "ALU", "ACC")
            time.sleep(0.5)
            
        elif opcode == 0xE:  # OUT - Output Accumulator
            # T4: OUT <- ACC
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Lo'] = 1  # Load OUT from bus
            self.current_step_description = "EXECUTE OUT T4: OUT <- ACC"
            self.draw()
            self.simulate_bus_transfer(self.ACC, "ACC", "OUT")
            time.sleep(0.5)
            
            # T5: No operation
            self.t_state = 5
            self.reset_control_signals()
            self.current_step_description = "EXECUTE OUT T5: No operation"
            self.draw()
            time.sleep(0.5)
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            self.current_step_description = "EXECUTE OUT T6: No operation"
            self.draw()
            time.sleep(0.5)
            
        elif opcode == 0xF:  # HLT - Halt execution
            # T4: Halt
            self.t_state = 4
            self.reset_control_signals()
            self.current_step_description = "EXECUTE HLT T4: HALT"
            self.draw()
            time.sleep(0.5)
            return True  # Signal to stop execution
            
        return False
    
    def reset_simulation(self):
        """Reset the simulation to initial state"""
        self.PC = 0
        self.MAR = 0
        self.ACC = 0
        self.IR = 0
        self.TMP = 0
        self.OUT = 0
        self.t_state = 0
        self.reset_control_signals()
        self.bus_value = 0
        self.bus_source = ""
        self.bus_dest = ""
        self.animation_progress = 0
        self.current_step_description = ""
    
    def run(self):
        """Run the complete simulation"""
        running = True
        simulation_active = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if buttons were clicked
                    x, y = event.pos
                    
                    # Step button
                    if 200 <= x <= 300 and 650 <= y <= 690:
                        if not simulation_active:
                            self.fetch_cycle()
                            simulation_active = self.execute_cycle()
                    
                    # Run button
                    elif 400 <= x <= 500 and 650 <= y <= 690:
                        # Run complete simulation
                        halt = False
                        while not halt:
                            self.fetch_cycle()
                            halt = self.execute_cycle()
                            self.draw()
                            time.sleep(0.5)
                        simulation_active = True
                    
                    # Reset button
                    elif 600 <= x <= 700 and 650 <= y <= 690:
                        self.reset_simulation()
                        simulation_active = False
                    
                    # Quit button
                    elif 800 <= x <= 900 and 650 <= y <= 690:
                        running = False
            
            # Draw the current state
            self.draw()
            time.sleep(0.05)
        
        pygame.quit()

# Run the simulation
if __name__ == "__main__":
    simulator = SAP1VisualSimulator()
    simulator.run()