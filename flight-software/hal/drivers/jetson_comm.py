# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`jetson_comm`
====================================================

Library for interfacing with the Jetson through UART. Also gives access
to the GPIO pins for signaling
--------------------

* Author(s): Sachit Goyal, Harry Rosmann
"""
from diagnostics.diagnostics import Diagnostics
from micropython import const
import board, Pin
import digitalio
from struct import pack, unpack 

MAX_PACKETS             = const(0xFFFF) # 65535 packets

# Packet types
PKT_TYPE_HEADER         = const(0x00) 
PKT_TYPE_DATA           = const(0x01)
PKT_TYPE_ACK            = const(0x02)
PKT_TYPE_NACK           = const(0x03)
PKT_TYPE_RESET          = const(0x04)

# Packet sizes
PACKET_SIZE             = const(256)
PKT_METADATA_SIZE       = const(4)
HEADER_PAYLOAD_SIZE     = const(4)
PAYLOAD_PER_PACKET      = PACKET_SIZE - PKT_METADATA_SIZE # 252 bytes
HEADER_PADDING_SIZE     = PAYLOAD_PER_PACKET - HEADER_PAYLOAD_SIZE # 248 bytes
ACK_PADDING_SIZE        = PAYLOAD_PER_PACKET

"""
Header Packet
+-----------------+-----------------+-----------------+-----------------+-----------------+---------------+
|  Header Seq     |  Packet Type    | Payload Size    |  Message Type   |  Num Packets    |    Padding    |
|  (2 bytes)      |  (1 byte)       |  (1 byte)       |  (1 byte)       |  (2 bytes)      |  (248 bytes)  |
+-----------------+-----------------+-----------------+-----------------+-----------------+---------------+

