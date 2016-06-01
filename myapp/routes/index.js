var express = require('express');
var router = express.Router();
var mysql = require('mysql');
var db_results;

var connection = mysql.createConnection({
	host : 'localhost',
	user : 'root',
	password : 'password',
	database: 'weatherdb'
});

connection.connect(function(err) {
	if (err) throw err
	console.log("Connected to MySQL databse");
	connection.query('SELECT * FROM boston', function(err, results){
		if (err) throw err
		db_results = results;
	})
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.json(db_results);
});

module.exports = router;
