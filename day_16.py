from math import prod

with open('day_16_input.txt') as f:
    input_line = f.read()

def get_section_to_int(binary_str: str, start_index: int, length: int) -> int:
    return int(binary_str[start_index:start_index+length], 2)

def get_section_to_str(binary_str: str, start_index: int, length: int) -> str:
    return binary_str[start_index:start_index+length]

class TurningTape():
    def __init__(self, binary_str: str):
        self.binary_str = binary_str
        self.current_index = 0

    def output_next_n_bits_as_int(self, n: int) -> int:
        value = self.binary_str[self.current_index:self.current_index + n]
        self.current_index += n
        return int(value, 2)

    def output_next_n_bits_as_str(self, n: int) -> str:
        value = self.binary_str[self.current_index:self.current_index + n]
        self.current_index += n
        return value

class Packet():
    def __init__(self, binary_str: str):
        # Variables:
        #   version_no (int)
        #   packet_type_id (int)
        #   literal_value (int) --- For use by Type 4's
        #   packets (Packet[]) --- For use by Type's other than 4
        #   binary_str_remaining (str)

        self.packets = []
        turning_tape = TurningTape(binary_str)

        self.version_no = turning_tape.output_next_n_bits_as_int(3)
        self.packet_type_id = turning_tape.output_next_n_bits_as_int(3)

        if (self.packet_type_id == 4):
            # Literal value type
            number_in_binary = ''
            
            while(True):
                current_section = turning_tape.output_next_n_bits_as_str(5)
                leading_bit = current_section[0]
                number_in_binary += current_section[1:]

                if leading_bit == '0':
                    break
            
            self.literal_value = int(number_in_binary, 2)
            if turning_tape.current_index == len(binary_str):
                self.binary_str_remaining = ''
            else:
                self.binary_str_remaining = binary_str[turning_tape.current_index:]

        else:
            # Operator type
            length_type_id = turning_tape.output_next_n_bits_as_str(1)

            if length_type_id == '0':
                # Next 15 bits represents packet length
                length_of_packet = turning_tape.output_next_n_bits_as_int(15)
                packet_bits = turning_tape.output_next_n_bits_as_str(length_of_packet)
                next_binary_str = packet_bits

                while(True):
                    packet = Packet(next_binary_str)
                    self.packets.append(packet)
                    next_binary_str = packet.binary_str_remaining

                    if len(next_binary_str) == 0 or len(next_binary_str.replace('0','')) == 0:
                        break

                if turning_tape.current_index == len(binary_str):
                    self.binary_str_remaining = ''
                else:
                    self.binary_str_remaining = binary_str[turning_tape.current_index:]

            else:
                # Next 11 bits represents packet quantity
                packet_quantity = turning_tape.output_next_n_bits_as_int(11)
                next_binary_str = binary_str[turning_tape.current_index:]

                for index in range(packet_quantity):
                    packet = Packet(next_binary_str)
                    self.packets.append(packet)
                    next_binary_str = packet.binary_str_remaining

                    if len(next_binary_str) == 0 or len(next_binary_str.replace('0','')) == 0:
                        break

                self.binary_str_remaining = next_binary_str


    def get_version_num_sum(self) -> int:
        if self.packet_type_id == 4:
            return self.version_no
        else:
            version_num_sum = self.version_no
            for packet in self.packets:
                version_num_sum += packet.get_version_num_sum()
            return version_num_sum

    def get_value(self) -> int:
        list_of_packet_values = [packet.get_value() for packet in self.packets]
        if(self.packet_type_id == 0):
            return sum(list_of_packet_values)
        elif(self.packet_type_id == 1):
            return prod(list_of_packet_values)
        elif(self.packet_type_id == 2):
            return min(list_of_packet_values)
        elif(self.packet_type_id == 3):
            return max(list_of_packet_values)
        elif(self.packet_type_id == 4):
            return self.literal_value
        elif(self.packet_type_id == 5):
            return int(self.packets[0].get_value() > self.packets[1].get_value())
        elif(self.packet_type_id == 6):
            return int(self.packets[0].get_value() < self.packets[1].get_value())
        elif(self.packet_type_id == 7):
            return int(self.packets[0].get_value() == self.packets[1].get_value())
        else:
            raise Exception("Shouldn't get here")

def get_answer(input: str, is_part_1: bool) -> int:
    input_as_int = int(input, 16)
    binary_str = '{0:b}'.format(input_as_int).zfill(len(input) * 4)

    main_packet = Packet(binary_str)

    if is_part_1:
        return main_packet.get_version_num_sum()
    return main_packet.get_value()


#~~~~~~~ Part 1 ~~~~~~~#
answer = get_answer(input_line,is_part_1=True)
print(f'Part 1 answer: {answer}')

#~~~~~~~ Part 2 ~~~~~~~#
answer = get_answer(input_line,is_part_1=False)
print(f'Part 2 answer: {answer}')
