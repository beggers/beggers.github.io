<!-- We only have the index page, so it's fine to have everything hardcoded.
     In the future I should perhaps separate things out properly. -->
<!DOCTYPE html>
<html>
  <head>
    <title>Ben Eggers dot com</title>
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <style>
      body {
        background: grey;
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
    </style>
  </head>
  <body>
    <pre>
        ${d.art}
    </pre>
  </body>
</html>