"""
LLM Model Selection Tool
========================
Hardware capacity detection and model recommendation utility.

Author: Antigravity
Created: 2026-01-21
Version: 1.0
Last Modified: 2026-01-21

Description:
    Detects available hardware (NVIDIA CUDA, Apple MPS, or CPU) and recommends
    appropriate LLM models for local deployment based on VRAM/memory capacity.
    Generates a beautiful HTML report with detailed recommendations.

Dependencies:
    - torch>=2.0.0
    - psutil>=5.9.0

Usage:
    python ll_model_selection.py

Output:
    - Console output with hardware analysis
    - hardware_report.html (auto-opens in browser)

Version History:
----------------
v1.0 (2026-01-21) - Initial release
    - Hardware detection for CUDA, MPS, CPU
    - Model recommendations based on VRAM
    - HTML report generation
"""
import torch
import psutil
import platform
import webbrowser
from pathlib import Path
from typing import Tuple, List, Dict
from html_report import generate_html_report

# Constants for memory calculations
MPS_USABLE_MEMORY_RATIO = 0.75  # Conservative estimate for macOS unified memory
CPU_USABLE_MEMORY_RATIO = 0.5   # Half of RAM for CPU inference
CONTEXT_OVERHEAD_GB = 2.0        # Memory overhead for context/KV cache
QUANT_4BIT_GB_PER_BILLION = 0.75 # VRAM per billion parameters (4-bit quantization)

# VRAM Tiers
VRAM_TIER_ENTERPRISE = 48.0
VRAM_TIER_PROFESSIONAL = 24.0
VRAM_TIER_ADVANCED = 16.0
VRAM_TIER_STANDARD = 8.0

def get_hardware_capacity() -> Tuple[float, str, float, str, List[Dict]]:
    """
    Detect available hardware and estimate usable VRAM/memory for LLM inference.
    
    Returns:
        Tuple containing:
        - vram_gb (float): Estimated VRAM in GB
        - device_type (str): 'cuda'/'mps'/'cpu'
        - ram_gb (float): Total system RAM in GB
        - system (str): Operating system name
        - gpu_details (List[Dict]): GPU information (for CUDA)
    """
    system = platform.system()
    device_type = "cpu"
    vram_gb = 0.0
    ram_gb = psutil.virtual_memory().total / (1024 ** 3)

    gpu_details = []
    
    print(f"### Hardware Audit: {system} ###")
    print(f"* System RAM: {ram_gb:.2f} GB")
    
    # 1. Check NVIDIA GPU (Windows/Linux)
    try:
        if torch.cuda.is_available():
            device_type = "cuda"
            gpu_count = torch.cuda.device_count()
            print(f"* Backend: NVIDIA CUDA ({gpu_count} devices)")
            for i in range(gpu_count):
                props = torch.cuda.get_device_properties(i)
                v_mem = props.total_memory / (1024 ** 3)
                print(f"  - GPU {i}: {props.name} | {v_mem:.2f} GB VRAM")
                gpu_details.append({'name': props.name, 'vram': v_mem})
                vram_gb += v_mem
    except (RuntimeError, AttributeError) as e:
        print(f"  Warning: CUDA detection failed: {e}")
    except ImportError:
        print("  Warning: CUDA not available (PyTorch built without CUDA support)")
    except Exception as e:
        print(f"  Warning: Unexpected error during CUDA detection: {e}")
            
    # 2. Check Apple Silicon (Mac)
    if vram_gb == 0:  # Only check if CUDA wasn't found
        try:
            if torch.backends.mps.is_available():
                device_type = "mps"
                # On Mac, VRAM is effectively Unified Memory (System RAM)
                # MacOS usually reserves ~20-30% for OS, so we use conservative estimate
                vram_gb = ram_gb * MPS_USABLE_MEMORY_RATIO
                print(f"* Backend: Apple Metal Performance Shaders (MPS)")
                print(f"* Unified Memory: {ram_gb:.2f} GB (Est. Usable for AI: {vram_gb:.2f} GB)")
        except (RuntimeError, AttributeError) as e:
            print(f"  Warning: MPS detection failed: {e}")
        except Exception as e:
            print(f"  Warning: Unexpected error during MPS detection: {e}")
        
    # 3. Fallback to CPU
    if vram_gb == 0:
        device_type = "cpu"
        vram_gb = ram_gb * CPU_USABLE_MEMORY_RATIO
        print("* Backend: CPU Only (Not recommended for large models)")
        print(f"* Estimated Usable Memory: {vram_gb:.2f} GB")
        
    return vram_gb, device_type, ram_gb, system, gpu_details

