$(document).ready(function () {
    // Animate elements on scroll
    function animateElements() {
        $('.feature-card, .testimonial-card').each(function () {
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

    // Add animation to carousel captions
    $('#mainCarousel').on('slide.bs.carousel', function (e) {
        var $next = $(e.relatedTarget);
        var nextIndex = $next.index();

        $next.find('.carousel-caption h2').removeClass().addClass('animate__animated').addClass('animate__fadeInDown');
        $next.find('.carousel-caption p').removeClass().addClass('animate__animated').addClass('animate__fadeInUp');
        $next.find('.carousel-caption a').removeClass().addClass('animate__animated').addClass('animate__fadeInUp');
    });
});