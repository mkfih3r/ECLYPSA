import json
import os

def export_json(analysis_data, filename):
    """Exports the security analysis report as a structured JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, indent=4)
        print(f"[+] JSON report successfully exported to: {filename}")
        return True
    except Exception as e:
        print(f"[-] Error exporting JSON report: {e}")
        return False

def export_html(target, analysis_data, filename):
    """Exports the security analysis report as a stylized HTML dashboard."""
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ECLYPSA AI - Security Report for {target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 10px; margin-top: 0; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ background: #334155; padding: 15px; border-radius: 8px; flex: 1; text-align: center; }}
        .card h3 {{ margin: 0; color: #94a3b8; font-size: 14px; text-transform: uppercase; }}
        .card p {{ margin: 10px 0 0 0; font-size: 24px; font-weight: bold; color: #f1f5f9; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background-color: #0f172a; color: #38bdf8; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
        .CRITICAL {{ background-color: #ef4444; color: white; }}
        .HIGH {{ background-color: #f97316; color: white; }}
        .MEDIUM {{ background-color: #eab308; color: black; }}
        .LOW {{ background-color: #22c55e; color: white; }}
        .INFO {{ background-color: #64748b; color: white; }}
        .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #64748b; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ECLYPSA AI — Security Assessment</h1>
        <p><strong>Target Host:</strong> {target}</p>
        
        <div class="summary">
            <div class="card">
                <h3>Total Open Ports</h3>
                <p>{analysis_data['total_open_ports']}</p>
            </div>
            <div class="card">
                <h3>Overall Threat Score</h3>
                <p>{analysis_data['overall_threat_score']}</p>
            </div>
        </div>

        <h2>Detailed Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Port</th>
                    <th>Service</th>
                    <th>Risk Level</th>
                    <th>Banner</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
"""
    for item in analysis_data.get('findings', []):
        risk = item['risk']
        html_content += f"""
                <tr>
                    <td><strong>{item['port']}</strong></td>
                    <td>{item['service']}</td>
                    <td><span class="badge {risk}">{risk}</span></td>
                    <td><code>{item['banner']}</code></td>
                    <td>{item['recommendation']}</td>
                </tr>
"""

    html_content += f"""
            </tbody>
        </table>
        <div class="footer">
            Generated automatically by ECLYPSA AI Recon Engine
        </div>
    </div>
</body>
</html>
"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"[+] HTML report successfully exported to: {filename}")
        return True
    except Exception as e:
        print(f"[-] Error exporting HTML report: {e}")
        return False
