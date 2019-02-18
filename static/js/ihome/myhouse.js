$(document).ready(function(){
    $.ajax({
        url:'/house/house_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            if (data.code == 1001){
                $('#houses-list').hide();
                $(".auth-warn").show();
            }

            if (data.code == 200){
                $('#houses-list').show();
                console.log(data.data.length)
                for(i=0;i<data.data.length;i++){

                node = '<li><a href="'+ '/house/detail/?id=' + data.data[i].id + '"><div class="house-title"><h3>房屋ID:' + data.data[i].id + '——' + data.data[i].title + '</h3></div><div class="house-content"><img src="' + '/static/media/' + data.data[i].image + '">' + '<div class="house-text"><ul><li>位于：' + data.data[i].area + '</li><li>价格：' + '￥' + data.data[i].price + '/晚</li><li>发布时间：' + data.data[i].create_time + '</li></ul></div> </div></a></li>'
                $('#houses-list').append(node)
                }
                $(".auth-warn").hide();
            }
        }
    })



})