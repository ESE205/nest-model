<?php
	//html framework
	function head($title){
		echo"
			<html>
				<head>
					<link href='https://fonts.googleapis.com/css?family=Roboto+Condensed' rel='stylesheet'>
					<link href='https://fonts.googleapis.com/css?family=Roboto+Mono' rel='stylesheet'>
					<title>$title</title>
					<link rel='stylesheet' href='style.css'>
				</head>
				<body>
		";
		// navbar();
	}
	function navbar($things){		//can only accommodate exactly 5 things besides home rn, figure out style adjustments
		echo"
		<ul class='navbar'>";
		foreach($things as $thing){
			if ($thing != 'Contact/Links'){
				echo"
					<li><a href='#$thing'>$thing</a></li>
				";
			}
		}
		echo"<li><a style='color: red'href='#Contact/Links'>Contact/Links</a></li>
		</ul>
		";
	}
	function foot(){
		echo 		"<script src='/js/jquery.js'></script>
					<script src='/js/jsfunctions.js'></script>
				</body>
			</html>
		";
    }
    function home(){
        echo"
            <a href='/index.php' style='bottom:5; position:absolute'>home</a>
        ";
	}
	function loginLink($bottom = "auto"){
		echo"<div style='bottom:".$bottom.", position:sticky'>
				<h3>Returning User?</h3>
				<a href='/login.php'>Log In</a><br><br><br>
			</div>
		";
	}
	function signupLink($bottom = "auto"){
		echo"<div style='bottom:".$bottom.", position:sticky'>
				<h3>Don't have an account?</h3>
				<a href='/signup.php'>Sign Up</a>
			</div>
		";
	}