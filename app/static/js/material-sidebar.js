$(document).ready(function () {
    var dropdown = $('.dropdown');

    // Add slidedown animation to dropdown
    dropdown.on('show.bs.dropdown', function (e) {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
    });

    // Add slideup animation to dropdown
    dropdown.on('hide.bs.dropdown', function (e) {
        alert("lalala");
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });
});

(function (removeClass) {

    jQuery.fn.removeClass = function (value) {
        if (value && typeof value.test === "function") {
            for (var i = 0, l = this.length; i < l; i++) {
                var elem = this[i];
                if (elem.nodeType === 1 && elem.className) {
                    var classNames = elem.className.split(/\s+/);

                    for (var n = classNames.length; n--;) {
                        if (value.test(classNames[n])) {
                            classNames.splice(n, 1);
                        }
                    }
                    elem.className = jQuery.trim(classNames.join(" "));
                }
            }
        } else {
            removeClass.call(this, value);
        }
        return this;
    }

})(jQuery.fn.removeClass);