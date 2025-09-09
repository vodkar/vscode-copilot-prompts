#!/usr/bin/env python3
"""
Token counter for instruction files across different LLMs.
Calculates token counts for Claude, ChatGPT, Gemini, and Grok models.
"""

import glob
import os
from typing import Any, Dict

import yaml

try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False

try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class TokenCounter:
    """Token counter for various LLM models."""

    def __init__(self):
        self.encoders = {}
        self._setup_encoders()

    def _setup_encoders(self):
        """Setup tokenizers for different models."""
        if TIKTOKEN_AVAILABLE:
            # OpenAI models - use cl100k_base for all GPT-4 variants and newer models
            try:
                base_encoding = tiktoken.get_encoding("cl100k_base")
                self.encoders["gpt-4"] = base_encoding
                self.encoders["gpt-3.5-turbo"] = base_encoding
                self.encoders["gpt-4o"] = base_encoding
                self.encoders["gpt-4.1"] = base_encoding
                self.encoders["gpt-5"] = base_encoding
                self.encoders["gpt-5-mini"] = base_encoding
            except Exception:
                # Final fallback
                fallback = tiktoken.get_encoding("cl100k_base")
                for model in ["gpt-4", "gpt-3.5-turbo", "gpt-4o", "gpt-4.1", "gpt-5", "gpt-5-mini"]:
                    self.encoders[model] = fallback

    def count_tokens_openai(self, text: str, model: str = "gpt-4") -> int:
        """Count tokens for OpenAI models."""
        if not TIKTOKEN_AVAILABLE:
            # Rough approximation: 1 token ≈ 4 characters
            return len(text) // 4

        encoder = self.encoders.get(model, self.encoders.get("gpt-4"))
        if encoder:
            return len(encoder.encode(text))
        return len(text) // 4

    def count_tokens_claude(self, text: str) -> int:
        """Count tokens for Claude models."""
        if ANTHROPIC_AVAILABLE:
            try:
                client = Anthropic()
                # Use token counting endpoint if available
                return client.count_tokens(text)
            except Exception:
                pass

        # Rough approximation for Claude: 1 token ≈ 3.5 characters
        return int(len(text) / 3.5)

    def count_tokens_gemini(self, text: str) -> int:
        """Count tokens for Gemini models."""
        # Gemini uses similar tokenization to GPT models
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4

    def count_tokens_grok(self, text: str) -> int:
        """Count tokens for Grok models."""
        # Grok likely uses similar tokenization to GPT models
        # Rough approximation: 1 token ≈ 4 characters
        return len(text) // 4

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single instruction file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return {
                "error": str(e),
                "file_path": file_path,
                "file_size_bytes": 0,
                "character_count": 0,
                "average_tokens": 0,
                "token_counts": {},
            }

        file_stats = os.stat(file_path)

        # Calculate token counts
        claude_opus = self.count_tokens_claude(content)
        claude_sonnet = self.count_tokens_claude(content)
        gpt5 = self.count_tokens_openai(content, "gpt-5")
        gpt5_mini = self.count_tokens_openai(content, "gpt-5-mini")
        gemini_pro = self.count_tokens_gemini(content)
        gemini_flash = self.count_tokens_gemini(content)
        grok = self.count_tokens_grok(content)

        # Calculate average tokens for this file
        all_tokens = [claude_opus, claude_sonnet, gpt5, gpt5_mini, gemini_pro, gemini_flash, grok]
        avg_tokens = int(sum(all_tokens) / len(all_tokens))

        result = {
            "file_path": file_path,
            "file_size_bytes": file_stats.st_size,
            "character_count": len(content),
            "average_tokens": avg_tokens,
            "token_counts": {
                "claude": {
                    "claude-4-opus": claude_opus,
                    "claude-4-sonnet": claude_sonnet,
                },
                "openai": {
                    "gpt-5": gpt5,
                    "gpt-5-mini": gpt5_mini,
                },
                "google": {
                    "gemini-2.5-pro": gemini_pro,
                    "gemini-2.5-flash": gemini_flash,
                },
                "x": {
                    "grok-1.5": grok,
                },
            },
        }

        return result