Data Packet (Including Ack)
+-----------------+-----------------+-----------------+---------------+
|  Packet Seq     |  Packet Type    | Payload Size    |     Data      |
|  (2 bytes)      |  (1 byte)       |  (1 byte)       |  (252 bytes)  |
+-----------------+-----------------+-----------------+---------------+
"""

class Message:
    """
    Message class to handle the creation of packets and headers
    """
    def __init__(self, message_type: int, data: bytearray):
        self.message_type = message_type
        self.data = data
        self.data_len = len(data)

        # Add padding
        if self.data_len % PAYLOAD_PER_PACKET != 0:
            self.data += bytearray(PAYLOAD_PER_PACKET - (self.data_len % PAYLOAD_PER_PACKET))
            self.data_len = len(self.data)
    
        self.num_packets = self.data_len // PAYLOAD_PER_PACKET

        if self.message_type > 0xFF or self.message_type < 0x00:
            raise ValueError("Message type out of range")
        if self.num_packets > MAX_PACKETS:
            raise ValueError("Data too large to send")
        
        self.packets = [self.data[i*PAYLOAD_PER_PACKET:(i+1)*PAYLOAD_PER_PACKET] 
                        for i in range(self.num_packets)]
        
    def create_header(self) -> bytearray:
        """create_header: creates the header packet for the entire message
        
        Returns:
            bytearray: the header packet for the message
        """

        header_seq = 0x00
        data = pack('@HBBBH', header_seq, PKT_TYPE_HEADER, HEADER_PAYLOAD_SIZE, 
             self.message_type, self.num_packets) + bytearray(HEADER_PADDING_SIZE)
        return data
    
    def create_packet(self, packet_seq: int) -> bytearray:
        """create_packet: creates a data packet for the message
        
        Args:
            packet_seq (int): the sequence number of the packet to create
        
        Returns:
            bytearray: the data packet for the message
        """

        if packet_seq > self.num_packets or packet_seq <= 0:
            raise ValueError("Packet number out of range")
        
        if packet_seq == self.num_packets:
            packet_payload_size = self.data_len % PAYLOAD_PER_PACKET 
            if packet_payload_size == 0:
                packet_payload_size = PAYLOAD_PER_PACKET
        else:
            packet_payload_size = PAYLOAD_PER_PACKET

        # Pack the structure of the packet
        metadata = pack('@HBB', packet_seq, PKT_TYPE_DATA, packet_payload_size)
        current_packet = self.packets[packet_seq - 1][:packet_payload_size]
        return metadata + current_packet
    
    @staticmethod
    def create_ack(packet_seq: int) -> bytearray:
        """create_ack: creates an ack packet for the given sequence number

        Args:
            packet_seq (int): the sequence number to ack
        
        Returns:
            bytearray: the ack packet
        """
        if packet_seq > MAX_PACKETS or packet_seq < 0:
            raise ValueError("Packet number out of range")
        return pack('@HBB', packet_seq, PKT_TYPE_ACK, 0x00) 

    @staticmethod
    def create_nack(packet_seq: int) -> bytearray:
        """create_nack: creates a nack packet for the given sequence number

        Args:
            packet_seq (int): the sequence number to nack

        Returns:
            bytearray: the nack packet
        """
        if packet_seq > MAX_PACKETS or packet_seq < 0:
            raise ValueError("Packet number out of range")
        return pack('@HBB', packet_seq, PKT_TYPE_NACK, 0x00) 

    @staticmethod
    def create_reset() -> bytearray:
        """create_reset: creates a reset packet to reset the sequence number
        
        Returns:
            bytearray: the reset packet
        """
        return pack('@HBB', 0x00, PKT_TYPE_RESET, 0x00) 
    
    @staticmethod
    def parse_packet_meta(metadata: bytearray) -> tuple[int, int, int]:
        """parse_packet_meta: parses the metadata of a packet
        
        Args:
            metadata (bytearray): the metadata of the packet

        Returns:
            tuple[int, int, int]: the sequence number, packet type, and payload size
        """
        try:
            seq_num, packet_type, payload_size = unpack('@HBB', metadata)
        except:
            raise ValueError("Invalid packet format")
        return seq_num, packet_type, payload_size
    
    @staticmethod                                                                                                                                    
    def parse_header_payload(header_payload: bytearray) -> tuple[int, int]:
        """parse_header_payload: parses the payload of the header

        Args:
            header_payload (bytearray): the payload of the header

        Returns:
            tuple[int, int]: the message type and the number of packets
        """
        message_type, num_packets = unpack('@BH', header_payload)
        return message_type, num_packets
    
# TODO: Add comments
class JetsonComm(Diagnostics):
    def __init__(self, uart, enable_pin: Pin = None):
        self.uart = uart

        self._enable = None
        if enable_pin is not None:
            self._enable = digitalio.DigitalInOut(enable_pin)
            self._enable.switch_to_output()
            self.enable()

        super().__init__(self._enable)
        
    def send_message(self, message):
        done = False
        current_seq = 0
        total_packets = message.num_packets
        while(not done):
            if current_seq == 0:
                self.uart.write(message.create_header())
            else:
                self.uart.write(message.create_packet(current_seq))
            while(self.uart.in_waiting < PKT_METADATA_SIZE):
                continue
            response = self.uart.read(PKT_METADATA_SIZE)
            (seq_num, packet_type, _) = Message.parse_packet_meta(response)
            if packet_type == PKT_TYPE_ACK and seq_num == current_seq:
                if current_seq == total_packets:
                    done = True
                current_seq += 1
            elif packet_type == PKT_TYPE_NACK:
                continue
            elif packet_type == PKT_TYPE_RESET:
                current_seq = 0
            else:
                current_seq = 0

    def receive_message(self):
        expected_seq_num = 0
        while(self.uart.in_waiting < PACKET_SIZE):
            continue
        header = self.uart.read(PACKET_SIZE)
        (seq_num, packet_type, payload_size) = Message.parse_packet_meta(header[:PKT_METADATA_SIZE])
        if packet_type != PKT_TYPE_HEADER:
            raise ValueError("Invalid header")
        (message_type, num_packets) = Message.parse_header_payload(header[PKT_METADATA_SIZE:]
                                                                   [:HEADER_PAYLOAD_SIZE])
        self.uart.write(Message.create_ack(seq_num))
        expected_seq_num = seq_num + 1
        message = bytearray()
        print(num_packets)
        for i in range(num_packets):
            while(self.uart.in_waiting < PACKET_SIZE):
                continue
            packet = self.uart.read(PACKET_SIZE)
            (seq_num, packet_type, payload_size) = Message.parse_packet_meta(packet[:PKT_METADATA_SIZE])
            if packet_type != PKT_TYPE_DATA or seq_num != expected_seq_num:
                raise ValueError("Incorrect seq num")
            # print(f'Received seq_num {seq_num}')
            self.uart.write(Message.create_ack(seq_num))
            # print(f'Acked seq_num {seq_num}')
            expected_seq_num += 1
            # message += packet[PKT_METADATA_SIZE:][:payload_size]
        return message
    
    def run_diagnostics(self) -> list[int] | None:
        """run_diagnostic_test: Run all tests for the component
        """
        # TODO: Implement simple comm test
        return [Diagnostics.NOERROR]
