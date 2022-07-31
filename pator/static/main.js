(function() {
      var swiper = new Swiper(".mySwiper", {
        slidesPerView: 1,
        spaceBetween: 20,
        breakpoints: {
          // when window width is <= 499px
          499: {
              slidesPerView: 2,
              spaceBetweenSlides: 50
          }
          },
      
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      });
        
})()


function showPopup(){
  document.querySelector(".popup").classList.add("active");
}

function closePopup(){
  document.querySelector(".popup").classList.remove("active");
}