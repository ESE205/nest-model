$(document).ready(function(){

        var WEBSOCKET_ROUTE = ":8888/ws";
	var piIP3 = "172.27.8.108";
//	read piIP3;
	var piIP0 = "172.27.178.159";

        if(window.location.protocol == "http:"){
            //localhost
            var ws = new WebSocket("ws://" + piIP0 +  WEBSOCKET_ROUTE);
	    console.log("http case");
            }
        else if(window.location.protocol == "https:"){
            //Dataplicity
	    console.log("in the https state");
            var ws = new WebSocket("wss://" + piIP0 + WEBSOCKET_ROUTE);
            }

        ws.onopen = function(evt) {
            $("#ws-status").html("Connected");
            };

        ws.onmessage = function(evt) {
	    //console.log(evt.data);
	    if(evt.data.includes("LUM")){
		$("#lumin").html(parseInt(evt.data,10));
	    }
	    if(evt.data.includes("TEMP")){
		$("#temp").html((parseInt(evt.data,10)));
	    }
	    //$("#message").html(evt.data);
            };

        ws.onclose = function(evt) {
            $("#ws-status").html("Disconnected. If you were unable to connect, please restart your outlet.");
            };

        /*$("#outlet2_on").click(function(){
            ws.send("on_outlet2");
	    if(ws.readyState === ws.OPEN){
        	    $("#outlet2-status").html("OUTLET ON");
	    }
            });

        $("#outlet2_off").click(function(){
            ws.send("off_outlet2");
            $("#outlet2-status").html("OUTLET OFF");
            });*/

        $("#outlet1_on").click(function(){
            ws.send("on_outlet1");
	    if(ws.readyState === ws.OPEN){
        	    $("#outlet1-status").html("OUTLET ON");
	    }
            });

        $("#outlet1_off").click(function(){
            ws.send("off_outlet1");
            $("#outlet1-status").html("OUTLET OFF");
            });

        $("#check_lumin").click(function(){
            ws.send("refresh_lum");
            });

        $("#check_tem").click(function(){
            ws.send("refresh_temp");
            });

      });
