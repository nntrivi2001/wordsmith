# -*- coding: utf-8 -*-
"""
Golden Three Chapters Checker v2.0 (LLM-Driven)

Function: Check if the first three chapters of a novel meet the "Golden Three Chapters" standard

v2.0 major upgrades:
- Keep keyword pre-check as fast mode
- New LLM deep evaluation mode (AI Native)
- Generate structured evaluation prompt, parse XML evaluation results

Core checkpoints:
- Chapter 1: Protagonist appears within 300 words + golden finger clue + strong conflict opening
- Chapter 2: Golden finger display + first small victory + immediate cool points
- Chapter 3: Suspense hook + next stage preview + cool point density >= 1

Usage:
python golden_three_checker.py --auto                    # Fast keyword mode
python golden_three_checker.py --auto --mode llm         # LLM deep evaluation (recommended)
python golden_three_checker.py --auto --generate-prompt  # Generate evaluation prompt only
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

from runtime_compat import enable_windows_utf8_stdio
from typing import Dict, List, Optional, Any

# Import project locator and chapter paths module
from project_locator import resolve_project_root
from chapter_paths import find_chapter_file

# Windows UTF-8 output fix
if sys.platform == "win32":
    enable_windows_utf8_stdio()


# ============================================================================
# LLM Evaluation Prompt Template
# ============================================================================

LLM_EVALUATION_PROMPT = """You are a web novel editor specializing in evaluating whether a novel's opening meets the "Golden Three Chapters" standard.

Please professionally evaluate the content of these three chapters according to the following criteria:

## Golden Three Chapters Standards

### Chapter 1 Core Checkpoints:
1. **Protagonist Appears Within 300 Characters**: Does the protagonist appear within the first 300 characters? Is their identity clear?
2. **Golden Finger Hint**: Is there any hint or clue about the protagonist's "golden finger" (special ability/system)?
3. **Strong Conflict Opening**: Does the opening present a sufficiently strong conflict/crisis/contradiction?

### Chapter 2 Core Checkpoints:
1. **Golden Finger Display**: Is the golden finger clearly displayed? Can readers understand its capabilities?
2. **First Minor Victory**: Does the protagonist achieve their first small-scale victory/success?
3. **Immediate Gratification Scene**: Is there a scene that makes readers feel satisfied/pleased?

### Chapter 3 Core Checkpoints:
1. **Suspense Hook**: Does the chapter end with suspense? Does it motivate readers to continue?
2. **Next Stage Preview**: Does it hint at the upcoming plot direction/new challenges?
3. **Gratification Density**: Does this chapter contain at least 1 obvious gratification scene?

---

## Content to Evaluate

### Chapter 1
```
{chapter1_content}
```

### Chapter 2
```
{chapter2_content}
```

### Chapter 3
```
{chapter3_content}
```

---

## Output Requirements

Please output your evaluation results in the following XML format (strict adherence to format is required):

```xml
<golden_three_assessment>
  <chapter num="1">
    <check name="Protagonist within 300 chars" passed="true|false" score="0-100">
      <evidence>Specific evidence / quoted original text</evidence>
      <suggestion>Improvement suggestions if not passed</suggestion>
    </check>
    <check name="Golden finger hint" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
    <check name="Strong conflict opening" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
  </chapter>

  <chapter num="2">
    <check name="Golden finger display" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
    <check name="First minor victory" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
    <check name="Immediate gratification" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
  </chapter>

  <chapter num="3">
    <check name="Suspense hook" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
    <check name="Next stage preview" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
    <check name="Gratification density >= 1" passed="true|false" score="0-100">
      <evidence>Specific evidence</evidence>
      <suggestion>Improvement suggestions</suggestion>
    </check>
  </chapter>

  <overall_score>0-100</overall_score>
  <verdict>Excellent|Good|Needs Improvement|Seriously Deficient</verdict>
  <top_issues>
    <issue priority="1">Most critical issue to address</issue>
    <issue priority="2">Secondary issue</issue>
  </top_issues>
</golden_three_assessment>
```

