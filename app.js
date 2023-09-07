const express = require("express");
const tl = require('express-tl')

const app = express();
const port = process.env.PORT || 3001;
app.engine('tl', tl);

app.use(express.static('public'))
app.set('views', './views');
app.set('view engine', 'tl');

app.get("/",
  (req, res) => res.render('index',
    {
      art: get_art()
    }
  )
);

app.listen(port, () => console.log(`Example app listening on port ${port}!`));

const get_art = function() {
  return (
`
  __________________ 
< ben eggers dot com >
  ------------------ 
        \\   ^__^
         \\  (oo)\\_______
            (__)\\       )\\/\\
                ||----w |
                ||     ||
`
  )
}