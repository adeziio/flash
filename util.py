import datetime
import os
import platform
import psutil
import GPUtil


def checkAuth(key):
    if (key == os.getenv('FREEFLASH_API_KEY')):
        return True
    return False


def convert_bytes(bytes_number):
    tags = ["Byte", "KB", "MB", "GB", "TB"]

    i = 0
    double_bytes = bytes_number

    while (i < len(tags) and bytes_number >= 1024):
        double_bytes = bytes_number / 1024.0
        i = i + 1
        bytes_number = bytes_number / 1024

    return str(round(double_bytes, 2)) + " " + tags[i]


def getSystemInfo():
    # System information
    output = "System Information" + "\n"
    uname = platform.uname()
    output += f"System: {uname.system}" + "\n"
    output += f"Node Name: {uname.node}" + "\n"
    output += f"Release: {uname.release}" + "\n"
    output += f"Version: {uname.version}" + "\n"
    output += f"Machine: {uname.machine}" + "\n"
    output += f"Processor: {uname.processor}" + "\n"
    output += "\n"
    return output


def getBootTime():
    # Boot time information
    output = "Boot Time" + "\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    output += f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}" + "\n"
    output += "\n"
    return output


def getCpuInfo():
    # CPU information
    output = "CPU Info" + "\n"
    # number of cores
    output += "Physical cores:" + str(psutil.cpu_count(logical=False)) + "\n"
    output += "Total cores:" + str(psutil.cpu_count(logical=True)) + "\n"
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    output += f"Max Frequency: {cpufreq.max:.2f}Mhz" + "\n"
    output += f"Min Frequency: {cpufreq.min:.2f}Mhz" + "\n"
    output += f"Current Frequency: {cpufreq.current:.2f}Mhz" + "\n"
    # CPU usage
    output += "CPU Usage Per Core:" + "\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        output += f"Core {i}: {percentage}%" + "\n"
    output += f"Total CPU Usage: {psutil.cpu_percent()}%" + "\n"
    output += "\n"
    return output


def getMemoryInfo():
    # Memory Information
    output = "Memory Information" + "\n"
    # get the memory details
    svmem = psutil.virtual_memory()
    output += f"Total: {convert_bytes(svmem.total)}" + "\n"
    output += f"Available: {convert_bytes(svmem.available)}" + "\n"
    output += f"Used: {convert_bytes(svmem.used)}" + "\n"
    output += f"Percentage: {svmem.percent}%" + "\n"
    output += "\n"
    return output


def getDiskInfo():
    # Disk Information
    output = "Disk Information" + "\n"
    output += "Partitions and Usage:" + "\n"

    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        output += f"=== Device: {partition.device} ===" + "\n"
        output += f"  Mountpoint: {partition.mountpoint}" + "\n"
        output += f"  File system type: {partition.fstype}" + "\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        output += f"  Total Size: {convert_bytes(partition_usage.total)}" + "\n"
        output += f"  Used: {convert_bytes(partition_usage.used)}" + "\n"
        output += f"  Free: {convert_bytes(partition_usage.free)}" + "\n"
        output += f"  Percentage: {partition_usage.percent}%" + "\n"
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    if (disk_io):
        output += f"Total read: {convert_bytes(disk_io.read_bytes)}" + "\n"
        output += f"Total write: {convert_bytes(disk_io.write_bytes)}" + "\n"
    output += "\n"
    return output


def getNetworkInfo():
    # Network information
    output = "Network Information" + "\n"
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            output += f"=== Interface: {interface_name} ===" + "\n"
            if str(address.family) == 'AddressFamily.AF_INET':
                output += f"  IP Address: {address.address}" + "\n"
                output += f"  Netmask: {address.netmask}" + "\n"
                output += f"  Broadcast IP: {address.broadcast}" + "\n"
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                output += f"  MAC Address: {address.address}" + "\n"
                output += f"  Netmask: {address.netmask}" + "\n"
                output += f"  Broadcast MAC: {address.broadcast}" + "\n"
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    output += f"Total Bytes Sent: {convert_bytes(net_io.bytes_sent)}" + "\n"
    output += f"Total Bytes Received: {convert_bytes(net_io.bytes_recv)}" + "\n"
    output += "\n"
    return output


def getGpuInfo():
    # GPU information
    output = "GPU Information" + "\n"
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        output += f"id: {gpu.id}" + "\n"
        output += f"name: {gpu.name}" + "\n"
        output += f"load: {gpu.load*100}%" + "\n"
        output += f"free memory: {convert_bytes(gpu.memoryFree*1000000)}" + "\n"
        output += f"used memory: {convert_bytes(gpu.memoryUsed*1000000)}" + "\n"
        output += f"total memory: {convert_bytes(gpu.memoryTotal*1000000)}" + "\n"
        output += f"temperature: {gpu.temperature} °C" + "\n"
        output += f"uuid: {gpu.uuid}" + "\n"
    output += "\n"
    return output
