        current_date = datetime.now().strftime("%Y-%m-%d")
        insert_markdown_section(results_path, current_date, table, 2)


def to_emoji(value: bool) -> str:
    return "\U00002705" if value else "\U0000274C"


def insert_markdown_section(file_path, section_title, section_text, level):
    with open(file_path, "r") as file:
        lines = file.readlines()

    header_prefix = "#" * level
    new_section = f"{header_prefix} {section_title}\n\n{section_text}\n\n"

    # Find the first section with the specified level
    line_number = -1
    for i, line in enumerate(lines):
        if line.startswith(header_prefix):
            line_number = i
            break

    if line_number != -1:
        lines.insert(line_number, new_section)
    else:
        print(f"Markdown file was of unexpected format. No section of level {level} found. Did not write results.")
        return

    # Write the file
    with open(file_path, "w") as file:
        file.writelines(lines)


def ask_yes_no(question: str) -> bool:
    while True:
        response = input(question + " (y/n): ").lower().strip()
        if response == "y":
            return True
        elif response == "n":
            return False
        else:
            print("Please enter either 'y' or 'n'.")


if __name__ == "__main__":
    run(main)
