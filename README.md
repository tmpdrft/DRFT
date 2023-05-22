# Supplementary information
## Introduction
Data remnants analysis of document files in Windows: Microsoft 365 as a case study

# DRFT (Data Remnants Forensics Tool)

## Building - Windows
 - The Python 3.7 or above must be registered in the system environment variable
 - No additional install is necessary
 
## Git

To get the source using git run:
<pre><code>git clone https://github.com/tmpdrft/DRFT.git</code></pre>

## Install/Dependency

To run DRFT, please change Powershell Execution Policy.

Execute Powershell as administrator:
```
Set-ExecutionPolicy Unrestricted
```

And enter
```
A
```

Installing the Requirements Library to Run in PowerShell:
```
.\build.ps1
```

## Run
Open Folder:
```
cd drft
```

Activate venv(if not activated):
```
cd venv\Scripts
Activate.bat
```

Run DRFT:
```
python DRTF_core.py
```
