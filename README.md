# LLM Model Selection Tool

A Python utility that detects your hardware capabilities and recommends appropriate Large Language Models (LLMs) for local deployment.

## Features

- **Cross-Platform Hardware Detection**: Supports NVIDIA CUDA, Apple Metal Performance Shaders (MPS), and CPU-only configurations
- **Smart Memory Analysis**: Estimates usable VRAM/memory for AI workloads
- **Model Recommendations**: Suggests optimal LLM models based on your hardware capacity
- **4-bit Quantization Support**: Calculations based on modern quantization techniques
- **Beautiful HTML Reports**: Generates stunning, modern HTML reports with gradient backgrounds and interactive elements
- **Automatic Browser Launch**: Opens the generated report in your default browser

## Requirements

- Python 3.8+
- PyTorch
- psutil

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script to analyze your hardware and get model recommendations:

```bash
python ll_model_selection.py
```

The script will:
1. Detect your hardware capabilities
2. Print analysis results to the console
3. Generate a beautiful HTML report (`hardware_report.html`)
4. Automatically open the report in your default browser

### Console Output Example

```
### Hardware Audit: Darwin ###
* System RAM: 16.00 GB
* Backend: Apple Metal Performance Shaders (MPS)
* Unified Memory: 16.00 GB (Est. Usable for AI: 12.00 GB)

### Feasible Local Deployment (4-bit Quantization) ###
* Effective VRAM Cap: 12.00 GB
* Theoretical Max Parameter Count: ~13B

Recommended Models (4-bit Quantization):
- Llama-3.1-8B: Gold standard for consumer hardware
- Mistral-7B: Excellent general-purpose model
- Gemma-7B: Google's efficient open model
- Qwen2.5-7B: Strong multilingual capabilities

✅ HTML report generated: /path/to/hardware_report.html
   Opening in browser...
```

### HTML Report Features

The generated HTML report includes:
- **Modern gradient design** with purple-to-blue background
- **Performance tier badges** (Enterprise, Professional, Advanced, Standard, Entry)
- **Color-coded stats** for quick visual assessment
- **Interactive hover effects** on all cards
- **Responsive layout** that works on desktop and mobile
- **Detailed model recommendations** with descriptions

## How It Works

The tool uses the following formula to estimate maximum model size:

```
Max Parameters (B) = (Available VRAM - Context Overhead) / GB per Billion Parameters
```

Where:
- **Context Overhead**: 2 GB (for KV cache and runtime overhead)
- **GB per Billion**: 0.75 GB (for 4-bit quantization)

## Supported Backends

1. **NVIDIA CUDA**: Detects GPU VRAM on Windows/Linux systems
2. **Apple MPS**: Uses unified memory on Apple Silicon Macs
3. **CPU**: Falls back to system RAM (with performance warnings)

## Model Recommendations by VRAM

| VRAM Range | Recommended Models |
|------------|-------------------|
| 48GB+ | Llama-3.1-70B, Qwen2.5-72B, Mixtral 8x7B |
| 24GB+ | Llama-3.1-70B (quantized), Command R 35B, Qwen2.5-32B |
| 16GB+ | Llama-3.1-13B, Qwen2.5-14B, Mistral-7B |
| 8GB+ | Llama-3.1-8B, Mistral-7B, Gemma-7B, Qwen2.5-7B |
| <8GB | Phi-3-mini, Gemma-2B, TinyLlama |

## License

MIT License - feel free to use and modify as needed.
