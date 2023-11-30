---
title: About
description: About me! And this website.
nav: 1
---

# About me

I'm Ben!

I work on computer stuff -- mainly "infrastructure," which seems to mean the computer stuff at least one layer removed from user interaction -- at a company called [Chroma](https://trychroma.com). In my free time I like to hike, play bad music, cook decent food, see my friends, and lift weights.

# About this website

I built this website myself, including most of the components needed to generate it (layouts, styling, HTML templating, ssg[1]). This was scary for me since I had never done web development work before. But it was fun! All the code and config are on [github](https://github.com/beggers/beneggers.com).

I thought it would be fun to make this an "upside-down" website. The entire website has no paths (things that come after the `/`, for example the `about` in `beneggers.com/about`). Instead, it relies on subdomains to represent different pages: a page that would normally be called `beneggers.com/posts/some-post` is instead called `some-post.posts.beneggers.com`. This introduced a lot of headaches for no benefit whatsoever; I plan to write about it sometime.

# Accessibility

I am committed to making this site accessible to anyone who wants to view it. If you have any suggestions for how I could do better, please email me at ben (at) beneggers (dot) com. I take this very seriously.

# Plagiarism

Many aspects of this site were inspired by, or stolen from, other people's work.

- The styling is inspired by the [Risotto](https://themes.gohugo.io/themes/risotto/) theme for [hugo](https://gohugo.io/) from the lovely [Joe Roe](https://joeroe.io/).
- The color scheme is [Solarized](https://ethanschoonover.com/solarized/).
- Most of the good ideas on this site can be traced back to my former colleagues.

[1] I did use a [Markdown parser](https://pypi.org/project/Markdown/).