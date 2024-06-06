import datetime
import os


def main():
    title = input("Post title: ")
    subtitle = input("Post subtitle: ")
    default_filename = title.lower().replace(" ", "-")
    filename = input(f"File name (default: {default_filename}): ")
    if not filename:
        filename = default_filename
    tags = input("Tags: ").split(",")
    for i in range(len(tags)):
        tags[i] = tags[i].strip()
    date = input("Date (default: today): ")
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")
    else:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime(
            "%Y-%m-%d"
        )
    if os.path.exists(f"drafts/posts/{filename}.md"):
        print("File already exists!")
        return
    with open(f"drafts/posts/{filename}.md", "w") as f:
        f.write(
            f"""---
title: {title}
subtitle: {subtitle}
date: {date}
tags: {tags}
layout: post.html
---

"""
        )


if __name__ == "__main__":
    main()
