$(function() {
    var BONUS_PATTERN = /^#(\S+)\s+(.+?)\s+(-?\d+)$/g;

    function insertBonus(bonus) {
        $.ajax({
            url: url_for('bonus'),
            data: bonus,
            type: 'POST',
            dataType: 'script'
        });
    }

    function parseBonus(text) {
        return text.match(BONUS_PATTERN) && { label: RegExp.$1, content: RegExp.$2, bonus: RegExp.$3 }
    }

    $('#input-bonus').keypress(function(e) {
        if (e.which != 13) return;

        var bonus = parseBonus($.trim(this.value));
        bonus && insertBonus(bonus);
    });
});
