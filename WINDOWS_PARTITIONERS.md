# Windows-Compatible Partitioners

This document lists all partitioners available in ExecuTorch that are compatible with Windows.

## Backend-Specific Partitioners

### 1. XNNPACK Partitioners
- **Location**: `backends/xnnpack/partition/xnnpack_partitioner.py`
- **Classes**:
  - `XnnpackPartitioner` - Main XNNPACK partitioner
  - `XnnpackDynamicallyQuantizedPartitioner` - For dynamically quantized models
  - `XnnpackFloatingPointPartitioner` - For FP32 models
  - `XnnpackQuantizedPartitioner` - For statically quantized models
- **Windows Support**: ✅ Yes (documented in `docs/source/desktop-backends.md`)
- **Description**: CPU acceleration backend, supports x86 and x86-64 architectures on Windows

### 2. OpenVINO Partitioner
- **Location**: `backends/openvino/partitioner.py`
- **Class**: `OpenvinoPartitioner`
- **Windows Support**: ✅ Yes (documented in `docs/source/desktop-backends.md`)
- **Description**: Intel hardware optimization backend for Windows

### 3. CUDA Partitioner
- **Location**: `backends/cuda/cuda_partitioner.py`
- **Class**: `CudaPartitioner`
- **Windows Support**: ✅ Yes (explicitly supports Windows in `backends/cuda/cuda_backend.py`)
- **Description**: CUDA GPU acceleration backend (experimental)

### 4. Vulkan Partitioner
- **Location**: `backends/vulkan/partitioner/vulkan_partitioner.py`
- **Class**: `VulkanPartitioner`
- **Windows Support**: ✅ Yes (Windows build configuration in `backends/vulkan/targets.bzl`)
- **Description**: Vulkan GPU acceleration backend

### 5. AOTI Partitioner (Base)
- **Location**: `backends/aoti/aoti_partitioner.py`
- **Class**: `AotiPartitioner`
- **Windows Support**: ✅ Yes (platform-agnostic base class)
- **Description**: Base partitioner for AOTInductor-driven backends (used by CUDA)

## Canonical Partitioners (Platform-Agnostic)

These partitioners are pure Python implementations and work on all platforms including Windows:

### 6. All Node Partitioner
- **Location**: `exir/backend/canonical_partitioners/all_node_partitioner.py`
- **Class**: `AllNodePartitioner`
- **Windows Support**: ✅ Yes (platform-agnostic)
- **Description**: Partitions all nodes in the graph to a specified backend

### 7. Pattern Op Partitioner
- **Location**: `exir/backend/canonical_partitioners/pattern_op_partitioner.py`
- **Functions**: `generate_partitions_from_list_of_nodes`, `generate_grouped_partitions_from_list_of_nodes`
- **Windows Support**: ✅ Yes (platform-agnostic)
- **Description**: Utility functions for pattern-based partitioning

### 8. Configuration-Based Partitioner
- **Location**: `exir/backend/canonical_partitioners/config_partitioner.py`
- **Classes**:
  - `PartitionerConfig` (abstract base)
  - `ConfigerationBasedPartitioner`
- **Windows Support**: ✅ Yes (platform-agnostic)
- **Description**: Base classes for configuration-driven partitioning (used by XNNPACK)

### 9. Group-Based Partitioner
- **Location**: `exir/backend/canonical_partitioners/group_partitioner.py`
- **Class**: `GroupBasedPartitioner`
- **Windows Support**: ✅ Yes (platform-agnostic)
- **Description**: Partitioner that allows explicit grouping of nodes

## Example/Demo Partitioners

### 10. Example Partitioner
- **Location**: `backends/example/example_partitioner.py`
- **Class**: `ExamplePartitioner`
- **Windows Support**: ✅ Yes (platform-agnostic)
- **Description**: Example partitioner for add/mul operations

## Platform-Specific Partitioners (NOT Windows-Compatible)

The following partitioners are NOT compatible with Windows:

- **Apple Backends**: `MetalPartitioner`, `MPSPartitioner`, `CoreMLPartitioner` (macOS/iOS only)
- **ARM Backends**: `TOSAPartitioner`, `VgfPartitioner`, `EthosUPartitioner` (ARM-specific)
- **Qualcomm**: `QnnPartitioner` (Qualcomm hardware only)
- **Samsung**: `EnnPartitioner` (Samsung hardware only)
- **NXP**: `NeutronPartitioner` (NXP hardware only)
- **MediaTek**: `NeuropilotPartitioner` (MediaTek hardware only)

## Summary

**Total Windows-Compatible Partitioners: 10+**

The main production-ready partitioners for Windows are:
1. **XNNPACK** (CPU acceleration) - Recommended for general use
2. **OpenVINO** (Intel hardware optimization) - Recommended for Intel CPUs
3. **CUDA** (GPU acceleration) - For NVIDIA GPUs (experimental)
4. **Vulkan** (GPU acceleration) - For Vulkan-compatible GPUs

All canonical partitioners and the example partitioner are also available on Windows as they are platform-agnostic Python implementations.
