import { get_body } from './body.js';
import express from 'express';
import tl from 'express-tl';

function main() {
  const app = express();
  const port = process.env.PORT || 3001;
  app.engine('tl', tl);

  app.use(express.static('public'))
  app.set('views', './views');
  app.set('view engine', 'tl');

  app.get("/",
    (req, res) => res.render('index',
      {
        body: get_body()
      }
    )
  );

  app.listen(port, () => console.log(`Example app listening on port ${port}!`));
}

main();