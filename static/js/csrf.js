(function (window) {
    function getQueryVariable(variable) {
        var query = window.location.search.substring(1);
        var vars = query.split("&");
        for (var i = 0; i < vars.length; i++) {
            var pair = vars[i].split("=");
            if (pair[0] == variable) {
                return pair[1];
            }
        }
        return (false);
    }

    //防token盗用
    if (getQueryVariable('token') != sessionStorage.getItem('token')) {
        window.location = '/'
    }
})(this);