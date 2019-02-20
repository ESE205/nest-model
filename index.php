<?php  
    include("\include\include_all.php");
    head("Nest Model Home");
    if(isset($_POST['login'])){
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
    ";
    foot();