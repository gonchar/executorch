#!/usr/bin/env python3

"""
List all Windows-compatible partitioners in ExecuTorch.

This script provides a programmatic way to discover partitioners that work on Windows.
"""

WINDOWS_COMPATIBLE_PARTITIONERS = {
    "Backend-Specific": [
        {
            "name": "XnnpackPartitioner",
            "module": "executorch.backends.xnnpack.partition.xnnpack_partitioner",
            "description": "Main XNNPACK partitioner for CPU acceleration",
            "variants": [
                "XnnpackDynamicallyQuantizedPartitioner",
                "XnnpackFloatingPointPartitioner",
                "XnnpackQuantizedPartitioner",
            ],
        },
        {
            "name": "OpenvinoPartitioner",
            "module": "executorch.backends.openvino.partitioner",
            "description": "OpenVINO partitioner for Intel hardware optimization",
        },
        {
            "name": "CudaPartitioner",
            "module": "executorch.backends.cuda.cuda_partitioner",
            "description": "CUDA partitioner for NVIDIA GPU acceleration (experimental)",
        },
        {
            "name": "VulkanPartitioner",
            "module": "executorch.backends.vulkan.partitioner.vulkan_partitioner",
            "description": "Vulkan partitioner for GPU acceleration",
        },
        {
            "name": "AotiPartitioner",
            "module": "executorch.backends.aoti.aoti_partitioner",
            "description": "Base partitioner for AOTInductor-driven backends",
        },
    ],
    "Canonical (Platform-Agnostic)": [
        {
            "name": "AllNodePartitioner",
            "module": "executorch.exir.backend.canonical_partitioners.all_node_partitioner",
            "description": "Partitions all nodes in the graph to a specified backend",
        },
        {
            "name": "ConfigerationBasedPartitioner",
            "module": "executorch.exir.backend.canonical_partitioners.config_partitioner",
            "description": "Configuration-driven partitioning base class",
        },
        {
            "name": "GroupBasedPartitioner",
            "module": "executorch.exir.backend.canonical_partitioners.group_partitioner",
            "description": "Partitioner that allows explicit grouping of nodes",
        },
    ],
    "Example/Demo": [
        {
            "name": "ExamplePartitioner",
            "module": "executorch.backends.example.example_partitioner",
            "description": "Example partitioner for add/mul operations",
        },
    ],
}


def list_all_windows_partitioners():
    """Return a list of all Windows-compatible partitioners."""
    all_partitioners = []
    for category, partitioners in WINDOWS_COMPATIBLE_PARTITIONERS.items():
        for part in partitioners:
            all_partitioners.append({
                "category": category,
                "name": part["name"],
                "module": part["module"],
                "description": part["description"],
                "variants": part.get("variants", []),
            })
    return all_partitioners


def print_windows_partitioners():
    """Print all Windows-compatible partitioners in a formatted way."""
    print("=" * 80)
    print("Windows-Compatible Partitioners")
    print("=" * 80)
    print()
    
    for category, partitioners in WINDOWS_COMPATIBLE_PARTITIONERS.items():
        print(f"{category}:")
        print("-" * 80)
        for part in partitioners:
            print(f"  • {part['name']}")
            print(f"    Module: {part['module']}")
            print(f"    Description: {part['description']}")
            if "variants" in part and part["variants"]:
                print(f"    Variants: {', '.join(part['variants'])}")
            print()
    
    all_partitioners = list_all_windows_partitioners()
    print("=" * 80)
    print(f"Total: {len(all_partitioners)} Windows-compatible partitioners")
    print("=" * 80)


if __name__ == "__main__":
    print_windows_partitioners()
