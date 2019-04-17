<?php
    include(__DIR__."/include/include_all.php");
    head("Nest Model Outlet");
	echo"
		<div>
			<h2>OUTLET HOME</h2>
			<p>Here you can turn on/off the outlet, controlled by the Raspberry Pi.</p>";
			//Green: <p>
			//	<input type=\"button\" id=\"green_on\" value=\"ON\">
			//	<input type=\"button\" id=\"green_off\" value=\"OFF\">
			//</p>
	echo"
		Outlet: <p>
				<input type=\"button\" id=\"red_on\" value=\"ON\">
				<input type=\"button\" id=\"red_off\" value=\"OFF\">
			</p>
		</div>
		<hr> Websocket status: <br>
		<div id=\"ws-status\">
			Waiting...
		</div>
		<a href='index.php'>Back to Outlets</a>
		<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js\"></script>
		<script src=\"static/ws-client.js\">
	";
    /*if(isset($_POST['login'])){
        login();
    }
    if(isset($_POST['signup'])){
        signup();
    }
    echo"
        <h1>Nest Model Home</h1>

        <br>
        <div style='float:left; clear:left; width:40%; padding-left: 15%'>
            <h2>
                Welcome! You've made it to <br>
                the home page of the Nest Model <br>
                Project for ESE 205, Spring 2019. <br>
                Please log in to your account, <br>
                or create a new account if you <br>
                don't already have one.
            </h2>
        </div>
        <div style='float:right; clear:right; width:30%; padding-right: 10%; padding-top: 2%'>";
            loginLink();
            signupLink();
        echo"</div>
    ";*/
    foot();
