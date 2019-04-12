$(document).ready(function(){

        var WEBSOCKET_ROUTE = ":8888/ws";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://172.27.8.228" + WEBSOCKET_ROUTE);
	    console.log("http case");
            }
        else if(window.location.protocol == "https:"){
            //Dataplicity
	    console.log("in the https state");
            var ws = new WebSocket("wss://172.27.8.228" + WEBSOCKET_ROUTE);
            }

        ws.onopen = function(evt) {
            $("#ws-status").html("Connected");
            };

        ws.onmessage = function(evt) {
            };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected");
            };

        $("#green_on").click(function(){
            ws.send("on_g");
            });

        $("#green_off").click(function(){
            ws.send("off_g");
            });

        $("#red_on").click(function(){
            ws.send("on_r");
            });

        $("#red_off").click(function(){
            ws.send("off_r");
            });

      });
