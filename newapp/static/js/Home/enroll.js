$(document).ready(function () {
    // Form submission
    $('#enrollmentForm').submit(function (e) {
        e.preventDefault();

        // Basic validation
        let isValid = true;
        $('#enrollmentForm input:required, #enrollmentForm select:required').each(function () {
            if (!$(this).val()) {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        if (isValid) {
            // Show success modal
            $('#successModal').modal('show');

            // Reset form
            $('#enrollmentForm')[0].reset();
        }
    });

    // Animate elements on scroll
    function animateElements() {
        $('.benefit-card, .testimonial-card').each(function () {
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