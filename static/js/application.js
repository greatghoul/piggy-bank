$(function() {
    var BONUS_PATTERN = /^#(\S+)\s+(.+?)\s+(-?\d+)$/g;
    var TARGET_PATTERN = /^(.+?)\s+(-?\d+)$/g;

    function parseTarget(text) {
        return text.match(TARGET_PATTERN) && { name: RegExp.$1, price: RegExp.$2 }
    }

    function insertTarget(target) {
        $.ajax({
            url: url_for('target'),
            data: target,
            type: 'POST',
            dataType: 'script'
        });
    }

    function parseBonus(text) {
        return text.match(BONUS_PATTERN) && { label: RegExp.$1, content: RegExp.$2, bonus: RegExp.$3 }
    }

    function insertBonus(bonus) {
        $.ajax({
            url: url_for('bonus'),
            data: bonus,
            type: 'POST',
            dataType: 'script'
        });
    }

    $('#input-bonus').keypress(function(e) {
        if (e.which != 13) return;

        var bonus = parseBonus($.trim(this.value));
        bonus && insertBonus(bonus);
    });

    $('#input-target').keypress(function(e) {
        if (e.which != 13) return;

        var target = parseTarget($.trim(this.value));
        target && insertTarget(target);
    });
});