Begin the evaluation now:
"""


class GoldenThreeChecker:
    """Golden Three Chapters Checker v2.0"""

    def __init__(self, chapter_files: List[str], mode: str = "keyword"):
        """
        Initialize the checker.

        Args:
            chapter_files: List of chapter file paths (must be the first 3 chapters)
            mode: Check mode ("keyword" fast mode, "llm" LLM evaluation mode)
        """
        if len(chapter_files) != 3:
            raise ValueError("Must provide file paths for the first 3 chapters")

        self.chapter_files = chapter_files
        self.mode = mode
        self.chapters: List[Dict[str, Any]] = []
        self.results: Dict[str, Any] = {
            "mode": mode,
            "ch1": {"Protagonist within 300 chars": False, "Golden finger hint": False, "Strong conflict opening": False, "details": {}},
            "ch2": {"Golden finger display": False, "First minor victory": False, "Immediate gratification": False, "details": {}},
            "ch3": {"Suspense hook": False, "Next stage preview": False, "Gratification density >= 1": False, "details": {}},
        }

    def load_chapters(self) -> None:
        """Load chapter content."""
        for i, file_path in enumerate(self.chapter_files):
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.chapters.append({
                    "number": i + 1,
                    "path": file_path,
                    "content": content,
                    "word_count": len(re.sub(r'\s+', '', content))
                })

    # ============================================================================
    # Fast keyword mode (preserving original logic)
    # ============================================================================

    def check_chapter1_keywords(self) -> None:
        """Check Chapter 1 (keyword mode)."""
        content = self.chapters[0]["content"]
        first_300_chars = content[:300]

        # Check 1: Protagonist appears within 300 characters
        protagonist_keywords = ["Lin Tian", "I", "protagonist", "young man", "he", "Ye Fan", "Xiao Yan", "Chu Feng"]
        for keyword in protagonist_keywords:
            if keyword in first_300_chars:
                self.results["ch1"]["Protagonist within 300 chars"] = True
                self.results["ch1"]["details"]["protagonist_keyword"] = keyword
                break

        # Check 2: Golden finger hint
        golden_finger_keywords = [
            "system", "space", "rebirth", "transmigration", "ring", "old grandfather",
            "spiritual artifact spirit", "inheritance", "bloodline", "awakening", "sign-in", "mission", "panel", "attributes"
        ]
        found = [kw for kw in golden_finger_keywords if kw in content]
        self.results["ch1"]["Golden finger hint"] = len(found) > 0
        self.results["ch1"]["details"]["golden_finger_keywords"] = found

        # Check 3: Strong conflict opening
        conflict_keywords = [
            "divorce humiliation", "shame", "mockery", "trash", "destitute", "crisis",
            "pursuit", "desperate situation", "trapped", "severe injury", "near death", "clan destruction"
        ]
        found = [kw for kw in conflict_keywords if kw in content]
        self.results["ch1"]["Strong conflict opening"] = len(found) > 0
        self.results["ch1"]["details"]["conflict_keywords"] = found

    def check_chapter2_keywords(self) -> None:
        """Check Chapter 2 (keyword mode)."""
        content = self.chapters[1]["content"]

        system_display_keywords = ["【", "╔", "name", "realm", "power", "attributes", "obtained", "reward", "level up"]
        found = [kw for kw in system_display_keywords if kw in content]
        self.results["ch2"]["Golden finger display"] = len(found) >= 2
        self.results["ch2"]["details"]["display_keywords"] = found

        victory_keywords = ["defeat", "victory", "win", "success", "pass", "breakthrough", "instant kill", "crush"]
        found = [kw for kw in victory_keywords if kw in content]
        self.results["ch2"]["First minor victory"] = len(found) > 0
        self.results["ch2"]["details"]["victory_keywords"] = found

        cool_keywords = ["shocked", "impossible", "how could", "everyone stunned", "dumbfounded", "unbelievable"]
        found = [kw for kw in cool_keywords if kw in content]
        self.results["ch2"]["Immediate gratification"] = len(found) >= 2
        self.results["ch2"]["details"]["gratification_keywords"] = found

    def check_chapter3_keywords(self) -> None:
        """Check Chapter 3 (keyword mode)."""
        content = self.chapters[2]["content"]
        last_300_chars = content[-300:]

        suspense_keywords = ["?", "!", "crisis", "about to", "suddenly", "at that moment", "shadow", "killing intent"]
        found = [kw for kw in suspense_keywords if kw in last_300_chars]
        self.results["ch3"]["Suspense hook"] = len(found) >= 2
        self.results["ch3"]["details"]["suspense_keywords"] = found

        preview_keywords = ["secret realm", "grand competition", "selection", "trial", "mission", "challenge", "heading to", "about to"]
        found = [kw for kw in preview_keywords if kw in content]
        self.results["ch3"]["Next stage preview"] = len(found) > 0
        self.results["ch3"]["details"]["preview_keywords"] = found

        cool_count = sum(content.count(kw) for kw in ["shocked", "impossible", "everyone stunned", "genius", "defeat", "obtained"])
        self.results["ch3"]["Gratification density >= 1"] = cool_count >= 1
        self.results["ch3"]["details"]["gratification_count"] = cool_count

    # ============================================================================
    # LLM Evaluation Mode
    # ============================================================================

    def generate_llm_prompt(self) -> str:
        """Generate the LLM evaluation prompt."""
        # Truncate each chapter (to avoid exceeding length limits)
        max_chars_per_chapter = 6000

        ch1 = self.chapters[0]["content"][:max_chars_per_chapter]
        ch2 = self.chapters[1]["content"][:max_chars_per_chapter]
        ch3 = self.chapters[2]["content"][:max_chars_per_chapter]

        prompt = LLM_EVALUATION_PROMPT.format(
            chapter1_content=ch1,
            chapter2_content=ch2,
            chapter3_content=ch3
        )
        return prompt

    def parse_llm_response(self, xml_response: str) -> Dict[str, Any]:
        """Parse the XML evaluation result returned by the LLM."""
        results: Dict[str, Any] = {
            "mode": "llm",
            "ch1": {"details": {}},
            "ch2": {"details": {}},
            "ch3": {"details": {}},
            "overall_score": 0,
            "verdict": "",
            "top_issues": []
        }

        # Extract overall_score
        score_match = re.search(r'<overall_score>(\d+)</overall_score>', xml_response)
        if score_match:
            results["overall_score"] = int(score_match.group(1))

        # Extract verdict
        verdict_match = re.search(r'<verdict>([^<]+)</verdict>', xml_response)
        if verdict_match:
            results["verdict"] = verdict_match.group(1).strip()

        # Extract each chapter's checkpoints
        chapter_pattern = re.compile(
            r'<chapter num="(\d)">(.*?)</chapter>',
            re.DOTALL
        )
        check_pattern = re.compile(
            r'<check name="([^"]+)" passed="(true|false)" score="(\d+)">\s*'
            r'<evidence>([^<]*)</evidence>\s*'
            r'<suggestion>([^<]*)</suggestion>\s*'
            r'</check>',
            re.DOTALL
        )

        for chapter_match in chapter_pattern.finditer(xml_response):
            chapter_num = chapter_match.group(1)
            chapter_content = chapter_match.group(2)
            chapter_key = f"ch{chapter_num}"

            for check_match in check_pattern.finditer(chapter_content):
                check_name = check_match.group(1)
                passed = check_match.group(2) == "true"
                score = int(check_match.group(3))
                evidence = check_match.group(4).strip()
                suggestion = check_match.group(5).strip()

                results[chapter_key][check_name] = passed
                results[chapter_key]["details"][check_name] = {
                    "score": score,
                    "evidence": evidence,
                    "suggestion": suggestion
                }

        # Extract top_issues
        issue_pattern = re.compile(r'<issue priority="(\d)">([^<]+)</issue>')
        for issue_match in issue_pattern.finditer(xml_response):
            priority = int(issue_match.group(1))
            issue_text = issue_match.group(2).strip()
            results["top_issues"].append({"priority": priority, "issue": issue_text})

        return results

    # ============================================================================
    # Report Generation
    # ============================================================================

    def calculate_score(self) -> tuple:
        """Calculate the overall score."""
        total_checks = 0
        passed_checks = 0

        for chapter_key in ["ch1", "ch2", "ch3"]:
            for check_key, check_value in self.results[chapter_key].items():
                if check_key != "details" and isinstance(check_value, bool):
                    total_checks += 1
                    if check_value:
                        passed_checks += 1

        score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        return score, passed_checks, total_checks

    def generate_report(self) -> str:
        """Generate the check report."""
        score, passed, total = self.calculate_score()

        report = []
        report.append("=" * 60)
        report.append(f"Golden Three Chapters Diagnostic Report (Mode: {self.mode})")
        report.append("=" * 60)
        report.append(f"\nOverall Score: {score:.1f}% ({passed}/{total} items passed)\n")

        # Chapter 1
        report.append("-" * 60)
        report.append("【Chapter 1】Check Results")
        report.append("-" * 60)
        for check_name in ["Protagonist within 300 chars", "Golden finger hint", "Strong conflict opening"]:
            passed = self.results["ch1"].get(check_name, False)
            icon = "✅" if passed else "❌"
            report.append(f"{icon} {check_name}: {'Passed' if passed else 'Failed'}")

            # Show details
            detail = self.results["ch1"]["details"].get(check_name)
            if isinstance(detail, dict):
                if detail.get("evidence"):
                    report.append(f"   └─ Evidence: {detail['evidence'][:100]}...")
                if not passed and detail.get("suggestion"):
                    report.append(f"   └─ Suggestion: {detail['suggestion']}")
            elif isinstance(detail, list) and detail:
                report.append(f"   └─ Keywords: {', '.join(detail[:5])}")

        # Chapter 2
        report.append("\n" + "-" * 60)
        report.append("【Chapter 2】Check Results")
        report.append("-" * 60)
        for check_name in ["Golden finger display", "First minor victory", "Immediate gratification"]:
            passed = self.results["ch2"].get(check_name, False)
            icon = "✅" if passed else "❌"
            report.append(f"{icon} {check_name}: {'Passed' if passed else 'Failed'}")
            detail = self.results["ch2"]["details"].get(check_name)
            if isinstance(detail, dict) and detail.get("evidence"):
                report.append(f"   └─ Evidence: {detail['evidence'][:100]}...")
            elif isinstance(detail, list) and detail:
                report.append(f"   └─ Keywords: {', '.join(detail[:5])}")

        # Chapter 3
        report.append("\n" + "-" * 60)
        report.append("【Chapter 3】Check Results")
        report.append("-" * 60)
        for check_name in ["Suspense hook", "Next stage preview", "Gratification density >= 1"]:
            passed = self.results["ch3"].get(check_name, False)
            icon = "✅" if passed else "❌"
            report.append(f"{icon} {check_name}: {'Passed' if passed else 'Failed'}")
            detail = self.results["ch3"]["details"].get(check_name)
            if isinstance(detail, dict) and detail.get("evidence"):
                report.append(f"   └─ Evidence: {detail['evidence'][:100]}...")

        # Improvement suggestions
        report.append("\n" + "=" * 60)
        report.append("【Improvement Suggestions】")
        report.append("=" * 60)

        if score < 60:
            report.append("\n🔴 Warning: The opening lacks appeal and severely impacts reader retention!")
        elif score < 80:
            report.append("\n🟡 Note: The opening has room for improvement")
        else:
            report.append("\n✅ Great! The opening meets the Golden Three Chapters standard")

        # Extra info for LLM mode
        if self.mode == "llm" and self.results.get("top_issues"):
            report.append("\nPriority fixes:")
            for issue in self.results["top_issues"]:
                report.append(f"  {issue['priority']}. {issue['issue']}")

        report.append("\n" + "=" * 60)
        return "\n".join(report)

    def run(self) -> None:
        """Execute the check."""
        print("Loading chapters...")
        self.load_chapters()

        print(f"✅ Loaded {len(self.chapters)} chapters")
        for ch in self.chapters:
            print(f"   - Chapter {ch['number']}: {ch['word_count']} characters")
        print(f"\nExecuting check (mode: {self.mode})...\n")

        if self.mode == "keyword":
            self.check_chapter1_keywords()
            self.check_chapter2_keywords()
            self.check_chapter3_keywords()
            report = self.generate_report()
            print(report)

        elif self.mode == "llm":
            prompt = self.generate_llm_prompt()
            print("=" * 60)
            print("LLM Evaluation Mode: Please send the following prompt to Claude/GPT")
            print("=" * 60)
            print("\n--- PROMPT START ---\n")
            print(prompt[:2000] + "\n...[Content truncated, see output file for full version]...")
            print("\n--- PROMPT END ---\n")

            # Save full prompt
            output_dir = Path(".wordsmith")
            output_dir.mkdir(exist_ok=True)
            prompt_file = output_dir / "golden_three_prompt.md"
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(prompt)
            print(f"📄 Full prompt saved to: {prompt_file}")
            print("\n💡 Usage:")
            print("   1. Send the prompt to Claude/GPT")
            print("   2. Get the XML format evaluation result")
            print("   3. Run: python golden_three_checker.py --parse-response <response.xml>")

        # Save results
        output_dir = Path(".wordsmith")
        output_dir.mkdir(exist_ok=True)
        output_file = output_dir / "golden_three_report.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Detailed results saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Golden Three Chapters Checker v2.0 (LLM-Driven)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fast keyword mode (default)
  python golden_three_checker.py --auto

  # LLM deep evaluation mode (recommended)
  python golden_three_checker.py --auto --mode llm

  # Parse LLM evaluation result
  python golden_three_checker.py --parse-response response.xml
""".strip(),
    )

    parser.add_argument("chapter_files", nargs="*", help="Paths to the first three chapter files")
    parser.add_argument("--auto", action="store_true", help="Automatically locate the first three chapter files")
    parser.add_argument("--mode", choices=["keyword", "llm"], default="keyword",
                        help="Check mode: keyword (fast) / llm (deep)")
    parser.add_argument("--project-root", default=None, help="Project root directory")
    parser.add_argument("--parse-response", metavar="FILE", help="Parse the XML file returned by the LLM")

    args = parser.parse_args()

    # Parse LLM response mode
    if args.parse_response:
        if not os.path.exists(args.parse_response):
            print(f"❌ File not found: {args.parse_response}")
            sys.exit(1)

        with open(args.parse_response, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        checker = GoldenThreeChecker(["dummy"] * 3, mode="llm")
        checker.results = checker.parse_llm_response(xml_content)

        print("=" * 60)
        print("LLM Evaluation Result Parsing")
        print("=" * 60)
        print(json.dumps(checker.results, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Normal check mode
    chapter_files = []

    if args.auto or not args.chapter_files:
        try:
            project_root = resolve_project_root(args.project_root)
        except FileNotFoundError as e:
            print(f"❌ {e}")
            sys.exit(1)

        for i in range(1, 4):
            chapter_path = find_chapter_file(project_root, i)
            if chapter_path:
                chapter_files.append(str(chapter_path))
            else:
                print(f"❌ Cannot find Chapter {i} file")
                sys.exit(1)

        print(f"📂 Project root: {project_root}")
        print(f"📄 Detected first three chapters: {', '.join(Path(f).name for f in chapter_files)}\n")
    else:
        if len(args.chapter_files) < 3:
            print("Usage: python golden_three_checker.py <Chapter1 path> <Chapter2 path> <Chapter3 path>")
            sys.exit(1)
        chapter_files = args.chapter_files[:3]

    try:
        checker = GoldenThreeChecker(chapter_files, mode=args.mode)
        checker.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
