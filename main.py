from spotify import Spotify

from bottle import route, run, request, get, post
import webbrowser

if __name__ == '__main__':
    s = Spotify()
    port = s.port
    webbrowser.open_new_tab("http://localhost:" + str(port))    

    @route('/')

    def index():
        if s.checkTokenFile() is True:
            return "<p>Token is valid</p>" + searchForm()
        else :
            return '<body onLoad="javascript:window.location.replace(\'' + s.auth() + '\');"></body>'

    @route('/tokenize')
    @route('/tokenize/')

    def tokenize():
        try :
            code = request.query['code']
            if code is not None:
                if s.getTokens(code) is True:
                    return "<p>Authorization successful</p>" + searchForm()
            else :
                return "Code is not provided"
        except :
            return "No request found"


    @route('/search')
    @route('/search/')

    def searchForm(val = "Search term"):
        formjs = "<script>function doSearch() { let s = document.getElementById('q').value; let url = 'http://localhost:" + str(port) + "/search/' + s; window.location.replace(url); } </script>"
        formhtml = '<input name="q" placeholder="' + val + '" type="text" id="q"> <input type="button" value="Search" name="search" id="search" onClick="javascript:doSearch();"><hr>'
        formenterjs = "<script>document.getElementById('q').addEventListener('keyup', function(event) { if (event.keyCode === 13) { doSearch(); } }); </script>"
        if s.checkTokenFile() is True:
            return formjs + formhtml + formenterjs
        else :
            return '<body onLoad="javascript:window.location.replace(\'' + s.auth() + '\');"></body>'


    @route('/search/<q>')

    def search(q):
        if s.checkTokenFile() is False:
            return '<body onLoad="javascript:window.location.replace(\'' + s.auth() + '\');"></body>'
        try :
            if q is not None:
                sr = s.search(q)
                if sr is not None:
                    res = "<ul>"
                    for i in sr:
                        m = ' - '.join(i)
                        res += '<li>' + m + '</li>'
                    res += "</ul>"
                    return searchForm(q) + res
                else :
                    return "<p>No results</p>" + searchForm(q)
            else :
                return "<p>No query provided</p>" + searchForm() 
        except :
            return "<p>No request found</p>" + searchForm()

    run(host='localhost', port=port)

