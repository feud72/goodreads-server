$(document).ready(function() {
	$('.responsive').slick({
		dots: true,
		arrows: true,
		infinite: true,
		speed: 500,
		slidesToShow: 5,
		slidesToScroll: 5,
		autoplay: true,
		autoplaySpeed: 8000,
		responsive: [
			{
				breakpoint: 1440,
				settings: {
					slidesToShow: 4,
					slidesToScroll: 4,
				},
			},
			{
				breakpoint: 1200,
				settings: {
					slidesToShow: 3,
					slidesToScroll: 3,
				},
			},
			{
				breakpoint: 960,
				settings: {
					slidesToShow: 2,
					slidesToScroll: 2,
				},
			},
			{breakpoint: 720, settings: {slidesToShow: 1, 
					slidesToScroll: 1,
			}},
		],
	});
});
