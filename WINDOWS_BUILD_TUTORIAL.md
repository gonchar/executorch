# ExecuTorch Windows Build and Installation Tutorial

This tutorial provides step-by-step instructions for compiling and installing ExecuTorch into a local Python virtual environment on Windows.

## Prerequisites

### 1. Install Required Software

#### Python 3.10-3.12
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation:
  ```cmd
  python --version
  ```

#### Git with Symlink Support
ExecuTorch requires Git symlinks to be enabled. This is critical for the build to succeed.

1. **Enable Developer Mode** (Recommended):
   - Open Windows Settings → Update & Security → For developers
   - Enable "Developer Mode"
   - This allows Git to create symlinks without administrator privileges

2. **Configure Git for Symlinks**:
   ```cmd
   git config --global core.symlinks true
   ```

3. **Re-clone the repository** if you already have it:
   - Delete the existing repository folder
   - Clone fresh: `git clone -b viable/strict https://github.com/pytorch/executorch.git`
   - Navigate into the directory: `cd executorch`

#### Visual Studio 2022 or later with Clang-CL
- Download [Visual Studio 2022 Community](https://visualstudio.microsoft.com/downloads/) (free)
- During installation, select:
  - "Desktop development with C++" workload
  - "Clang tools for Windows" component (under Individual components)
- Verify installation:
  ```cmd
  clang-cl --version
  ```

#### CMake 3.29 or later
- Download from [cmake.org](https://cmake.org/download/)
- During installation, select "Add CMake to system PATH"
- Verify installation:
  ```cmd
  cmake --version
  ```

### 2. Verify Git Symlink Configuration

Before proceeding, verify that Git symlinks are properly configured:

```cmd
git config --get core.symlinks
```

This should output `true`. If not, run:
```cmd
git config --global core.symlinks true
```

Then re-clone the repository if needed.

## Step-by-Step Installation

### Step 1: Open Command Prompt or PowerShell

Open a new Command Prompt or PowerShell window as a regular user (not administrator).

### Step 2: Navigate to the ExecuTorch Directory

```cmd
cd path\to\executorch
```

Replace `path\to\executorch` with the actual path to your ExecuTorch repository.

### Step 3: Create and Activate Python Virtual Environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

You should see `(.venv)` in your prompt, indicating the virtual environment is active.

### Step 4: Upgrade pip and Install Build Tools

```cmd
python -m pip install --upgrade pip
python -m pip install wheel setuptools
```

### Step 5: Install ExecuTorch and Dependencies

Use the provided installation script:

```cmd
python install_executorch.py
```

This script will:
- Check and update Git submodules
- Install all required Python dependencies (including PyTorch)
- Build the C++ components using CMake
- Install ExecuTorch into your virtual environment

**Note:** The first build can take 30-60 minutes depending on your system.

### Alternative: Manual Installation Steps

If you prefer to run the steps manually or need more control:

#### 5a. Install Core Dependencies

```cmd
python install_requirements.py
```

This installs:
- PyTorch (nightly build by default)
- All Python dependencies from `requirements-dev.txt`
- Local packages from `third-party/ao`

#### 5b. Build and Install ExecuTorch Package

```cmd
pip install . --no-build-isolation -v
```

The `--no-build-isolation` flag is required because the build process needs access to the installed PyTorch package.

### Step 6: Verify Installation

Test that ExecuTorch is installed correctly:

```cmd
python -m executorch.examples.xnnpack.aot_compiler --model_name="mv2" --delegate
```

This should:
- Complete without errors
- Create a file named `mv2_xnnpack_fp32.pte` in the current directory

If successful, ExecuTorch is properly installed!

## Installation Options

### Editable Mode (for Development)

For development where you want Python code changes to be reflected immediately:

```cmd
python install_executorch.py --editable
```

Or manually:
```cmd
pip install -e . --no-build-isolation
```

**Note:** C++ changes still require a full rebuild.

### Minimal Installation

Install only core dependencies (skip example dependencies):

```cmd
python install_executorch.py --minimal
```

### Use Pinned PyTorch Version

Use the pinned PyTorch commit instead of nightly:

```cmd
python install_executorch.py --use-pt-pinned-commit
```

### Enable Additional Backends

Enable specific backends using CMake arguments:

```cmd
set CMAKE_ARGS=-DEXECUTORCH_BUILD_MPS=ON
python install_executorch.py
```

Or for multiple backends:
```cmd
set CMAKE_ARGS=-DEXECUTORCH_BUILD_MPS=ON -DEXECUTORCH_BUILD_VULKAN=ON
python install_executorch.py
```

## Troubleshooting

### Error: "version.py not found" or Symlink Issues

**Problem:** Git symlinks are not properly configured.

**Solution:**
1. Verify Developer Mode is enabled in Windows Settings
2. Run: `git config --global core.symlinks true`
3. Re-clone the repository:
   ```cmd
   cd ..
   rmdir /s executorch
   git clone -b viable/strict https://github.com/pytorch/executorch.git
   cd executorch
   ```

### Error: "clang-cl not found"

**Problem:** Clang-CL is not installed or not in PATH.

**Solution:**
1. Install Visual Studio 2022 with "Clang tools for Windows"
2. Or add Clang to PATH manually:
   ```cmd
   set PATH=%PATH%;C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\Llvm\x64\bin
   ```

### Error: "CMake not found"

**Problem:** CMake is not installed or not in PATH.

**Solution:**
1. Install CMake from [cmake.org](https://cmake.org/download/)
2. During installation, select "Add CMake to system PATH"
3. Restart your command prompt

### Error: Build Fails with CMake Errors

**Problem:** CMake configuration or build issues.

**Solution:**
1. Clean build artifacts:
   ```cmd
   python install_executorch.py --clean
   ```
2. Update submodules:
   ```cmd
   git submodule sync
   git submodule update --init --recursive
   ```
3. Try again: `python install_executorch.py`

### Error: "Python version not compatible"

**Problem:** Python version is not 3.10, 3.11, or 3.12.

**Solution:**
Install a compatible Python version (3.10-3.12) and recreate the virtual environment.

### Build Takes Too Long

**Solution:**
- The first build is always slow (30-60 minutes)
- Subsequent builds are faster due to incremental compilation
- Consider installing `ccache` for faster rebuilds (if available for Windows)

### Import Errors After Installation

**Problem:** Some modules can't be imported directly in editable mode.

**Solution:**
This is a [known issue](https://github.com/pytorch/executorch/issues/9558). Use full import paths:
```python
# This may fail in editable mode
from executorch.exir import CaptureConfig

# Use this instead
from executorch.exir.capture import CaptureConfig
```

## Cleaning Build Artifacts

To clean all build artifacts and start fresh:

```cmd
python install_executorch.py --clean
```

This removes:
- `pip-out/` directory
- `cmake-out*/` directories
- `buck-out/` directory
- Buck cached state

## Using ExecuTorch

After installation, you can use ExecuTorch in your Python scripts:

```python
import torch
from executorch.exir import to_edge_transform_and_lower
from executorch.backends.xnnpack.partition.xnnpack_partitioner import XnnpackPartitioner

# Export your PyTorch model
model = MyModel().eval()
example_inputs = (torch.randn(1, 3, 224, 224),)
exported_program = torch.export.export(model, example_inputs)

# Optimize for target hardware
program = to_edge_transform_and_lower(
    exported_program,
    partitioner=[XnnpackPartitioner()]
).to_executorch()

# Save for deployment
with open("model.pte", "wb") as f:
    f.write(program.buffer)
```

## Next Steps

- Read the [main README](README.md) for usage examples
- Check out [examples](examples/) for model-specific tutorials
- See [documentation](https://docs.pytorch.org/executorch/main/index.html) for detailed guides
- Explore [backend documentation](https://docs.pytorch.org/executorch/main/backends-overview.html) for hardware-specific optimizations

## Summary

The complete installation process:

1. ✅ Install prerequisites (Python, Git, Visual Studio, CMake)
2. ✅ Enable Git symlinks (`git config --global core.symlinks true`)
3. ✅ Create and activate virtual environment (`.venv`)
4. ✅ Run `python install_executorch.py`
5. ✅ Verify with `python -m executorch.examples.xnnpack.aot_compiler --model_name="mv2" --delegate`

That's it! ExecuTorch is now installed and ready to use.
