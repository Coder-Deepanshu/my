$(document).ready(function () {
    // Animate elements on scroll
    function animateElements() {
        $('.benefit-card, .testimonial-card, .company-card').each(function () {
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

        // Animate stats counting
        $('.stat-number').each(function () {
            var position = $(this).offset().top;
            var scroll = $(window).scrollTop();
            var windowHeight = $(window).height();

            if (scroll + windowHeight - 150 > position && !$(this).hasClass('counted')) {
                $(this).addClass('counted');
                var $this = $(this);
                var countTo = $this.attr('data-count');
                $({ countNum: $this.text() }).animate({
                    countNum: countTo
                }, {
                    duration: 2000,
                    easing: 'swing',
                    step: function () {
                        $this.text(Math.floor(this.countNum));
                    },
                    complete: function () {
                        $this.text(this.countNum);
                    }
                });
            }
        });
    });
});