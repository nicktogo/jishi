$(document).ready(function () {
    var dropdown = $('.dropdown');

    // Add slidedown animation to dropdown
    dropdown.on('show.bs.dropdown', function (e) {
        $(this).find('.dropdown-menu').first().stop(true, true).slideDown();
        dropdown.addClass("open");
        $('.dropdown-toggle').attr("");
    });

    // Add slideup animation to dropdown
    dropdown.on('hide.bs.dropdown', function (e) {
        $(this).find('.dropdown-menu').first().stop(true, true).slideUp();
    });
});