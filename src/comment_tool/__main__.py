import argparse
import json
import logging
import os

import regex
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("translation.log"), logging.StreamHandler()],
)


class CommentsTool:
    def __init__(self, dictionary_path: str = "translations.json"):
        self.dictionary_path = dictionary_path
        self.translations: dict[str, str] = self._load_dictionary()
        self.japanese_pattern = regex.compile(r"[\p{Hiragana}\p{Katakana}\p{Han}]")
        self.non_ascii_pattern = regex.compile(r"[^\x00-\x7F]")
        self.bom_pattern = regex.compile(r"\ufeff")

    def _load_dictionary(self) -> dict[str, str]:
        """Load the translation dictionary from JSON file."""
        try:
            if os.path.exists(self.dictionary_path):
                with open(self.dictionary_path, encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error loading dictionary: {e}")
            return {}

    def _save_dictionary(self):
        """Save the translation dictionary to JSON file."""
        try:
            with open(self.dictionary_path, "w", encoding="utf-8") as f:
                json.dump(self.translations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Error saving dictionary: {e}")

    def _is_japanese_text(self, text: str) -> bool:
        """Check if text contains Japanese characters."""
        return bool(self.japanese_pattern.search(text))

    def _find_japanese_characters(self, text: str) -> list[tuple[int, int, str]]:
        """Find all Japanese characters in text and return their positions and characters."""
        matches = []
        for match in self.japanese_pattern.finditer(text):
            matches.append((match.start(), match.end(), match.group()))
        return matches

    def _find_non_ascii_characters(self, text: str) -> list[tuple[int, int, str]]:
        """Find all non-ASCII characters in text and return their positions and characters."""
        matches = []
        for match in self.non_ascii_pattern.finditer(text):
            matches.append((match.start(), match.end(), match.group()))
        return matches

    def _find_bom_characters(self, text: str) -> list[tuple[int, int, str]]:
        """Find all BOM characters in text and return their positions."""
        matches = []
        for match in self.bom_pattern.finditer(text):
            matches.append((match.start(), match.end(), match.group()))
        return matches

    def remove_bom_from_file(self, file_path: str) -> bool:
        """Remove BOM characters from a file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Check if file has BOM
            if not self._find_bom_characters(content):
                return False

            # Remove BOM characters
            new_content = self.bom_pattern.sub("", content)

            # Write back to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            logging.info(f"Removed BOM from file: {file_path}")
            return True

        except Exception as e:
            logging.error(f"Error removing BOM from file {file_path}: {e}")
            return False

    def scan_file_for_bom(self, file_path: str) -> list[tuple[int, int, str]]:
        """Scan a file for BOM characters and return their locations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            matches = self._find_bom_characters(content)
            if matches:
                # Convert character positions to line numbers and positions
                lines = content.split("\n")
                line_positions = []
                current_pos = 0

                for line_num, line in enumerate(lines):
                    line_length = len(line) + 1  # +1 for newline
                    for start, _end, char in matches:
                        if current_pos <= start < current_pos + line_length:
                            # Found a match in this line
                            line_positions.append(
                                (line_num + 1, start - current_pos, char)
                            )
                    current_pos += line_length

                return line_positions
            return []

        except Exception as e:
            logging.error(f"Error scanning file {file_path}: {e}")
            return []

    def scan_file_for_japanese(self, file_path: str) -> list[tuple[int, int, str]]:
        """Scan a file for Japanese characters and return their locations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            matches = self._find_japanese_characters(content)
            if matches:
                # Convert character positions to line numbers and positions
                lines = content.split("\n")
                line_positions = []
                current_pos = 0

                for line_num, line in enumerate(lines):
                    line_length = len(line) + 1  # +1 for newline
                    for start, _end, char in matches:
                        if current_pos <= start < current_pos + line_length:
                            # Found a match in this line
                            line_positions.append(
                                (line_num + 1, start - current_pos, char)
                            )
                    current_pos += line_length

                return line_positions
            return []

        except Exception as e:
            logging.error(f"Error scanning file {file_path}: {e}")
            return []

    def scan_file_for_non_ascii(self, file_path: str) -> list[tuple[int, int, str]]:
        """Scan a file for non-ASCII characters and return their locations."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            matches = self._find_non_ascii_characters(content)
            if matches:
                # Convert character positions to line numbers and positions
                lines = content.split("\n")
                line_positions = []
                current_pos = 0

                for line_num, line in enumerate(lines):
                    line_length = len(line) + 1  # +1 for newline
                    for start, _end, char in matches:
                        if current_pos <= start < current_pos + line_length:
                            # Found a match in this line
                            line_positions.append(
                                (line_num + 1, start - current_pos, char)
                            )
                    current_pos += line_length

                return line_positions
            return []

        except Exception as e:
            logging.error(f"Error scanning file {file_path}: {e}")
            return []

    def _extract_comments(self, content: str) -> list[tuple[str, int, int]]:
        """Extract comments from file content."""
        comments = []

        # Handle single-line comments
        for i, line in enumerate(content.split("\n")):
            if "//" in line:
                comment_start = line.find("//")
                comment = line[comment_start:].strip()
                if comment:
                    comments.append((comment, i, i))

        # Handle multi-line comments
        start = 0
        while True:
            start = content.find("/*", start)
            if start == -1:
                break
            end = content.find("*/", start)
            if end == -1:
                break
            comment = content[start : end + 2].strip()
            if comment:
                # Calculate line numbers
                start_line = content[:start].count("\n")
                end_line = content[:end].count("\n")
                comments.append((comment, start_line, end_line))
            start = end + 2

        return comments

    def _update_file_content(
        self, content: str, comments: list[tuple[str, int, int]]
    ) -> str:
        """Update file content by removing comments."""
        lines = content.split("\n")
        for comment, start_line, end_line in comments:
            if comment.startswith("//"):
                # For single-line comments, keep the code part and remove the comment
                line = lines[start_line]
                code_part = line[: line.find("//")].rstrip()
                lines[start_line] = code_part
            else:
                # For multi-line comments, keep the code structure
                first_line = lines[start_line]
                # Keep any code before the comment starts
                code_before = first_line[: first_line.find("/*")].rstrip()

                # Keep any code after the comment ends
                last_line = lines[end_line]
                comment_end_pos = last_line.find("*/")
                code_after = ""
                if comment_end_pos != -1:
                    code_after = last_line[comment_end_pos + 2 :].strip()

                # Update the first line with code before and after
                if code_before and code_after:
                    lines[start_line] = f"{code_before} {code_after}"
                elif code_before:
                    lines[start_line] = code_before
                elif code_after:
                    lines[start_line] = code_after
                else:
                    lines[start_line] = ""

                # Clear the lines in between
                for i in range(start_line + 1, end_line + 1):
                    lines[i] = ""

        # Join lines back together, removing empty lines
        return "\n".join(line for line in lines if line.strip())

    def process_file(self, file_path: str) -> bool:
        """Process a file and extract Japanese comments."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Extract comments
            comments = self._extract_comments(content)

            # Process each comment
            for comment, start_line, _end_line in comments:
                if self._is_japanese_text(comment):
                    # Add to translations if not already present
                    if comment not in self.translations:
                        self.translations[comment] = ""
                        logging.info(
                            f"Found Japanese comment in {file_path} at line {start_line + 1}: {comment}"
                        )

            # Save translations
            self._save_dictionary()
            return True

        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            return False

    def process_files(self, file_paths: list[str]) -> tuple[list[str], list[str]]:
        """Process multiple files and return lists of successful and failed files."""
        processed_files = []
        not_processed_files = []

        for file_path in file_paths:
            if self.process_file(file_path):
                processed_files.append(file_path)
            else:
                not_processed_files.append(file_path)

        return processed_files, not_processed_files


def find_source_files(directory: str) -> list[str]:
    """Find all C/C++ source files in the given directory."""
    source_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".c", ".cpp", ".h", ".hpp")):
                source_files.append(os.path.join(root, file))
    return source_files


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Process C/C++ files for Japanese comments"
    )
    parser.add_argument(
        "--scan", action="store_true", help="Scan files for Japanese characters"
    )
    parser.add_argument(
        "--scan-non-ascii",
        action="store_true",
        help="Scan files for non-ASCII characters",
    )
    parser.add_argument(
        "--scan-bom", action="store_true", help="Scan files for BOM characters"
    )
    parser.add_argument(
        "--remove-bom", action="store_true", help="Remove BOM characters from files"
    )
    parser.add_argument("--file", type=str, help="Process a specific file")
    parser.add_argument(
        "--directory", type=str, default=".", help="Directory to process"
    )

    args = parser.parse_args()

    translator = CommentsTool()

    if args.file:
        files = [args.file]
    else:
        files = find_source_files(args.directory)

    if not files:
        logging.warning("No source files found!")
        return

    if args.scan:
        for file in tqdm(files, desc="Scanning for Japanese characters"):
            matches = translator.scan_file_for_japanese(file)
            if matches:
                logging.info(f"Found Japanese characters in {file}:")
                for line_num, pos, char in matches:
                    logging.info(f"  Line {line_num}, Position {pos}: {char}")
    elif args.scan_non_ascii:
        for file in tqdm(files, desc="Scanning for non-ASCII characters"):
            matches = translator.scan_file_for_non_ascii(file)
            if matches:
                logging.info(f"Found non-ASCII characters in {file}:")
                for line_num, pos, char in matches:
                    logging.info(f"  Line {line_num}, Position {pos}: {char}")
    elif args.scan_bom:
        for file in tqdm(files, desc="Scanning for BOM characters"):
            matches = translator.scan_file_for_bom(file)
            if matches:
                logging.info(f"Found BOM characters in {file}:")
                for line_num, pos, _char in matches:
                    logging.info(f"  Line {line_num}, Position {pos}")
    elif args.remove_bom:
        for file in tqdm(files, desc="Removing BOM characters"):
            if translator.remove_bom_from_file(file):
                logging.info(f"Removed BOM from {file}")
    else:
        for file in tqdm(files, desc="Processing files"):
            translator.process_file(file)


if __name__ == "__main__":
    main()
