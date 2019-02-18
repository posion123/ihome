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

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    $.ajax({
        url:'/order/my_order/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            for(i=0;i<data.data.length;i++){
            node = ''
            node += '<li order-id='+ data.data[i].order_id +'>'
               node += '<div class="order-title">'
                  node += '<h3>订单编号：' + data.data[i].order_id + '</h3>'
                    node += '<div class="fr order-operate" id="' + 'my_comment' + data.data[i].order_id +'">'
                       node += '<button type="button" class="btn btn-success order-comment" data-toggle="modal" data-target="#comment-modal">发表评价</button>'
                        node += '</div>'
                    node +='</div>'
                    node +='<div class="order-content">'
                        node +='<img src="' + '/static/media/' +data.data[i].image + '">'
                        node +='<div class="order-text">'
                            node +='<h3 id="'+ 'zhl_' + data.data[i].order_id + '">订单</h3>'
                            node +='<ul>'
                                node +='<li>创建日期：' + data.data[i].create_date +'</li>'
                                node +='<li>入住日期：' + data.data[i].begin_date +'</li>'
                                node +='<li>离开日期：' + data.data[i].end_date +'</li>'
                                node +='<li>合计金额：' + data.data[i].amount + '元' + '(共' + data.data[i].days +'晚)</li>'
                                node +='<li>订单状态：<span id="' + 'zhl' + data.data[i].order_id +'">已拒单</span></li><li id="' + 'zhl_comment_' + data.data[i].order_id +'" >我的评价：' + data.data[i].comment + '</li></ul></div></div></li> '
            $('.orders-list').append(node);
            var zhl_id = '#zhl_' + data.data[i].order_id
            console.log(zhl_id)
            $(''+ zhl_id + '').text(data.data[i].house_title)
            var span_id = '#zhl' + data.data[i].order_id
            if (data.data[i].status == 'WAIT_ACCEPT'){
                $('.order-text ul li '+ span_id +'').text('待接单')
            };
            if (data.data[i].status == "WAIT_PAYMENT"){
                $('.order-text ul li '+ span_id +'').text('待支付')
            };

            if (data.data[i].status == "PAID"){
                $('.order-text ul li '+ span_id +'').text('已支付')
            };

            var my_id = '#my_comment' + data.data[i].order_id
            if (data.data[i].status != "PAID"){
                $('' + my_id + '').hide()
            };

            if (data.data[i].status == 'WAIT_COMMENT'){
                $('.order-text ul li '+ span_id +'').text('待评价')
            };

            if (data.data[i].status == 'COMPLETE'){
                $('.order-text ul li '+ span_id +'').text('已完成')
            };

            if (data.data[i].status == 'CANCELED'){
                $('.order-text ul li '+ span_id +'').text('以取消')
            };

            if (data.data[i].status == 'REJECTED'){
                $('.order-text ul li '+ span_id +'').text('已拒单')
            };

            var comment_id = '#zhl_comment_' + data.data[i].order_id
            console.log(comment_id)
            if(data.data[i].comment == null){
                 $('.order-text ul '+ comment_id +'').text('我的评价: 未评价')
            }

            }

        $(".order-comment").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
        $(".modal-comment").attr("order-id", orderId);
        console.log(orderId)
    });

        }

    })

});

$('.modal-comment').click(function(){
                    var id =$(".modal-comment").attr("order-id");
                    var  client_comment = $('#comment').val()
                    console.log(client_comment)
                    $.ajax({
                        url:'/order/my_comment/',
                        dataType:'json',
                        type:'PATCH',
                        data:{'id':id, 'client_comment':client_comment},
                        success:function(data){
                            if (data.code == 200){
                                location.href = '/order/orders/'
                            }
                        }
                    })
               })