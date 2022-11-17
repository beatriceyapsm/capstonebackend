const express = require("express");
const api = require("./api");
//const authdemo = require("./authdemo");
const body_parser = require("body-parser");
const cors = require("cors");

let app=express();
//app.use(express.json());

app.use(cors());
app.use(body_parser.json());
app.use(api.router);//ask app to use router
//app.use(authdemo.router);

app.get('/', (req,res) => {
    res.send("Hello World");});

app.post("/readPython", (request, response) => {
    // Reading Python files
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python3', ['app.py', "hi", "Duyen"]);
  
       // collect data from script
    python.stdout.on('data', function (data) {
    dataToSend = data.toString();
    });
  
    python.stderr.on('data', data => {
    console.error(`stderr: ${data}`);
    });
  
       // in close event we are sure that stream from child process is closed
    python.on('exit', (code) => {
    console.log(`child process exited with code ${code}, ${dataToSend}`);
    response.sendFile(`${__dirname}/public/result.html`);
    }); 
  });


app.listen(process.env.PORT || 3000, (error)=> {
    if (error) {
        console.log(error);
        process.exit(0);
    } else {
        console.log("Server started at port:3000");
    }
});