const express = require("express");
const bodyParser = require("body-parser");
var multer = require('multer');

const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const swaggerDocument = YAML.load('./swagger-generated.yaml');

var app = express();


var upload = multer();
// for parsing application/json

const cors = require('cors');
app.use(function (req, res, next) {
    res.header('Access-Control-Allow-Credentials', true);
    res.header('Access-Control-Allow-Origin', req.headers.origin);
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.header('Access-Control-Allow-Headers', 'X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept');
    if ('OPTIONS' == req.method) {
        res.sendStatus(200);
    } else {
        next();
    }

})

app.use(cors({
    origin: '*'
}));

app.use(express.urlencoded({extended: true}))
//form-urlencoded

// for parsing multipart/form-data
app.use(upload.array());

// simple route
app.get("/", (req, res) => {
  console.log(req.body);
  res.send("ok");
});

require("./app/routes/user.routes.js")(app);





//SWAGGER
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// set port, listen for requests
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
});
