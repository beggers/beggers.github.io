// Terrible, terrible stuff.
export const index = (body) => `
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
                background: var(--base03);
                border-radius: 1em;
                padding: 1em;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                position: absolute;
            }
            button {
                all: unset;
                background: var(--base03);
                color: var(--base0);
                left: 50%;
                transform: translate(-50%, +20%);
                position: relative;
            }
            button.pressed {
                color: var(--base01);
            }
            .animal {
                color: var(--base1);
            }
            .bubble {
                color: var(--base0);
            }
            .dialogue {
                color: var(--base1);
            }
            .grass {
                color: var(--green);
            }
            .fence {
                color: var(--base02);
            }
        </style>
    </head>
    ${body}
</html>
`;