function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');

        $.ajax({
        url:'/house/newhouse_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            console.log(data.data.length)
            for(i=0; i<data.data.length;i++){

                $('#area-id').append('<option value="' + data.data[i].id + '">' + data.data[i].name + '</option>')
            }
        }
    });

            $.ajax({
        url:'/house/func_info/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            console.log(data.data.length)
            for(i=0; i<data.data.length;i++){

                node = '<li><div class="checkbox"><label><input type="checkbox" name="facility" value="'+ data.data[i].id +'">' + data.data[i].name + '</label></div></li>'
                $('.clearfix').append(node)
            }
        }
    });

       $('#form-house-info').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            type:'POST',
            dataType:'json',
            success:function(data){
                console.log(data)
                console.log(data.data)
                 if(data.code == 200){
                    $('#form-house-info').hide()
                    $('#house-id').val(data.data)
                    $('#form-house-image').show()

                 }
            },
            error:function(data){
                alert('失败')
            }
        });
    });


    $('#form-house-image').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/house/newhouse/',
            type:'PATCH',
            dataType:'json',
            success:function(data){
                    alert('成功')
            },
            error:function(data){
                alert('失败')
            }
        });
    });

})
