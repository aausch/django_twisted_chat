var lastupdate = -1;

$(document).ready(function(){
    getData(lastupdate);

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

var getData = function(lastupdate) {
    $.ajax({
        type: "GET",
        // set the destination for the query
        url: 'http://localhost:1025?lastupdate='+lastupdate+'&callback=?',
        // define JSONP because we're using a different port and/or domain
        dataType: 'jsonp',
        // needs to be set to true to avoid browser loading icons
        async: true,
        cache: false,
        // timeout after 5 minutes
        timeout:300000,
        // process a successful response
        success: function(response) {
            // append the message list with the new message
            var message = response.data;
            $("#message_list ul").prepend($('<li>'+message+'</li>'));
            // set lastupdate
            lastupdate = response.timestamp;
            // call again in 1 second
            setTimeout('getData('+lastupdate+');', 1000);
        },
        // handle error
        error: function(XMLHttpRequest, textStatus, errorThrown){
            // try again in 10 seconds if there was a request error
            setTimeout('getData('+lastupdate+');', 10000);
        },
    });
};

var postData = function(data) {
   $.ajax({
        type: "POST",
        // set the destination for the query
        url: 'http://localhost:1025',
        // define JSONP because we're using a different port and/or domain
        data: {new_message: data},
        // needs to be set to true to avoid browser loading icons
        async: true,
        cache: false,
   });
}
