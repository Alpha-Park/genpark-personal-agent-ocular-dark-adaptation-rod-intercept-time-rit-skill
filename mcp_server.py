"""
MCP Server for Ocular Dark Adaptation Rod Intercept Time (RIT) Skill.
Conforms to Model Context Protocol (MCP) JSON-RPC 2.0 stdio specification.
"""

import sys
import json
from client import DarkAdaptationRITClient


def handle_request(line: str) -> None:
    try:
        req = json.loads(line)
    except Exception:
        return

    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {
                    "name": "genpark-personal-agent-ocular-dark-adaptation-rod-intercept-time-rit-skill",
                    "version": "1.0.0"
                }
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_dark_adaptation_curve",
                        "description": "Analyze retinal dark adaptation kinetics, Kohlrausch break, and calculate Rod Intercept Time (RIT).",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "time_minutes": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Minutes elapsed since photo-bleach."
                                },
                                "log_sensitivity_thresholds": {
                                    "type": "array",
                                    "items": {"type": "number"},
                                    "description": "Log luminance threshold values (log cd/m^2)."
                                },
                                "target_scotopic_threshold": {
                                    "type": "number",
                                    "description": "Target log threshold for RIT (default: 3.0)."
                                },
                                "age_years": {"type": "integer", "description": "Subject age in years."}
                            },
                            "required": ["time_minutes", "log_sensitivity_thresholds"]
                        }
                    }
                ]
            }
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_dark_adaptation_curve":
            target = float(args.get("target_scotopic_threshold", 3.0))
            client = DarkAdaptationRITClient(target_scotopic_threshold_log_units=target)
            times = args.get("time_minutes", [])
            sensitivities = args.get("log_sensitivity_thresholds", [])
            age = int(args.get("age_years", 35))
            try:
                res = client.analyze_dark_adaptation_curve(
                    time_minutes=[float(t) for t in times],
                    log_sensitivity_thresholds=[float(s) for s in sensitivities],
                    age_years=age
                )
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
                    }
                }
            except Exception as e:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
    else:
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method {method} not found"}
        }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


def main():
    for line in sys.stdin:
        if line.strip():
            handle_request(line)


if __name__ == "__main__":
    main()
