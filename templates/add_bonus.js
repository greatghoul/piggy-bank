(function() {
    $('#bonus-list').prepend('{% filter escapejs %}{% include '_bonus.html' %}{% endfilter %}');
})();
