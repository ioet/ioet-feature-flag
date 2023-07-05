import re
import os
from get_version import get_version
from markdown_to_text import markdown_to_text

changelog_lines = {}
changelog_first_line = "v" + get_version("setup.py")
changelog_first_line = os.getenv("VERSION", changelog_first_line)
in_changelog_section = False
version_regex = "^v[0-9]\.+[0-9]+\.[0-9] \([^)]*\)"
changelog_line_regex = "(FF-[1-9][0-9]*) (.*) \((#[1-9][0-9]*)\) \(([0-9a-f]+)\)$"
current_type = None

with open("./CHANGELOG.md") as changelog_file:
    for line in changelog_file:
        text_line = markdown_to_text(line)
        if re.match(version_regex, text_line):
            if text_line.startswith(changelog_first_line):
                changelog_lines["version"] = text_line
                in_changelog_section = True
                continue
            in_changelog_section = False
        if in_changelog_section:
            if text_line in ["Feature", "Fix", "Build", "CI", "DOCS", "PERF", "REFACTOR", "TEST"]:
                changelog_lines["type"] = text_line
                continue
            parsed = re.search(changelog_line_regex, text_line)
            if parsed:
                changelog_lines["ticket"] = parsed.group(1)
                changelog_lines["title"] = parsed.group(2)
                changelog_lines["FF"] = parsed.group(3)
                changelog_lines["commit"] = parsed.group(4)

slack_message = """
Released *{version}* to *{environment}*:
""".format(
    version=changelog_first_line, environment=os.getenv("ENVIRONMENT", "Staging")
)
slack_message += f"- {changelog_lines['ticket']}: {changelog_lines['title']} ({changelog_lines['FF']} merged as {changelog_lines['commit']}) ({changelog_lines['type']})"
print(slack_message)
