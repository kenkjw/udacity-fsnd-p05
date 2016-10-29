$(document).ready(function() {
    $('.logout').click(function(){
        signOut();
    });
});

function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.disconnect();
    auth2.signOut().then(function () {
    });
}

