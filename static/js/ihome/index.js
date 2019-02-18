//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/user/search/?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    url += "&";
    url += ("sk=" + 'new');
    location.href = url;
}

$(document).ready(function(){
    $(".top-bar>.register-login").show();


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.ajax({
        url:'/user/house_sourse/',
        dataType:'json',
        type:'GET',
        success:function(data){
        console.log(data)
            if(data.username){
                $('.user-info').show()
                $('.register-login').hide()
                $('.user-name').html(data.username)
            }else{
                $('.user-info').hide()
                $('.register-login').show()
            };
            for (i=0;i<data.data.length;i++){
            node=''
            node += '<div class="swiper-slide">'
            node += '<a href="'+ '/house/detail/?id=' + data.data[i].id + '">'
            node += '<img src="' + '/static/media/' + data.data[i].image +'"></a>'
            node += '<div class="slide-title">' + data.data[i].title + '</div>'
            node += '</div>'
            $('.swiper-wrapper').append(node);

            var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationClickable: true
    });
          }
        }
    });


        $.ajax({
        url:'/house/newhouse_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            console.log(data.data.length)
            for(i=0; i<data.data.length;i++){
                node = '<a href="#" area-id="'+ data.data[i].id +'">'+ data.data[i].name +'</a>'
                $('.area-list').append(node)

            };
            $(".area-list a").click(function(e){
                $("#area-btn").html($(this).html());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");
            });
        }
    });

})