def recommend_models(vram_gb: float, device_type: str) -> Tuple[int, List[Tuple[str, str]]]:
    """
    Recommend LLM models based on available VRAM/memory.
    
    Args:
        vram_gb: Available VRAM in GB
        device_type: Type of compute device ('cuda', 'mps', or 'cpu')
    
    Returns:
        Tuple containing:
        - max_params (int): Maximum parameter count in billions
        - models (List[Tuple[str, str]]): List of (model_name, description) tuples
    """
    # Rule of Thumb (4-bit quant): ~0.7-0.8 GB VRAM per 1 Billion Parameters + Context overhead
    # Formula: Max_Params = (VRAM - Context_Overhead) / GB_per_Billion
    
    if QUANT_4BIT_GB_PER_BILLION > 0:
        max_params = (vram_gb - CONTEXT_OVERHEAD_GB) / QUANT_4BIT_GB_PER_BILLION
    else:
        max_params = 0

    if max_params < 2: 
        max_params = 2

    print(f"\n### Feasible Local Deployment (4-bit Quantization) ###")
    print(f"* Effective VRAM Cap: {vram_gb:.2f} GB")
    print(f"* Theoretical Max Parameter Count: ~{int(max_params)}B")
    
    models = []
    print("\nRecommended Models (4-bit Quantization):")
    if vram_gb >= VRAM_TIER_ENTERPRISE:
        models = [
            ("Llama-3.1-70B / Llama-3.3-70B", "High performance flagship models"),
            ("Qwen2.5-72B", "Excellent reasoning and multilingual capabilities"),
            ("Mixtral 8x7B", "Mixture of Experts architecture for efficiency")
        ]
    elif vram_gb >= VRAM_TIER_PROFESSIONAL:
        models = [
            ("Llama-3.1-70B", "Heavily quantized, may be slower but very capable"),
            ("Mixtral 8x7B", "Comfortable fit with good performance"),
            ("Command R (35B)", "Optimized for RAG and tool use"),
            ("Qwen2.5-32B", "Strong reasoning with multilingual support")
        ]
    elif vram_gb >= VRAM_TIER_ADVANCED:
        models = [
            ("Llama-3.1-13B / Llama-2-13B", "Balanced performance and efficiency"),
            ("Mistral-7B", "Quantized with plenty of headroom"),
            ("Qwen2.5-14B", "Strong performance in this tier")
        ]
    elif vram_gb >= VRAM_TIER_STANDARD:
        models = [
            ("Llama-3.1-8B", "Gold standard for consumer hardware"),
            ("Mistral-7B", "Excellent general-purpose model"),
            ("Gemma-7B", "Google's efficient open model"),
            ("Qwen2.5-7B", "Strong multilingual capabilities")
        ]
    else:
        models = [
            ("Phi-3-mini (3.8B)", "Highly capable for its size"),
            ("Gemma-2B", "Efficient small model"),
            ("TinyLlama (1.1B)", "Minimal resource requirements")
        ]
    
    for model_name, description in models:
        print(f"- {model_name}: {description}")
    
    if device_type == "cpu":
        print("\n⚠️  Note: CPU inference will be significantly slower than GPU/MPS.")
        print("   Consider using GGUF format models with llama.cpp for better CPU performance.")
    
    return int(max_params), models

def main(output_path: str = "hardware_report.html"):
    """
    Main execution function.
    
    Args:
        output_path (str): Path to save the HTML report.
    """
    # Get hardware information
    vram_gb, device_type, ram_gb, system, gpu_details = get_hardware_capacity()
    
    # Get model recommendations
    max_params, models = recommend_models(vram_gb, device_type)
    
    # Generate HTML report
    html_content = generate_html_report(
        system=system,
        ram_gb=ram_gb,
        device_type=device_type,
        vram_gb=vram_gb,
        max_params=max_params,
        gpu_details=gpu_details if gpu_details else None,
        recommended_models=models
    )
    
    # Save report to file
    out_file = Path(output_path)
    try:
        out_file.write_text(html_content, encoding='utf-8')
        print(f"\n✅ HTML report generated: {out_file.absolute()}")
        print("   Opening in browser...")
        
        # Open in default browser
        webbrowser.open(f"file://{out_file.absolute()}")
    except IOError as e:
        print(f"\n❌ Error saving report: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()