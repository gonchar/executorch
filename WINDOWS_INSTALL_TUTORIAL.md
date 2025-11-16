# ExecuTorch Windows Installation Tutorial

Complete step-by-step guide to compile and install ExecuTorch into a local Python virtual environment on Windows.

## Prerequisites

Before starting, ensure you have the following installed:

### 1. Python 3.10, 3.11, or 3.12
- Download from [python.org](https://www.python.org/downloads/)
- **Important**: During installation, check "Add Python to PATH"
- Verify installation:
  ```cmd
  python --version
  ```
  Should show Python 3.10.x, 3.11.x, or 3.12.x

### 2. Visual Studio 2022 or later
- Download [Visual Studio 2022 Community](https://visualstudio.microsoft.com/downloads/) (free)
- During installation, select:
  - **Desktop development with C++** workload
  - **Clang tools for Windows** component (required for ClangCL)
- Verify installation by opening "Developer Command Prompt for VS 2022"

### 3. CMake 3.29 or later (but < 4.0.0)
- Download from [cmake.org](https://cmake.org/download/)
- During installation, select "Add CMake to system PATH"
- Verify installation:
  ```cmd
  cmake --version
  ```
  Should show version 3.29.x or higher (but less than 4.0.0)

### 4. Git with Symlink Support
- Download from [git-scm.com](https://git-scm.com/download/win)
- **Critical**: Enable Developer Mode in Windows Settings:
  1. Open Windows Settings (Win + I)
  2. Go to **Privacy & Security** → **For developers**
  3. Enable **Developer Mode**
- Configure Git to use symlinks:
  ```cmd
  git config --global core.symlinks true
  ```
- **Important**: If you already cloned the repository, you must re-clone it after enabling symlinks:
  ```cmd
  git clone <repository-url>
  ```

## Step-by-Step Installation

### Step 1: Open Developer Command Prompt

**IMPORTANT**: You must use Visual Studio Developer Command Prompt or Developer PowerShell. Regular Command Prompt or PowerShell will not work.

- Open **Start Menu**
- Search for "Developer Command Prompt for VS 2022" or "Developer PowerShell for VS 2022"
- Right-click and select "Run as Administrator" (recommended)

### Step 2: Navigate to Project Directory

```cmd
cd /d C:\path\to\executorch
```

Replace `C:\path\to\executorch` with your actual ExecuTorch repository path.

### Step 3: Create and Activate Virtual Environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` prefix in your command prompt, indicating the virtual environment is active.

### Step 4: Upgrade pip and Install Build Tools

```cmd
python -m pip install --upgrade pip
python -m pip install wheel setuptools
```

### Step 5: Verify Git Symlink Configuration

```cmd
git config --get core.symlinks
```

This should output `true`. If it shows `false` or nothing, run:
```cmd
git config --global core.symlinks true
```
Then re-clone the repository if needed.

### Step 6: Install ExecuTorch

You have two options:

#### Option A: Standard Installation (Recommended)

This installs ExecuTorch normally into your virtual environment:

```cmd
python install_executorch.py
```

This script will:
1. Check and update Git submodules
2. Install all required dependencies (including PyTorch nightly)
3. Build the C++ extensions using CMake
4. Install ExecuTorch into your virtual environment

#### Option B: Editable Installation (For Development)

If you plan to modify the Python code and want changes to be picked up immediately:

```cmd
python install_executorch.py --editable
```

#### Option C: Minimal Installation (Core Only)

If you only need core ExecuTorch without example dependencies:

```cmd
python install_executorch.py --minimal
```

### Step 7: Wait for Build to Complete

The installation process will:
- Download and install PyTorch nightly (CPU-only on Windows)
- Install all Python dependencies
- Configure CMake with the "pybind" preset
- Compile C++ extensions (this may take 10-30 minutes depending on your system)
- Install the package

**Note**: The first build can take 20-30 minutes. Subsequent builds will be faster due to caching.

### Step 8: Verify Installation

Test that ExecuTorch is installed correctly:

```cmd
python -c "import executorch; print(executorch.__version__)"
```

You should see the version number printed.

Test a basic import:

```cmd
python -c "from executorch.exir import to_edge_transform_and_lower; print('Import successful!')"
```

## Troubleshooting

### Error: "CL.exe not found" or "cl: command not found"

**Solution**: You must use Visual Studio Developer Command Prompt. Regular Command Prompt doesn't have the necessary environment variables.

### Error: "Git symlink support required"

**Solution**: 
1. Enable Developer Mode in Windows Settings
2. Run: `git config --global core.symlinks true`
3. Re-clone the repository

### Error: "CMake version too old" or "CMake version 4.0.0+"

**Solution**: Install CMake 3.29.x (but not 4.0.0 or higher). The project requires `cmake>=3.29,<4.0.0`.

### Error: "Python version not compatible"

**Solution**: ExecuTorch requires Python 3.10, 3.11, or 3.12. Python 3.13 is not supported yet.

### Build Fails with ClangCL Errors

**Solution**: Ensure you have "Clang tools for Windows" installed in Visual Studio. Re-run Visual Studio Installer and add this component.

### Out of Memory During Build

**Solution**: Reduce parallelism by setting:
```cmd
set CMAKE_BUILD_PARALLEL_LEVEL=2
python install_executorch.py
```

### Want to Clean Build Artifacts

To remove all build artifacts and start fresh:

```cmd
python install_executorch.py --clean
```

## Using ExecuTorch

After installation, you can use ExecuTorch in your Python scripts:

```python
import torch
from executorch.exir import to_edge_transform_and_lower
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner

model = MyModel().eval()
example_inputs = (torch.randn(1, 3, 224, 224),)
exported_program = torch.export.export(model, example_inputs)

program = to_edge_transform_and_lower(
    exported_program,
    partitioner=[XnnpackPartitioner()]
).to_executorch()

with open("model.pte", "wb") as f:
    f.write(program.buffer)
```

## Additional Notes

- **Windows uses CPU-only PyTorch**: CUDA support is not available on Windows builds yet
- **Build Time**: First build takes 20-30 minutes. Subsequent builds are faster
- **Disk Space**: Ensure you have at least 5-10 GB free space for the build
- **Virtual Environment**: Always activate `.venv` before using ExecuTorch:
  ```cmd
  .venv\Scripts\activate
  ```

## Next Steps

- Read the [Getting Started Guide](https://docs.pytorch.org/executorch/main/getting-started.html)
- Try the [Quick Start Examples](https://docs.pytorch.org/executorch/main/quick-start-section.html)
- Explore the [Examples Directory](examples/) in the repository

## Getting Help

- [GitHub Issues](https://github.com/pytorch/executorch/issues)
- [Discord Community](https://discord.gg/Dh43CKSAdc)
- [Documentation](https://docs.pytorch.org/executorch/main/index.html)
