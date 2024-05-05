function start_game() {
    send_request("start")
}

function play_round() {
    send_request("play_round")
    const chkbox = document.querySelector('#autoadvance');
    if (chkbox.checked) {
        const delay = document.querySelector('#delay');
        setTimeout(judge_round, delay.value * 1000)        
    }    
}

function judge_round() {
    send_request("judge_round")
    const chkbox = document.querySelector('#autoadvance');
    if (chkbox.checked) {
        const delay = document.querySelector('#delay');
        setTimeout(end_round, delay.value * 1000)        
    }    
}

function end_round() {
    send_request("end_round")
}

function toggle_autoadvance() {
    const chkbox = document.querySelector('#autoadvance');
    document.querySelector('#judge-round').disabled = chkbox.checked;
    document.querySelector('#end-round').disabled = chkbox.checked;
    document.querySelector('#delay').disabled = !chkbox.checked;
}

function log(status) {
    const div = document.querySelector('#statusDiv');
    const d = document.createElement('div');
    d.style.margin="10px"
    d.innerHTML = status;
    div.prepend(d);
}

function clear_log() {
    const div = document.querySelector('#statusDiv');
    div.innerHTML = "";
}

function send_request(request) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        try {
            var resp = JSON.parse(this.response)
   
            if (resp.hasOwnProperty('status')) {
                if (resp["status"] == "ok") {
                    if (resp.hasOwnProperty("message")) {
                        log(resp["message"])
                    } 
                    else {
                        resp["results"].forEach((element) => log(element)); 
                    }
                }
                else {
                    console.log("Error received: " + this.response);
                }
            }
            else {
                console.log("Bad response received: " + this.response);
            }
        } catch (error) {
            console.log("Bad response received. Could not parse: " + this.response + "," + error);
        }
      }
    };
    xhttp.responsType = 'json'
    xhttp.open("POST", "/admin", true);
    message = '{"action": "' + request +     '"}'
    xhttp.send(message);
    
}

function poll_for_update() {
    send_request("server_update")
}

var intervalId = window.setInterval(poll_for_update, 100);