$(function () {
    
    
    // header slider js

$('.slider-img').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    dots: false,
    prevArrow: '.slidPrv',
    nextArrow: '.slidNext',
    arrows: true,
    autoplaySpeed: 5000,
    infinite: true,
    speed: 1000,
    fade: true,
    cssEase: 'linear',
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
