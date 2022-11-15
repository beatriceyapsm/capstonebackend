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

app.listen(process.env.PORT || 3000, (error)=> {
    if (error) {
        console.log(error);
        process.exit(0);
    } else {
        console.log("Server started at port:3000");
    }
});