def main():
    """Main function to analyze all instruction files."""
    counter = TokenCounter()

    # Find all *-instructions.md files
    instruction_files = glob.glob("**/*-instructions.md", recursive=True)

    if not instruction_files:
        print(
            "No *-instructions.md files found in the current directory or subdirectories."
        )
        return

    results = {
        "analysis_metadata": {
            "total_files": len(instruction_files),
            "tiktoken_available": TIKTOKEN_AVAILABLE,
            "anthropic_available": ANTHROPIC_AVAILABLE,
            "note": "Token counts are approximations when official tokenizers are unavailable",
        },
        "files": {},
        "averages": {},
    }

    for file_path in sorted(instruction_files):
        print(f"Analyzing: {file_path}")
        file_result = counter.analyze_file(file_path)

        # Use relative path as key for cleaner output
        rel_path = os.path.relpath(file_path)
        results["files"][rel_path] = file_result

    # Calculate averages
    if results["files"]:
        total_files = len(results["files"])
        avg_file_size = sum(data["file_size_bytes"] for data in results["files"].values() if "error" not in data) / total_files
        avg_char_count = sum(data["character_count"] for data in results["files"].values() if "error" not in data) / total_files
        
        # Calculate average token counts for each model
        avg_tokens = {}
        for provider in ["claude", "openai", "google", "x"]:
            avg_tokens[provider] = {}
            for file_data in results["files"].values():
                if "error" not in file_data:
                    for model_name, token_count in file_data["token_counts"][provider].items():
                        if model_name not in avg_tokens[provider]:
                            avg_tokens[provider][model_name] = []
                        avg_tokens[provider][model_name].append(token_count)
        
        # Calculate final averages
        for provider in avg_tokens:
            for model_name in avg_tokens[provider]:
                avg_tokens[provider][model_name] = int(sum(avg_tokens[provider][model_name]) / len(avg_tokens[provider][model_name]))
        
        results["averages"] = {
            "average_file_size_bytes": int(avg_file_size),
            "average_character_count": int(avg_char_count),
            "average_token_counts": avg_tokens
        }

    # Write results to YAML file
    output_file = "token_analysis_report.yaml"
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            results, f, default_flow_style=False, sort_keys=False, allow_unicode=True
        )

    print(f"\nAnalysis complete! Report saved to: {output_file}")

    # Print summary
    print("\nSummary:")
    for rel_path, data in results["files"].items():
        if "error" not in data:
            avg_tokens = data["average_tokens"]
            claude_tokens = data["token_counts"]["claude"]["claude-4-opus"]
            gpt5_tokens = data["token_counts"]["openai"]["gpt-5"]
            gemini_tokens = data["token_counts"]["google"]["gemini-2.5-pro"]
            print(
                f"  {rel_path}: ~{avg_tokens} tokens (avg), ~{claude_tokens} tokens (Claude 4 Opus), ~{gpt5_tokens} tokens (GPT-5), ~{gemini_tokens} tokens (Gemini 2.5 Pro)"
            )
    
    # Print averages
    if "averages" in results:
        print("\nAverages across all files:")
        avg_data = results["averages"]
        avg_claude = avg_data["average_token_counts"]["claude"]["claude-4-opus"]
        avg_gpt5 = avg_data["average_token_counts"]["openai"]["gpt-5"]
        avg_gemini = avg_data["average_token_counts"]["google"]["gemini-2.5-pro"]
        print(f"  Average file size: {avg_data['average_file_size_bytes']} bytes")
        print(f"  Average character count: {avg_data['average_character_count']} characters")
        print(f"  Average tokens: ~{avg_claude} (Claude 4 Opus), ~{avg_gpt5} (GPT-5), ~{avg_gemini} (Gemini 2.5 Pro)")


if __name__ == "__main__":
    main()
