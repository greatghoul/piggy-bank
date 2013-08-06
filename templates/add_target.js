(function() {
    $('#target-list').prepend('{% filter escapejs %}{% include '_target.html' %}{% endfilter %}');
})();
