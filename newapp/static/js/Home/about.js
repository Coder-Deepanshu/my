$(document).ready(function () {
    // Animate elements on scroll
    function animateElements() {
        $('.about-image, .about-content, .mv-card, .team-card, .story-card, .partner-logo').each(function () {
            var position = $(this).offset().top;
            var scroll = $(window).scrollTop();
            var windowHeight = $(window).height();

            if (scroll + windowHeight - 100 > position) {
                $(this).addClass('animate__animated animate__fadeInUp');
            }
        });
    }

    // Initialize animation
    animateElements();

    // Animate on scroll
    $(window).scroll(function () {
        animateElements();
    });
});