import psutil
import platform
import socket
import uuid
import colorama
import os
from datetime import datetime
import GPUtil
import sys

colorama.init()
clear_command = "cls" if os.name == "nt" else "clear"

def clear_screen():
    os.system(clear_command)

def get_system_info():
    return {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

def get_cpu_info():
    return {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f}Mhz",
        "Min Frequency": f"{psutil.cpu_freq().min:.2f}Mhz",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f}Mhz",
        "CPU Usage Per Core": [f"{x}%" for x in psutil.cpu_percent(percpu=True, interval=1)],
        "Total CPU Usage": f"{psutil.cpu_percent()}%"
    }

def get_memory_info():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    return {
        "Total Memory": f"{get_size(svmem.total)}",
        "Available Memory": f"{get_size(svmem.available)}",
        "Used Memory": f"{get_size(svmem.used)}",
        "Percentage": f"{svmem.percent}%",
        "Total Swap": f"{get_size(swap.total)}",
        "Free Swap": f"{get_size(swap.free)}",
        "Used Swap": f"{get_size(swap.used)}",
        "Percentage Swap": f"{swap.percent}%"
    }

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_info = {}
    for partition in partitions:
        partition_info = {}
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        partition_info['Mountpoint'] = partition.mountpoint
        partition_info['File System Type'] = partition.fstype
        partition_info['Total Size'] = get_size(partition_usage.total)
        partition_info['Used'] = get_size(partition_usage.used)
        partition_info['Free'] = get_size(partition_usage.free)
        partition_info['Percentage'] = f"{partition_usage.percent}%"
        disk_info[partition.device] = partition_info
    return disk_info

def get_network_info():
    if_addrs = psutil.net_if_addrs()
    net_io = psutil.net_io_counters()
    network_info = {}
    for interface_name, interface_addresses in if_addrs.items():
        addresses = []
        for address in interface_addresses:
            address_info = {}
            if str(address.family) == 'AddressFamily.AF_INET':
                address_info["IP Address"] = address.address
                address_info["Netmask"] = address.netmask
                address_info["Broadcast IP"] = address.broadcast
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                address_info["MAC Address"] = address.address
                address_info["Netmask"] = address.netmask
                address_info["Broadcast MAC"] = address.broadcast
            addresses.append(address_info)
        network_info[interface_name] = addresses
    network_info["Total Bytes Sent"] = f"{get_size(net_io.bytes_sent)}"
    network_info["Total Bytes Received"] = f"{get_size(net_io.bytes_recv)}"
    return network_info

def get_bios_info():
    bios_info = {}
    try:
        if platform.system() == "Windows":
            import wmi
            w = wmi.WMI()
            bios = w.Win32_BIOS()[0]
            bios_info["Manufacturer"] = bios.Manufacturer
            bios_info["Version"] = bios.Version
            bios_info["Release Date"] = bios.ReleaseDate
        else:
            bios_info["Error"] = "BIOS information is only available on Windows."
    except Exception as e:
        bios_info["Error"] = str(e)
    return bios_info

def get_network_connections():
    connections = psutil.net_connections()
    connection_info = []
    for conn in connections:
        conn_info = {}
        conn_info["FD"] = conn.fd
        conn_info["Family"] = conn.family.name
        conn_info["Type"] = conn.type.name
        conn_info["Local Address"] = f"{conn.laddr.ip}:{conn.laddr.port}"
        if conn.raddr:
            conn_info["Remote Address"] = f"{conn.raddr.ip}:{conn.raddr.port}"
        else:
            conn_info["Remote Address"] = "None"
        conn_info["Status"] = conn.status
        connection_info.append(conn_info)
    return {"Connections": connection_info}

def get_installed_programs():
    programs = {}
    try:
        if platform.system() == "Windows":
            import winreg as reg
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(reg.QueryInfoKey(reg_key)[0]):
                sub_key_name = reg.EnumKey(reg_key, i)
                sub_key = reg.OpenKey(reg_key, sub_key_name)
                try:
                    display_name = reg.QueryValueEx(sub_key, "DisplayName")[0]
                    display_version = reg.QueryValueEx(sub_key, "DisplayVersion")[0]
                    programs[display_name] = display_version
                except FileNotFoundError:
                    pass
                reg.CloseKey(sub_key)
            reg.CloseKey(reg_key)
        else:
            programs["Error"] = "Installed programs information is only available on Windows."
    except Exception as e:
        programs["Error"] = str(e)
    return programs

