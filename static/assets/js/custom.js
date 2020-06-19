$(function () {

    var heroCarousel = $("#heroCarousel");
    var heroCarouselIndicators = $("#hero-carousel-indicators");
    heroCarousel.find(".carousel-inner").children(".carousel-item").each(function (index) {
        (index === 0) ?
        heroCarouselIndicators.append("<li data-target='#heroCarousel' data-slide-to='" + index + "' class='active'></li>"):
            heroCarouselIndicators.append("<li data-target='#heroCarousel' data-slide-to='" + index + "'></li>");
    });

    heroCarousel.on('slid.bs.carousel', function (e) {
        $(this).find('h2').addClass('animated fadeInDown');
        $(this).find('p').addClass('animated fadeInUp');
        $(this).find('.btn-get-started').addClass('animated fadeInUp');
    });



    //insta_slider

    $('.insta_slider').slick({
        slidesToShow: 5,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 1500,
        arrows: false,
        button: false,
        speed: 2000,
        dots: false,
        responsive: [
            {
                breakpoint: 481,
                settings: {
                    slidesToShow: 1,
                    centerMode: false,
                    centerPadding: 0,
                }
    },
            {
                breakpoint: 321,
                settings: {
                    slidesToShow: 1,
                }
    },
            {
                breakpoint: 769,
                settings: {
                    slidesToShow: 2,
                    centerMode: false,
                    centerPadding: 0,
                }
    },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                }
    }

  ]
    });
    
        //movie_double_slider

    $('.movie_double_slider').slick({
        slidesToShow: 2,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 2500,
        arrows: false,
        button: false,
        speed: 3000,
        dots: true,
        responsive: [
            {
                breakpoint: 481,
                settings: {
                    slidesToShow: 1,
                    centerMode: false,
                    centerPadding: 0,
                }
    },
            {
                breakpoint: 321,
                settings: {
                    slidesToShow: 1,
                }
    },
            {
                breakpoint: 769,
                settings: {
                    slidesToShow: 2,
                    centerMode: false,
                    centerPadding: 0,
                }
    },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                }
    }

  ]
    });


    const toggles = document.querySelectorAll('.faq-toggle');

    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            toggle.parentNode.classList.toggle('active');
        });
    });

    // SOCIAL PANEL JS
    const floating_btn = document.querySelector('.floating-btn');
    const close_btn = document.querySelector('.close-btn');
    const social_panel_container = document.querySelector('.social-panel-container');

    floating_btn.addEventListener('click', () => {
        social_panel_container.classList.toggle('visible')
    });

    close_btn.addEventListener('click', () => {
        social_panel_container.classList.remove('visible')
    });
});
