function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    var address = location.search.split('=')[1]
    console.log(address)
    $.ajax({
        url:'/house/my_detail/' +address +'/',
        dataType:'json',
        type:'GET',
        success:function(data){
          console.log(data)
          console.log(data.data[0].images.length)
          for (i=0;i<data.data[0].images.length;i++){
          code = '<li class="swiper-slide"><img src="' + '/static/media/' +data.data[0].images[i] + '">' + '</li>'
          $('.swiper-wrapper').append(code)

        var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'

    })

          }
          console.log(data.data[2])
           $('.house-price span').text(data.data[0].price)
           $('.house-title').text(data.data[0].title)
           $('.landlord-pic img').attr('src', '/static/media/' + data.data[2])
           $('.landlord-name span').text(data.data[1])

            $(".book-house").attr('href', '/order/booking/?id=' + data.data[0].id);



        },
    });

    $(".book-house").show();
})