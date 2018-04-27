import socket


def get_ip():
    """
    Get the IP by connecting to the internet and watching which interface is being used
    :return: Local IP address of the main network interface
    """

    return socket.gethostbyname(socket.gethostname())
