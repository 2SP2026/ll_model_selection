"""
HTML Report Generator for Hardware Detection Results.
Creates a modern, visually stunning dashboard-style report.
"""
from datetime import datetime
from typing import Dict, List, Tuple

def generate_html_report(
    system: str,
    ram_gb: float,
    device_type: str,
    vram_gb: float,
    max_params: int,
    gpu_details: List[Dict] = None,
    recommended_models: List[Tuple[str, str]] = None
) -> str:
    """
    Generate a beautiful HTML report for hardware detection results.
    
    Args:
        system: Operating system name
        ram_gb: Total system RAM in GB
        device_type: Device type ('cuda', 'mps', or 'cpu')
        vram_gb: Available VRAM/memory for AI in GB
        max_params: Maximum parameter count (in billions)
        gpu_details: List of GPU information dicts (for CUDA)
        recommended_models: List of (model_name, description) tuples
    
    Returns:
        str: Complete HTML document as string
    """
    
    # Determine backend display name and icon
    backend_info = {
        'cuda': ('NVIDIA CUDA', '🎮', '#76B900'),
        'mps': ('Apple Metal (MPS)', '🍎', '#147EFB'),
        'cpu': ('CPU Only', '💻', '#FF6B6B')
    }
    backend_name, backend_icon, backend_color = backend_info.get(
        device_type, ('Unknown', '❓', '#888888')
    )
    
    # Build GPU details HTML
    gpu_html = ""
    if gpu_details:
        for gpu in gpu_details:
            gpu_html += f"""
            <div class="gpu-card">
                <div class="gpu-icon">🎮</div>
                <div class="gpu-info">
                    <div class="gpu-name">{gpu['name']}</div>
                    <div class="gpu-vram">{gpu['vram']:.2f} GB VRAM</div>
                </div>
            </div>
            """
    
    # Build model recommendations HTML
    models_html = ""
    if recommended_models:
        for model_name, description in recommended_models:
            models_html += f"""
            <div class="model-card">
                <div class="model-icon">🤖</div>
                <div class="model-info">
                    <div class="model-name">{model_name}</div>
                    <div class="model-desc">{description}</div>
                </div>
            </div>
            """
    
    # Performance tier badge
    if vram_gb >= 48:
        tier = "Enterprise"
        tier_color = "#9333EA"
    elif vram_gb >= 24:
        tier = "Professional"
        tier_color = "#3B82F6"
    elif vram_gb >= 16:
        tier = "Advanced"
        tier_color = "#10B981"
    elif vram_gb >= 8:
        tier = "Standard"
        tier_color = "#F59E0B"
    else:
        tier = "Entry"
        tier_color = "#EF4444"
    
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hardware Analysis Report - LLM Model Selection</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
            color: #1a1a1a;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 3rem;
            animation: fadeInDown 0.6s ease-out;
        }}
        
        .header h1 {{
            color: white;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 20px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            color: rgba(255,255,255,0.9);
            font-size: 1.1rem;
            font-weight: 400;
        }}
        
        .report-card {{
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 60px rgba(0,0,0,0.15);
            animation: fadeInUp 0.6s ease-out;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .report-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 25px 70px rgba(0,0,0,0.2);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            padding-bottom: 1.5rem;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .card-title {{
            font-size: 1.75rem;
            font-weight: 700;
            color: #1a1a1a;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        
        .card-icon {{
            font-size: 2rem;
        }}
        
        .badge {{
            padding: 0.5rem 1.25rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .tier-badge {{
            background: linear-gradient(135deg, {tier_color}, {tier_color}dd);
            color: white;
            box-shadow: 0 4px 15px {tier_color}40;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid {backend_color};
            transition: all 0.3s ease;
        }}
        
        .stat-box:hover {{
            transform: translateX(4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: #6b7280;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.5rem;
        }}
        
        .stat-value {{
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
        }}
        
        .stat-unit {{
            font-size: 1rem;
            color: #6b7280;
            font-weight: 500;
        }}
        
        .backend-display {{
            background: linear-gradient(135deg, {backend_color}15, {backend_color}05);
            border: 2px solid {backend_color}40;
            padding: 1.5rem;
            border-radius: 16px;
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .backend-icon {{
            font-size: 3rem;
        }}
        
        .backend-info {{
            flex: 1;
        }}
        
        .backend-name {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {backend_color};
            margin-bottom: 0.25rem;
        }}
        
        .backend-desc {{
            color: #6b7280;
            font-size: 0.95rem;
        }}
        
        .gpu-grid {{
            display: grid;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .gpu-card {{
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            padding: 1.25rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 1rem;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }}
        
        .gpu-card:hover {{
            border-color: #76B900;
            box-shadow: 0 4px 12px rgba(118, 185, 0, 0.15);
        }}
        
        .gpu-icon {{
            font-size: 2rem;
        }}
        
        .gpu-name {{
            font-weight: 600;
            color: #1a1a1a;
            font-size: 1.1rem;
        }}
        
        .gpu-vram {{
            color: #6b7280;
            font-size: 0.9rem;
        }}
        
        .models-grid {{
            display: grid;
            gap: 1rem;
        }}
        
        .model-card {{
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            padding: 1.25rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 1rem;
            border: 1px solid #e5e7eb;
            transition: all 0.3s ease;
        }}
        
        .model-card:hover {{
            border-color: {backend_color};
            box-shadow: 0 4px 12px {backend_color}30;
            transform: translateX(4px);
        }}
        
        .model-icon {{
            font-size: 2rem;
        }}
        
        .model-name {{
            font-weight: 700;
            color: #1a1a1a;
            font-size: 1.1rem;
            margin-bottom: 0.25rem;
        }}
        
        .model-desc {{
            color: #6b7280;
            font-size: 0.9rem;
        }}
        
        .warning-box {{
            background: linear-gradient(135deg, #FEF3C7, #FDE68A);
            border-left: 4px solid #F59E0B;
            padding: 1.25rem;
            border-radius: 12px;
            margin-top: 1.5rem;
            display: flex;
            gap: 1rem;
        }}
        
        .warning-icon {{
            font-size: 1.5rem;
        }}
        
        .warning-content {{
            flex: 1;
        }}
        
        .warning-title {{
            font-weight: 700;
            color: #92400E;
            margin-bottom: 0.5rem;
        }}
        
        .warning-text {{
            color: #78350F;
            font-size: 0.95rem;
            line-height: 1.6;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 2rem;
            font-size: 0.9rem;
        }}
        
        .footer a {{
            color: white;
            text-decoration: none;
            font-weight: 600;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .report-card {{
                padding: 1.5rem;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Hardware Analysis Report</h1>
            <div class="subtitle">LLM Model Selection & Capacity Assessment</div>
        </div>
        
        <!-- System Overview Card -->
        <div class="report-card">
            <div class="card-header">
                <div class="card-title">
                    <span class="card-icon">💻</span>
                    System Overview
                </div>
                <div class="badge tier-badge">{tier} Tier</div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-label">Operating System</div>
                    <div class="stat-value">{system}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Total RAM</div>
                    <div class="stat-value">{ram_gb:.1f} <span class="stat-unit">GB</span></div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Usable AI Memory</div>
                    <div class="stat-value">{vram_gb:.1f} <span class="stat-unit">GB</span></div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Max Model Size</div>
                    <div class="stat-value">~{max_params} <span class="stat-unit">B</span></div>
                </div>
            </div>
            
            <div class="backend-display">
                <div class="backend-icon">{backend_icon}</div>
                <div class="backend-info">
                    <div class="backend-name">{backend_name}</div>
                    <div class="backend-desc">Detected compute backend for AI workloads</div>
                </div>
            </div>
            
            {f'<div class="gpu-grid">{gpu_html}</div>' if gpu_html else ''}
        </div>
        
        <!-- Model Recommendations Card -->
        <div class="report-card">
            <div class="card-header">
                <div class="card-title">
                    <span class="card-icon">🎯</span>
                    Recommended Models
                </div>
                <div class="badge" style="background: #E0E7FF; color: #4338CA;">4-bit Quantization</div>
            </div>
            
            <div class="models-grid">
                {models_html}
            </div>
            
            {'''
            <div class="warning-box">
                <div class="warning-icon">⚠️</div>
                <div class="warning-content">
                    <div class="warning-title">CPU Performance Notice</div>
                    <div class="warning-text">
                        CPU inference will be significantly slower than GPU/MPS acceleration. 
                        Consider using GGUF format models with llama.cpp for better CPU performance.
                    </div>
                </div>
            </div>
            ''' if device_type == 'cpu' else ''}
        </div>
        
        <div class="footer">
            Generated on {timestamp} | <a href="https://github.com">LLM Model Selection Tool</a>
        </div>
    </div>
</body>
</html>"""
    
    return html_template
