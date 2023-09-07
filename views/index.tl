<!-- We only have the index page, so it's fine to have everything hardcoded.
     In the future I should perhaps separate things out properly. -->
<!DOCTYPE html>
<html>
    <head>
        <title>Ben Eggers dot com</title>
        <link rel="icon" type="image/x-icon" href="/favicon.ico">
        <style> 
            :root {
                --base03: #002b36;
                --base02: #073642;
                --base01: #586e75;
                --base00: #657b83;
                --base0: #839496;
                --base1: #93a1a1;
                --base2: #eee8d5;
                --base3: #fdf6e3;
                --yellow: #b58900;
                --orange: #cb4b16;
                --red: #dc322f;
                --magenta: #d33682;
                --violet: #6c71c4;
                --blue: #268bd2;
                --cyan: #2aa198;
                --green: #859900;
            }
            body {
                background: var(--base02);
            }
            pre {
                border-radius: 1em;
                padding: 1em;
                position: absolute;
                top: 50%;
                left: 50%;
                margin-right: -50%;
                transform: translate(-50%, -50%);
            }
            .grass {
                color: var(--base1);
            }
        </style>
    </head>
    <body>
        <pre class="grass">
            ${d.art}
        </pre>
    </body>
</html>