def get_gpu_info():
    gpus = GPUtil.getGPUs()
    gpu_info = []
    for gpu in gpus:
        gpu_info.append({
            "GPU Name": gpu.name,
            "GPU Load": f"{gpu.load * 100}%",
            "GPU Free Memory": f"{gpu.memoryFree}MB",
            "GPU Used Memory": f"{gpu.memoryUsed}MB",
            "GPU Total Memory": f"{gpu.memoryTotal}MB",
            "GPU Temperature": f"{gpu.temperature} °C"
        })
    return {"GPUs": gpu_info}

def get_boot_time():
    boot_time_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    return {"Boot Time": boot_time}

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def print_info(title, info):
    print(colorama.Fore.GREEN + f"[System Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + f"{title}")
    print("")
    for key, value in info.items():
        if isinstance(value, dict):
            print(colorama.Fore.YELLOW + f"{key}:")
            for sub_key, sub_value in value.items():
                print(colorama.Fore.LIGHTWHITE_EX + f"  {sub_key}: {sub_value}")
        elif isinstance(value, list):
            print(colorama.Fore.YELLOW + f"{key}:")
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        print(colorama.Fore.LIGHTWHITE_EX + f"  {sub_key}: {sub_value}")
                else:
                    print(colorama.Fore.LIGHTWHITE_EX + f"  {item}")
        else:
            print(colorama.Fore.YELLOW + f"{key}: " + colorama.Fore.LIGHTWHITE_EX + f"{value}")
    print("")

def main():
    while True:
        clear_screen()
        print(colorama.Fore.GREEN + "[System Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Choose an option to display system information (type 'exit' to quit):")
        print("")
        print(colorama.Fore.YELLOW + "1 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "System Information")
        print(colorama.Fore.YELLOW + "2 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "CPU Information")
        print(colorama.Fore.YELLOW + "3 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "Memory Information")
        print(colorama.Fore.YELLOW + "4 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "Disk Information")
        print(colorama.Fore.YELLOW + "5 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "Network Information")
        print(colorama.Fore.YELLOW + "6 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "BIOS Information")
        print(colorama.Fore.YELLOW + "7 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "Network Connections")
        print(colorama.Fore.YELLOW + "8 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "Installed Programs")
        print(colorama.Fore.YELLOW + "9 " + colorama.Fore.LIGHTYELLOW_EX + " = " + colorama.Fore.WHITE + "GPU Information")
        print(colorama.Fore.YELLOW + "10 " + colorama.Fore.LIGHTYELLOW_EX + "= " + colorama.Fore.WHITE + "System Boot Time")
        print("")

        choice = input(colorama.Fore.MAGENTA + "root@you:~$ " + colorama.Fore.WHITE).strip()

        if choice == '1':
            info = get_system_info()
            print_info("System Information", info)
        elif choice == '2':
            info = get_cpu_info()
            print_info("CPU Information", info)
        elif choice == '3':
            info = get_memory_info()
            print_info("Memory Information", info)
        elif choice == '4':
            info = get_disk_info()
            print_info("Disk Information", info)
        elif choice == '5':
            info = get_network_info()
            print_info("Network Information", info)
        elif choice == '6':
            info = get_bios_info()
            print_info("BIOS Information", info)
        elif choice == '7':
            info = get_network_connections()
            print_info("Network Connections", info)
        elif choice == '8':
            info = get_installed_programs()
            print_info("Installed Programs", info)
        elif choice == '9':
            info = get_gpu_info()
            print_info("GPU Information", info)
        elif choice == '10':
            info = get_boot_time()
            print_info("Boot Time", info)
        elif choice.lower() == 'exit':
            break
        else:
            print(colorama.Fore.RED + "Invalid choice, please try again.")
        
        input(colorama.Fore.GREEN + "[System Scanner]: " + colorama.Fore.LIGHTYELLOW_EX + "Press Enter to continue...")

if __name__ == "__main__":
    main()
