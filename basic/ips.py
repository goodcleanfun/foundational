import socket

ip_address = None
try:
    from ipaddress import IPv4Address as ip_address
except ImportError:
    try:
        from ipaddr import IPAddress as ip_address
    except ImportError:
        pass


def current_host():
    return socket.gethostname()


def get_ip_for_host(host, ip_type=ip_address):
    return ip_type(socket.gethostbyname(host))


def current_ip_address(as_type=str):
    return get_ip_for_host(current_host(), ip_type=as_type)


def get_user_ip(request):
    remote_addr = request.remote_addr

    if "X-Original-Forwarded-For" in request.headers:
        remote_addr = request.headers.getlist("X-Original-Forwarded-For")[0].rpartition(
            " "
        )[-1]
    elif "X-Forwarded-For" in request.headers:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(" ")[-1]

    if remote_addr:
        return ip_address(remote_addr)
    return remote_addr


def cidr_block_to_ipv4_range(network):
    addr, cidr = network.split("/")
    # Split address into octets and turn CIDR into int
    addr = addr.split(".")
    cidr = int(cidr)

    # Initialize the netmask and calculate based on CIDR mask
    mask = [0, 0, 0, 0]
    for i in range(cidr):
        mask[i // 8] = mask[i // 8] + (1 << (7 - i % 8))

    # Initialize net and binary and netmask with addr to get network
    net = []
    for i in range(4):
        net.append(int(addr[i]) & mask[i])

    broad = list(net)
    brange = 32 - cidr
    for i in range(brange):
        broad[3 - i // 8] = broad[3 - i // 8] + (1 << (i % 8))

    network_start = net[0] * 2**24 + net[1] * 2**16 + net[2] * 2**8 + net[3]
    network_end = broad[0] * 2**24 + broad[1] * 2**16 + broad[2] * 2**8 + broad[3]

    return (network_start, network_end)
