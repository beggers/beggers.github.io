import datetime
import os


def main():
    title = input("Post title: ")
    default_filename = title.lower().replace(" ", "-")
    filename = input(f"File name (default: {default_filename}): ")
    if not filename:
        filename = default_filename
    date = input("Date (default: today): ")
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
            "%Y-%m-%d"
        )
    if os.path.exists(f"drafts/{filename}.md"):
        print("File already exists!")
        return
    with open(f"drafts/{filename}.md", "w") as f:
        f.write(
            f"""---
title: {title}
date: {date}
---

"""
        )


if __name__ == "__main__":
    main()
