function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){


    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var address = location.search.split('=')[1]
        console.log(address)
        $.ajax({
            url:'/order/my_booking/' + address,
            dataType:'json',
            type:'GET',
            success:function(data){
                console.log(data)
                console.log(data.data.title)
                $('.house-text h3').text(data.data.title)
                $('.house-text p span').text(data.data.price)
                $('.house-info img').attr('src', '/static/media/' + data.data.image)

            }
        });


    $('.submit-btn').click(function(){
        var price = $('.house-text p span').text()
        var start_time = $('#start-date').val()
        var end_time = $('#end-date').val()
        var sd = new Date(start_time);
        var ed = new Date(end_time);
        var days = (ed - sd)/(1000*3600*24) + 1;
        var amount = days * parseFloat(price);
        $.ajax({
            url:'/order/booking/',
            dataType:'json',
            type:'POST',
            data:{'house_id':address, 'start_time':start_time, 'end_time':end_time, 'days':days, 'house_price':price, 'amount':amount},
            success:function(data){
                alert('成功')
            }
        })

    })
})
