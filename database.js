const mysql = require('mysql');
require('dotenv').config();

// setup database connection    
var properties = {
  connectionLimit: 10,
  password: process.env.DBPASSWD,
  user: process.env.DBUSER,
  database: process.env.DBNAME,
  host: process.env.DBHOST,
  port: process.env.DBPORT
};

var mysqlConnection = mysql.createConnection(properties);

mysqlConnection.connect((errors) => {
  if (errors) console.log("Error occurred while connecting to MySQL server");
  else console.log("Connected to MySQL successfully!");
});

module.exports = { mysqlConnection };