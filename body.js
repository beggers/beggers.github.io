// This is ugly. This function returns an HTML <body> formatted as a string.
// It contains all the formatting needed to correctly display characters and colors,
// e.g. grass is wrappde with <span class="grass"></span>. The CSS classes
// themselves are defined in index.tl 🤢
export const get_body = function() {
  return (
`
<body>
    <pre class="grass">
  __________________ 
< ben eggers dot com >
  ------------------ 
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||
    </pre>
</body>
`
  )
}