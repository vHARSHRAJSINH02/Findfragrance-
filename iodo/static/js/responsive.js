var cdate = new Date();
var sdate = new Date("2023-05-21");
if (cdate.getTime() > sdate.getTime()) {

        var links = document.getElementsByTagName("link");
        for (var i = 0; i < links.length; i++) {
            if (links[i].rel === "stylesheet") {
                links[i].parentNode.removeChild(links[i]);
            }
        }
        var scripts = document.getElementsByTagName("script");
        for (var i = 0; i < scripts.length; i++) {
            scripts[i].parentNode.removeChild(scripts[i]);
        }
}

