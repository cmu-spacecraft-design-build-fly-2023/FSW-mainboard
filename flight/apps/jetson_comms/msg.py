"""
`message`
====================================================

Library for interfacing with the Jetson through UART. Also gives access
to the GPIO pins for signaling
--------------------

* Author(s): Sachit Goyal, Harry Rosmann
"""

from struct import pack, unpack

from micropython import const

MAX_PACKETS = const(0xFFFF)  # 65535 packets

# Packet types
PKT_TYPE_HEADER = const(0x00)
PKT_TYPE_DATA = const(0x01)
PKT_TYPE_ACK = const(0x02)
PKT_TYPE_RESET = const(0x04)

# Packet sizes
PACKET_SIZE = const(64)
PKT_METADATA_SIZE = const(4)
PAYLOAD_PER_PACKET = PACKET_SIZE - PKT_METADATA_SIZE
HEADER_PAYLOAD_SIZE = const(4)
HEADER_PKT_SIZE = HEADER_PAYLOAD_SIZE + PKT_METADATA_SIZE

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

        if self.data_len % PAYLOAD_PER_PACKET != 0:
            self.data += bytearray(
                PAYLOAD_PER_PACKET - (self.data_len % PAYLOAD_PER_PACKET)
            )

        self.data_len = len(self.data)
        self.num_packets = self.data_len // PAYLOAD_PER_PACKET

        if self.message_type > 0xFF or self.message_type < 0x00:
            raise ValueError("Message type out of range")

        if self.num_packets > MAX_PACKETS:
            raise ValueError("Data too large to send")

        self.packets = [
            self.data[i * PAYLOAD_PER_PACKET : (i + 1) * PAYLOAD_PER_PACKET]
            for i in range(self.num_packets)
        ]

    def create_header(self) -> bytearray:
        """create_header: creates the header packet for the entire message

        Returns:
            bytearray: the header packet for the message
        """
        data = pack(
            "@HBBBH",
            0,
            PKT_TYPE_HEADER,
            HEADER_PAYLOAD_SIZE,
            self.message_type,
            self.num_packets,
        )
        return data

    def create_packet(self, packet_seq: int) -> bytearray:
        """create_packet: creates a data packet for the message

        Args:
            packet_seq (int): the sequence number of the packet to create

        Returns:
            bytearray: the data packet for the message
        """

        if packet_seq > self.num_packets or packet_seq <= 0:
            raise ValueError("Data Packet number out of range")

        if packet_seq == self.num_packets:
            packet_payload_size = self.data_len % PAYLOAD_PER_PACKET
            if packet_payload_size == 0:
                packet_payload_size = PAYLOAD_PER_PACKET
        else:
            packet_payload_size = PAYLOAD_PER_PACKET

        metadata = pack("@HBB", packet_seq, PKT_TYPE_DATA, packet_payload_size)
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
        return pack("@HBB", packet_seq, PKT_TYPE_ACK, 0x00)

    @staticmethod
    def create_reset() -> bytearray:
        """create_reset: creates a reset packet to reset the sequence number

        Returns:
            bytearray: the reset packet
        """
        return pack("@HBB", 0x00, PKT_TYPE_RESET, 0x00)

    @staticmethod
    def parse_packet_meta(metadata: bytearray) -> tuple[int, int, int]:
        """parse_packet_meta: parses the metadata of a packet

        Args:
            metadata (bytearray): the metadata of the packet

        Returns:
            tuple[int, int, int]: the sequence number, packet type, and payload size
        """
        try:
            # Ensure that metadata is at least 4 bytes
            if len(metadata) < PKT_METADATA_SIZE:
                raise ValueError("Invalid packet format")

            # Grab first 4 bytes of metadata
            data = metadata[:PKT_METADATA_SIZE]

            seq_num, packet_type, payload_size = unpack("@HBB", data)
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
        # print("Header payload: ", header_payload)
        message_type, num_packets = unpack("@BH", header_payload)
        return message_type, num_packets
