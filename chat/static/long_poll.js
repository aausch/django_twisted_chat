//Numeric representation of the last time we received a message from the server
lastupdate = -1;
 
$(document).ready(function(){

    getData();
 
    var inputBox = document.getElementById("inputbox");
 
    inputbox.addEventListener("keydown", function(e) {
      if (!e) { var e = window.event; }
 
      if (e.keyCode == 13) { 
        e.preventDefault(); // sometimes useful
        postData(inputbox.value);  
        inputbox.value="";
      }
    }, false);
 
});
 
var getData = function() {
    $.ajax({
        type: "GET",
        // set the destination for the query
        url: 'http://127.0.0.1:1025?lastupdate='+lastupdate,
        dataType: 'jsonp',
        // needs to be set to true to avoid browser loading icons
        async: true,
        cache: false,
        timeout:1000,
        // process a successful response
        success: function(response) {
            // append the message list with the new message
            var message = response.data;
            $("#message_list ul").prepend($('<li>'+message+'</li>'));
            // set lastupdate
            lastupdate = response.timestamp;
        },
        complete: getData,
        error: function(err) {
            if (err.statusText !== "timeout") 
                console.log("unexpected error: " + err);
        },
    });
};
 
var postData = function(data) {
   $.ajax({
        type: "POST",
        // set the destination for the query
        url: 'http://127.0.0.1:1025?lastupdate='+lastupdate,
        data: {new_message: data},
        // needs to be set to true to avoid browser loading icons
        async: true,
        cache: false,
   });
}
