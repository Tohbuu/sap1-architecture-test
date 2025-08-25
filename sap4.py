import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1440, 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("SAP-1 Architecture Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (180, 60, 240)
CYAN = (0, 200, 200)
DARK_BLUE = (0, 80, 160)

# Fonts
font = pygame.font.SysFont('consolas', 16)
title_font = pygame.font.SysFont('consolas', 24)
small_font = pygame.font.SysFont('consolas', 14)

class SAP1Simulator:
    def __init__(self):
        # Initialize all registers to zero (all zeroes)
        self.PC = 0    # Program Counter
        self.MAR = 0   # Memory Address Register
        self.ACC = 0   # Accumulator
        self.IR = 0    # Instruction Register
        self.TMP = 0   # Temporary Register
        self.OUT = 0   # Output Register
        
        # 16-byte memory for 
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
        
        # Initialize memory with user program
        self.initialize_memory_with_user_input()
    
    def get_user_input(self):
        """Get program instructions and data from user"""
        # Set up input screen
        input_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("SAP-1 Program Input")
        
        program_input = []
        data_input = {}
        current_input = ""
        input_mode = "program"  # or "data"
        current_address = 0
        message = "Enter program instructions (e.g., LDA 5, ADD 3, OUT, HLT). Type 'DATA' to switch to data input."
        
        input_font = pygame.font.SysFont('consolas', 18)
        title_font = pygame.font.SysFont('consolas', 24)
        
        input_rect = pygame.Rect(100, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 200, 40)
        program_rect = pygame.Rect(100, 100, SCREEN_WIDTH - 200, SCREEN_HEIGHT - 250)
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if current_input.upper() == "DATA":
                            input_mode = "data"
                            message = "Enter data values (e.g., 5 10 for address 5 value 10). Type 'DONE' when finished."
                        elif current_input.upper() == "DONE" and input_mode == "data":
                            running = False
                        else:
                            if input_mode == "program":
                                program_input.append((current_address, current_input))
                                current_address += 1
                            else:
                                parts = current_input.split()
                                if len(parts) == 2:
                                    try:
                                        addr = int(parts[0])
                                        value = int(parts[1])
                                        data_input[addr] = value
                                    except ValueError:
                                        message = "Invalid data format. Use: address value"
                        
                        current_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode
            
            input_screen.fill(WHITE)
            
            # Draw title
            title = title_font.render("SAP-1 Program Input", True, BLUE)
            input_screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
            
            # Draw message
            msg_text = input_font.render(message, True, BLACK)
            input_screen.blit(msg_text, (100, 70))
            
            # Draw input area
            pygame.draw.rect(input_screen, LIGHT_GRAY, input_rect)
            pygame.draw.rect(input_screen, BLACK, input_rect, 2)
            input_text = input_font.render(current_input, True, BLACK)
            input_screen.blit(input_text, (input_rect.x + 10, input_rect.y + 10))
            
            # Draw program/data display
            pygame.draw.rect(input_screen, LIGHT_GRAY, program_rect)
            pygame.draw.rect(input_screen, BLACK, program_rect, 2)
            
            y_pos = program_rect.y + 10
            if input_mode == "program":
                for addr, instr in program_input:
                    text = input_font.render(f"{addr:02X}: {instr}", True, BLUE)
                    input_screen.blit(text, (program_rect.x + 10, y_pos))
                    y_pos += 25
            else:
                for addr, value in data_input.items():
                    text = input_font.render(f"Address {addr}: {value} ({value:02X}h)", True, GREEN)
                    input_screen.blit(text, (program_rect.x + 10, y_pos))
                    y_pos += 25
            
            pygame.display.flip()
        
        # Return to main screen
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("SAP-1 Architecture Simulator")
        
        return program_input, data_input
    
    def initialize_memory_with_user_input(self):
        """Load user program into memory"""
        program_input, data_input = self.get_user_input()
        
        # Clear memory
        self.memory = [0] * 16
        
        # Parse program instructions
        opcode_map = {'LDA': 0x1, 'ADD': 0x2, 'SUB': 0x3, 'OUT': 0xE, 'HLT': 0xF, 'NOP': 0x0}
        
        for addr, instruction in program_input:
            parts = instruction.upper().split()
            if not parts:
                continue
                
            opcode_str = parts[0]
            if opcode_str in opcode_map:
                if opcode_str in ['LDA', 'ADD', 'SUB'] and len(parts) > 1:
                    try:
                        mem_addr = int(parts[1])
                        self.memory[addr] = (opcode_map[opcode_str] << 4) | mem_addr
                    except ValueError:
                        self.memory[addr] = opcode_map[opcode_str] << 4
                else:
                    self.memory[addr] = opcode_map[opcode_str] << 4
        
        # Load data values
        for addr, value in data_input.items():
            if addr < 16:
                self.memory[addr] = value
    
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
        
        return ' '.join(con_sequence)
    
    def fetch_cycle(self):
        """Execute the fetch cycle (T1-T3)"""
        # T1: MAR <- PC
        self.t_state = 1
        self.reset_control_signals()
        self.control_signals['Ep'] = 1  # Put PC on bus
        self.control_signals['Lm'] = 1  # Load MAR from bus
        self.MAR = self.PC  # This happens in hardware
        
        # T2: IR <- Memory[MAR], PC <- PC + 1
        self.t_state = 2
        self.reset_control_signals()
        self.control_signals['Ce'] = 1  # Enable PC increment
        self.control_signals['Li'] = 1  # Load IR from bus
        self.IR = self.memory[self.MAR]  # Memory puts value on bus, IR loads it
        self.PC += 1  # PC increments
        
        # T3: Decode instruction (no control signals needed)
        self.t_state = 3
        self.reset_control_signals()
    
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
            
            # T5: ACC <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['La'] = 1  # Load ACC from bus
            self.ACC = self.memory[self.MAR]  # Memory puts value on bus
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            
        elif opcode == 0x2:  # ADD - Add to Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.MAR = address
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.TMP = self.memory[self.MAR]  # Memory puts value on bus
            
            # T6: ACC <- ACC + TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.ACC += self.TMP  # ALU performs addition
            
        elif opcode == 0x3:  # SUB - Subtract from Accumulator
            # T4: MAR <- address from IR
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ei'] = 1  # Put IR on bus (lower 4 bits)
            self.control_signals['Lm'] = 1  # Load MAR from bus
            self.MAR = address
            
            # T5: TMP <- Memory[MAR]
            self.t_state = 5
            self.reset_control_signals()
            self.control_signals['Lb'] = 1  # Load TMP from bus
            self.TMP = self.memory[self.MAR]  # Memory puts value on bus
            
            # T6: ACC <- ACC - TMP
            self.t_state = 6
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Eu'] = 1  # Put ALU result on bus
            self.control_signals['La'] = 1  # Load ACC from bus
            self.control_signals['Su'] = 1  # Set ALU to subtract mode
            self.ACC -= self.TMP  # ALU performs subtraction
            
        elif opcode == 0xE:  # OUT - Output Accumulator
            # T4: OUT <- ACC
            self.t_state = 4
            self.reset_control_signals()
            self.control_signals['Ea'] = 1  # Put ACC on bus
            self.control_signals['Lo'] = 1  # Load OUT from bus
            self.OUT = self.ACC
            
            # T5: No operation
            self.t_state = 5
            self.reset_control_signals()
            
            # T6: No operation
            self.t_state = 6
            self.reset_control_signals()
            
        elif opcode == 0xF:  # HLT - Halt execution
            # T4: Halt
            self.t_state = 4
            self.reset_control_signals()
            return True  # Signal to stop execution
            
        return False

class SAP1Visualizer:
    def __init__(self, simulator):
        self.simulator = simulator
        self.current_step = 0
        self.execution_speed = 1.0  # seconds per step
        self.last_step_time = 0
        self.auto_advance = False
        self.execution_history = []
        self.memory_view_start = 0
        self.show_help = False
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        
    def scale_value(self, value, is_width=True):
        """Scale values based on current screen size"""
        base_dimension = SCREEN_WIDTH if is_width else SCREEN_HEIGHT
        current_dimension = self.screen_width if is_width else self.screen_height
        return int(value * current_dimension / base_dimension)
    
    def draw_register(self, x, y, width, height, name, value, active=False):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw register box
        color = YELLOW if active else LIGHT_GRAY
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw register name
        name_text = title_font.render(name, True, BLACK)
        screen.blit(name_text, (x + (width - name_text.get_width()) // 2, y + 10))
        
        # Draw register value
        value_text = font.render(f"{value:02X}h ({value})", True, BLUE)
        screen.blit(value_text, (x + (width - value_text.get_width()) // 2, y + height - 30))
        
        return pygame.Rect(x, y, width, height)
    
    def draw_bus(self, x, y, width, height, active=False):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw bus line
        color = RED if active else BLACK
        pygame.draw.rect(screen, color, (x, y, width, height), 2)
        
        # Draw bus label
        bus_text = font.render("BUS", True, BLACK)
        screen.blit(bus_text, (x + width + 5, y + height // 2 - 10))
        
        return pygame.Rect(x, y, width, height)
    
    def draw_memory(self, x, y, width, height):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw memory box
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw memory title
        mem_text = title_font.render("MEMORY (16 bytes)", True, BLACK)
        screen.blit(mem_text, (x + (width - mem_text.get_width()) // 2, y + 10))
        
        # Draw memory cells
        cell_height = self.scale_value(30, False)
        cells_x = x + 10
        cells_y = y + 50
        
        for i in range(16):
            addr = self.memory_view_start + i
            if addr < 16:
                # Draw address label
                addr_text = font.render(f"{addr:02X}", True, DARK_BLUE)
                screen.blit(addr_text, (cells_x, cells_y + i * cell_height))
                
                # Draw memory value
                value = self.simulator.memory[addr]
                value_text = font.render(f"{value:02X}", True, BLUE)
                screen.blit(value_text, (cells_x + 50, cells_y + i * cell_height))
                
                # Highlight current MAR address
                if addr == self.simulator.MAR:
                    pygame.draw.rect(screen, YELLOW, 
                                    (cells_x + 45, cells_y + i * cell_height, 30, 20), 2)
        
        # Draw scroll buttons if needed
        if self.memory_view_start > 0:
            pygame.draw.polygon(screen, BLUE, [(x + width - 20, y + 30), 
                                             (x + width - 10, y + 20), 
                                             (x + width, y + 30)])
        
        if self.memory_view_start < 8:
            pygame.draw.polygon(screen, BLUE, [(x + width - 20, y + height - 30), 
                                             (x + width - 10, y + height - 20), 
                                             (x + width, y + height - 30)])
        
        return pygame.Rect(x, y, width, height)
    
    def draw_alu(self, x, y, width, height):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw ALU box
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw ALU title
        alu_text = title_font.render("ALU", True, BLACK)
        screen.blit(alu_text, (x + (width - alu_text.get_width()) // 2, y + 10))
        
        # Draw operation
        op = "SUB" if self.simulator.control_signals.get('Su', 0) else "ADD"
        op_text = font.render(f"Operation: {op}", True, BLUE)
        screen.blit(op_text, (x + 10, y + 40))
        
        # Draw inputs
        acc_text = font.render(f"ACC: {self.simulator.ACC:02X}h", True, DARK_BLUE)
        screen.blit(acc_text, (x + 10, y + 70))
        
        tmp_text = font.render(f"TMP: {self.simulator.TMP:02X}h", True, DARK_BLUE)
        screen.blit(tmp_text, (x + 10, y + 90))
        
        # Draw result
        if self.simulator.control_signals.get('Su', 0):
            result = self.simulator.ACC - self.simulator.TMP
        else:
            result = self.simulator.ACC + self.simulator.TMP
            
        result_text = font.render(f"Result: {result:02X}h", True, GREEN)
        screen.blit(result_text, (x + 10, y + 120))
        
        return pygame.Rect(x, y, width, height)
    
    def draw_control_matrix(self, x, y, width, height):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw control matrix box
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw title
        title_text = title_font.render("CONTROL MATRIX", True, BLACK)
        screen.blit(title_text, (x + (width - title_text.get_width()) // 2, y + 10))
        
        # Draw control signals
        signals = [
            ('Cp', 'Counter enable'),
            ('Ep', 'PC to bus'),
            ('Lm', 'Load MAR'),
            ('Ce', 'Count enable'),
            ('Li', 'Load IR'),
            ('Ei', 'IR to bus'),
            ('La', 'Load ACC'),
            ('Ea', 'ACC to bus'),
            ('Su', 'ALU subtract'),
            ('Eu', 'ALU to bus'),
            ('Lb', 'Load TMP'),
            ('Lo', 'Load OUT')
        ]
        
        y_pos = y + 40
        for signal, description in signals:
            color = GREEN if self.simulator.control_signals.get(signal, 0) else RED
            signal_text = font.render(f"{signal}: {description}", True, color)
            screen.blit(signal_text, (x + 10, y_pos))
            y_pos += 25
        
        return pygame.Rect(x, y, width, height)
    
    def draw_output_panel(self, x, y, width, height):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw output panel
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw title
        title_text = title_font.render("OUTPUT", True, BLACK)
        screen.blit(title_text, (x + (width - title_text.get_width()) // 2, y + 10))
        
        # Draw output in different formats
        dec_text = font.render(f"Decimal: {self.simulator.OUT}", True, BLUE)
        screen.blit(dec_text, (x + 10, y + 40))
        
        hex_text = font.render(f"Hexadecimal: {self.simulator.OUT:02X}h", True, BLUE)
        screen.blit(hex_text, (x + 10, y + 70))
        
        bin_text = font.render(f"Binary: {self.simulator.OUT:08b}", True, BLUE)
        screen.blit(bin_text, (x + 10, y + 100))
        
        return pygame.Rect(x, y, width, height)
    
    def draw_instructions(self, x, y, width, height):
        # Scale dimensions
        x = self.scale_value(x)
        y = self.scale_value(y, False)
        width = self.scale_value(width)
        height = self.scale_value(height, False)
        
        # Draw instruction panel
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        
        # Draw title
        title_text = title_font.render("INSTRUCTIONS", True, BLACK)
        screen.blit(title_text, (x + (width - title_text.get_width()) // 2, y + 10))
        
        # Draw current instruction
        opcode = self.simulator.IR >> 4
        address = self.simulator.IR & 0x0F
        instruction = self.simulator.instructions.get(opcode, 'UNK')
        
        instr_text = font.render(f"Current: {instruction} {address if address else ''}", True, BLUE)
        screen.blit(instr_text, (x + 10, y + 40))
        
        # Draw T-state
        tstate_text = font.render(f"T-State: T{self.simulator.t_state}", True, GREEN)
        screen.blit(tstate_text, (x + 10, y + 70))
        
        # Draw PC
        pc_text = font.render(f"Program Counter: {self.simulator.PC:02X}h", True, DARK_BLUE)
        screen.blit(pc_text, (x + 10, y + 100))
        
        # Draw control sequence
        con_text = font.render(f"CON: {self.simulator.print_control_sequence()}", True, PURPLE)
        screen.blit(con_text, (x + 10, y + 130))
        
        return pygame.Rect(x, y, width, height)
    
    def draw_buttons(self):
        # Draw control buttons
        button_y = self.scale_value(SCREEN_HEIGHT - 50, False)
        button_width = self.scale_value(120)
        button_height = self.scale_value(40, False)
        button_spacing = self.scale_value(20)
        
        buttons = []
        
        # Step button
        step_rect = pygame.Rect(self.scale_value(20), button_y, button_width, button_height)
        pygame.draw.rect(screen, GREEN, step_rect)
        pygame.draw.rect(screen, BLACK, step_rect, 2)
        step_text = font.render("Step", True, BLACK)
        screen.blit(step_text, (step_rect.x + (button_width - step_text.get_width()) // 2, 
                               step_rect.y + (button_height - step_text.get_height()) // 2))
        buttons.append(("step", step_rect))
        
        # Auto button
        auto_color = ORANGE if self.auto_advance else BLUE
        auto_rect = pygame.Rect(self.scale_value(20) + button_width + button_spacing, button_y, button_width, button_height)
        pygame.draw.rect(screen, auto_color, auto_rect)
        pygame.draw.rect(screen, BLACK, auto_rect, 2)
        auto_text = font.render("Auto", True, BLACK)
        screen.blit(auto_text, (auto_rect.x + (button_width - auto_text.get_width()) // 2, 
                               auto_rect.y + (button_height - auto_text.get_height()) // 2))
        buttons.append(("auto", auto_rect))
        
        # Reset button
        reset_rect = pygame.Rect(self.scale_value(20) + 2 * (button_width + button_spacing), button_y, button_width, button_height)
        pygame.draw.rect(screen, RED, reset_rect)
        pygame.draw.rect(screen, BLACK, reset_rect, 2)
        reset_text = font.render("Reset", True, BLACK)
        screen.blit(reset_text, (reset_rect.x + (button_width - reset_text.get_width()) // 2, 
                                reset_rect.y + (button_height - reset_text.get_height()) // 2))
        buttons.append(("reset", reset_rect))
        
        # Speed buttons
        speed_text = font.render("Speed:", True, BLACK)
        screen.blit(speed_text, (self.scale_value(20) + 3 * (button_width + button_spacing), button_y + 10))
        
        # Faster button
        faster_rect = pygame.Rect(self.scale_value(20) + 3 * (button_width + button_spacing) + self.scale_value(70), button_y, self.scale_value(40), button_height)
        pygame.draw.rect(screen, CYAN, faster_rect)
        pygame.draw.rect(screen, BLACK, faster_rect, 2)
        faster_text = font.render("+", True, BLACK)
        screen.blit(faster_text, (faster_rect.x + (self.scale_value(40) - faster_text.get_width()) // 2, 
                                 faster_rect.y + (button_height - faster_text.get_height()) // 2))
        buttons.append(("faster", faster_rect))
        
        # Slower button
        slower_rect = pygame.Rect(self.scale_value(20) + 3 * (button_width + button_spacing) + self.scale_value(120), button_y, self.scale_value(40), button_height)
        pygame.draw.rect(screen, PURPLE, slower_rect)
        pygame.draw.rect(screen, BLACK, slower_rect, 2)
        slower_text = font.render("-", True, BLACK)
        screen.blit(slower_text, (slower_rect.x + (self.scale_value(40) - slower_text.get_width()) // 2, 
                                 slower_rect.y + (button_height - slower_text.get_height()) // 2))
        buttons.append(("slower", slower_rect))
        
        # Help button
        help_rect = pygame.Rect(self.screen_width - self.scale_value(100), self.scale_value(10, False), self.scale_value(80), self.scale_value(30, False))
        pygame.draw.rect(screen, ORANGE, help_rect)
        pygame.draw.rect(screen, BLACK, help_rect, 2)
        help_text = font.render("Help", True, BLACK)
        screen.blit(help_text, (help_rect.x + (self.scale_value(80) - help_text.get_width()) // 2, 
                               help_rect.y + (self.scale_value(30, False) - help_text.get_height()) // 2))
        buttons.append(("help", help_rect))
        
        return buttons
    
    def draw_help(self):
        # Draw help overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Draw help content
        help_rect = pygame.Rect(self.screen_width // 8, self.screen_height // 8, self.screen_width * 3 // 4, self.screen_height * 3 // 4)
        pygame.draw.rect(screen, WHITE, help_rect)
        pygame.draw.rect(screen, BLACK, help_rect, 3)
        
        title = title_font.render("SAP-1 Simulator Help", True, BLUE)
        screen.blit(title, (help_rect.x + (help_rect.width - title.get_width()) // 2, help_rect.y + 20))
        
        help_texts = [
            "SAP-1 (Simple As Possible) is a basic 8-bit computer architecture",
            "designed for educational purposes.",
            "",
            "CONTROLS:",
            "- Step: Execute one T-state",
            "- Auto: Automatically execute T-states",
            "- Reset: Reset the simulator",
            "- +/-: Adjust execution speed",
            "",
            "ARCHITECTURE COMPONENTS:",
            "- Program Counter (PC): Holds the address of the next instruction",
            "- Memory Address Register (MAR): Holds the address for memory access",
            "- Instruction Register (IR): Holds the current instruction",
            "- Accumulator (ACC): Stores arithmetic results",
            "- Temporary Register (TMP): Stores operands for ALU operations",
            "- Output Register (OUT): Holds the output value",
            "- ALU: Performs arithmetic operations (addition and subtraction)",
            "- Control Matrix: Generates control signals for each T-state",
            "",
            "Press any key to close this help"
        ]
        
        y_pos = help_rect.y + 70
        for text in help_texts:
            text_surface = font.render(text, True, BLACK)
            screen.blit(text_surface, (help_rect.x + 20, y_pos))
            y_pos += 25
    
    def draw(self):
        # Clear screen
        screen.fill(WHITE)
        
        # Draw title
        title = title_font.render("SAP-1 Architecture Simulator", True, BLUE)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 10))
        
        # Draw components
        bus_rect = self.draw_bus(150, 100, self.screen_width - 300, 4, any(self.simulator.control_signals.values()))
        
        # Left side components
        pc_rect = self.draw_register(50, 150, 100, 80, "PC", self.simulator.PC, 
                                    self.simulator.control_signals.get('Ep', 0))
        mar_rect = self.draw_register(50, 250, 100, 80, "MAR", self.simulator.MAR, 
                                     self.simulator.control_signals.get('Lm', 0))
        acc_rect = self.draw_register(50, 450, 100, 80, "ACC", self.simulator.ACC, 
                                     self.simulator.control_signals.get('La', 0) or 
                                     self.simulator.control_signals.get('Ea', 0))
        
        # Center components
        mem_rect = self.draw_memory(self.screen_width // 2 - 120, 150, 240, 300)
        alu_rect = self.draw_alu(self.screen_width // 2 - 80, 470, 160, 150)
        
        # Right side components
        ir_rect = self.draw_register(self.screen_width - 150, 150, 100, 80, "IR", self.simulator.IR, 
                                    self.simulator.control_signals.get('Li', 0) or 
                                    self.simulator.control_signals.get('Ei', 0))
        tmp_rect = self.draw_register(self.screen_width - 150, 250, 100, 80, "TMP", self.simulator.TMP, 
                                     self.simulator.control_signals.get('Lb', 0))
        out_rect = self.draw_register(self.screen_width - 150, 350, 100, 80, "OUT", self.simulator.OUT, 
                                     self.simulator.control_signals.get('Lo', 0))
        
        # Bottom panels
        control_rect = self.draw_control_matrix(20, 550, 350, 200)
        output_rect = self.draw_output_panel(390, 550, 250, 200)
        instr_rect = self.draw_instructions(660, 550, 250, 200)
        
        # Draw connections (simplified)
        if self.simulator.control_signals.get('Ep', 0):  # PC to bus
            pygame.draw.line(screen, RED, 
                            (pc_rect.x + pc_rect.width, pc_rect.y + pc_rect.height // 2),
                            (bus_rect.x, pc_rect.y + pc_rect.height // 2), 2)
        
        if self.simulator.control_signals.get('Lm', 0):  # Bus to MAR
            pygame.draw.line(screen, RED, 
                            (bus_rect.x + bus_rect.width, mar_rect.y + mar_rect.height // 2),
                            (mar_rect.x, mar_rect.y + mar_rect.height // 2), 2)
        
        if self.simulator.control_signals.get('Ei', 0):  # IR to bus
            pygame.draw.line(screen, RED, 
                            (ir_rect.x, ir_rect.y + ir_rect.height // 2),
                            (bus_rect.x + bus_rect.width, ir_rect.y + ir_rect.height // 2), 2)
        
        if self.simulator.control_signals.get('Ea', 0):  # ACC to bus
            pygame.draw.line(screen, RED, 
                            (acc_rect.x + acc_rect.width, acc_rect.y + acc_rect.height // 2),
                            (bus_rect.x, acc_rect.y + acc_rect.height // 2), 2)
        
        if self.simulator.control_signals.get('Eu', 0):  # ALU to bus
            pygame.draw.line(screen, RED, 
                            (alu_rect.x + alu_rect.width // 2, alu_rect.y),
                            (alu_rect.x + alu_rect.width // 2, bus_rect.y), 2)
        
        # Draw buttons
        buttons = self.draw_buttons()
        
        # Draw help if needed
        if self.show_help:
            self.draw_help()
        
        return buttons
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.VIDEORESIZE:
                # Update screen dimensions
                self.screen_width, self.screen_height = event.size
                screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            
            if self.show_help and event.type == pygame.KEYDOWN:
                self.show_help = False
                return True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check button clicks
                    buttons = self.draw()
                    for btn_name, btn_rect in buttons:
                        if btn_rect.collidepoint(mouse_pos):
                            if btn_name == "step":
                                self.step_simulation()
                            elif btn_name == "auto":
                                self.auto_advance = not self.auto_advance
                            elif btn_name == "reset":
                                self.reset_simulation()
                            elif btn_name == "faster":
                                self.execution_speed = max(0.1, self.execution_speed * 0.7)
                            elif btn_name == "slower":
                                self.execution_speed = min(2.0, self.execution_speed * 1.3)
                            elif btn_name == "help":
                                self.show_help = True
                    
                    # Check memory scroll
                    mem_rect = pygame.Rect(self.screen_width // 2 - self.scale_value(120), 
                                          self.scale_value(150, False), 
                                          self.scale_value(240), 
                                          self.scale_value(300, False))
                    if mem_rect.collidepoint(mouse_pos):
                        if mouse_pos[0] > mem_rect.x + mem_rect.width - self.scale_value(30):
                            if mouse_pos[1] < mem_rect.y + self.scale_value(30, False):
                                self.memory_view_start = max(0, self.memory_view_start - 1)
                            elif mouse_pos[1] > mem_rect.y + mem_rect.height - self.scale_value(30, False):
                                self.memory_view_start = min(8, self.memory_view_start + 1)
        
        # Auto-advance if enabled
        current_time = time.time()
        if self.auto_advance and current_time - self.last_step_time > self.execution_speed:
            self.step_simulation()
            self.last_step_time = current_time
        
        return True
    
    def step_simulation(self):
        if self.simulator.t_state == 0:
            self.simulator.fetch_cycle()
        elif self.simulator.t_state == 3:
            halt = self.simulator.execute_cycle()
            if halt:
                self.auto_advance = False
        elif self.simulator.t_state == 6:
            self.simulator.t_state = 0
        else:
            if self.simulator.t_state < 3:
                self.simulator.fetch_cycle()
            else:
                self.simulator.execute_cycle()
        
        # Record execution state
        state = {
            'PC': self.simulator.PC,
            'MAR': self.simulator.MAR,
            'ACC': self.simulator.ACC,
            'IR': self.simulator.IR,
            'TMP': self.simulator.TMP,
            'OUT': self.simulator.OUT,
            't_state': self.simulator.t_state,
            'control_signals': self.simulator.control_signals.copy()
        }
        self.execution_history.append(state)
        
        self.current_step += 1
    
    def reset_simulation(self):
        self.simulator = SAP1Simulator()
        self.current_step = 0
        self.execution_history = []
        self.auto_advance = False
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

# Main function
def main():
    # Create simulator
    simulator = SAP1Simulator()
    
    # Run visualization
    visualizer = SAP1Visualizer(simulator)
    visualizer.run()

if __name__ == "__main__":
    main()