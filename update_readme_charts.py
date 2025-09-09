#!/usr/bin/env python3
"""
Script to update mermaid gantt charts in README files based on token_analysis_report.yaml
"""

import os
import re
from typing import Any

import yaml


def load_token_data() -> dict[str, Any]:
    """Load token analysis data from YAML file"""
    with open("token_analysis_report.yaml", "r") as f:
        return yaml.safe_load(f)


def create_gantt_chart(relevant_files: dict[str, Any]) -> str:
    """Create mermaid gantt chart from token data"""
    chart_lines: list[str] = [
        "```mermaid",
        "%%{init: {'gantt': {'leftPadding': 200, 'rightPadding': 75, 'topPadding': 75, 'fontSize': 11, 'sectionFontSize': 16}}}%%",
        "gantt",
        "    title Token counts per file and tokenizer (values = tokens)",
        "    dateFormat  X",
        "    axisFormat  %s",
        "",
    ]

    # Group files by type
    for file_path, file_data in relevant_files.items():
        # Create section name from file name
        file_name = (
            os.path.basename(file_path).replace(".md", "").replace("-", " ").title()
        )
        chart_lines.append(f"    section {file_name}")

        # Add tokenizer data
        token_counts = file_data["token_counts"]

        # Claude models
        claude_opus = token_counts["claude"]["claude-4-opus"]
        claude_sonnet = token_counts["claude"]["claude-4-sonnet"]
        chart_lines.append(f"    Claude Opus    : 0, {claude_opus}")
        chart_lines.append(f"    Claude Sonnet  : 0, {claude_sonnet}")

        # OpenAI models
        gpt5 = token_counts["openai"]["gpt-5"]
        gpt5_mini = token_counts["openai"]["gpt-5-mini"]
        chart_lines.append(f"    GPT-5          : 0, {gpt5}")
        chart_lines.append(f"    GPT-5 Mini     : 0, {gpt5_mini}")

        # Google models
        gemini_pro = token_counts["google"]["gemini-2.5-pro"]
        gemini_flash = token_counts["google"]["gemini-2.5-flash"]
        chart_lines.append(f"    Gemini Pro     : 0, {gemini_pro}")
        chart_lines.append(f"    Gemini Flash   : 0, {gemini_flash}")

        # X model
        grok = token_counts["x"]["grok-1.5"]
        chart_lines.append(f"    Grok 1.5       : 0, {grok}")
        chart_lines.append("")

    chart_lines.append("```")
    return "\n".join(chart_lines)


def update_readme_file(readme_path: str, new_chart: str) -> bool:
    """Update README file with new gantt chart"""
    if not os.path.exists(readme_path):
        return False

    with open(readme_path, "r") as f:
        content = f.read()

    # Pattern to match existing mermaid gantt chart
    pattern = r"```mermaid\s*\n%%\{init:.*?\n```"

    if re.search(pattern, content, re.DOTALL):
        # Replace existing chart
        updated_content = re.sub(pattern, new_chart, content, flags=re.DOTALL)
    else:
        # No existing chart found, skip this file
        return False

    with open(readme_path, "w") as f:
        f.write(updated_content)

    return True


def get_readme_mappings(files_data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Generate README mappings based on files in token analysis data"""
    readme_groups: dict[str, dict[str, Any]] = {}
    
    for file_path, file_data in files_data.items():
        if not file_path.endswith('.md'):
            continue
            
        # Determine which README this file should belong to
        if file_path.startswith('languages/'):
            # Language-specific files go to their language README
            parts = file_path.split('/')
            if len(parts) >= 2:
                language_dir = f"{parts[0]}/{parts[1]}"
                readme_path = f"{language_dir}/README.md"
                if readme_path not in readme_groups:
                    readme_groups[readme_path] = {}
                readme_groups[readme_path][file_path] = file_data
        elif file_path.startswith('approaches/'):
            # Approach-specific files go to their approach README
            parts = file_path.split('/')
            if len(parts) >= 2:
                approach_dir = f"{parts[0]}/{parts[1]}"
                readme_path = f"{approach_dir}/README.md"
                if readme_path not in readme_groups:
                    readme_groups[readme_path] = {}
                readme_groups[readme_path][file_path] = file_data
        else:
            # Root level files go to main README
            readme_path = "README.md"
            if readme_path not in readme_groups:
                readme_groups[readme_path] = {}
            readme_groups[readme_path][file_path] = file_data
    
    return readme_groups


def main() -> None:
    """Main function to update all README files"""
    data = load_token_data()
    files_data = data["files"]
    
    # Generate README mappings based on actual file data
    readme_mappings = get_readme_mappings(files_data)
    
    for readme_path, relevant_files in readme_mappings.items():
        if os.path.exists(readme_path):
            chart = create_gantt_chart(relevant_files)
            if update_readme_file(readme_path, chart):
                print(f"Updated {readme_path}")
            else:
                print(f"No gantt chart found in {readme_path}")
        else:
            print(f"README not found: {readme_path}")

    print("README update complete")


if __name__ == "__main__":
    main()
