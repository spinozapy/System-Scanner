# System Scanner

A comprehensive Python tool for gathering detailed system information and diagnostics.

## Requirements

- Python 3.x
- `psutil` library (Install using `pip install psutil`)
- `platform` library (Included with Python)
- `socket` library (Included with Python)
- `uuid` library (Included with Python)
- `colorama` library (Install using `pip install colorama`)
- `GPUtil` library (Install using `pip install GPUtil`)

To install the required libraries, you can use the `requirements.txt` file. Create a `requirements.txt` file with the following content:

```
psutil
colorama
GPUtil
```

Then, run the following command to install all the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository.
2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:

    ```bash
    python main.py
    ```

4. Choose an option from the menu to display various system information or type 'exit' to quit.

## Options

- **1** = System Information
  - Displays basic system details such as OS, Node Name, Release, Version, Machine, and Processor.
  
- **2** = CPU Information
  - Shows CPU details including physical cores, total cores, max/min/current frequency, and CPU usage.

- **3** = Memory Information
  - Provides information about total, available, and used memory, along with swap memory details.

- **4** = Disk Information
  - Lists disk partitions with information about mount points, file system types, and space usage.

- **5** = Network Information
  - Fetches network interface details, including IP addresses, MAC addresses, and network usage statistics.

- **6** = BIOS Information
  - Displays BIOS manufacturer, version, and release date (only available on Windows).

- **7** = Network Connections
  - Shows details of current network connections, including local and remote addresses, and connection status.

- **8** = Installed Programs
  - Lists installed programs on the system (only available on Windows).

- **9** = GPU Information
  - Provides details about available GPUs, including load, memory usage, and temperature.

- **10** = System Boot Time
  - Displays the system's boot time.

## Usage Caution

- For educational or testing purposes only.
- Do not use for malicious activities.
- Follow ethical standards while using this tool.
