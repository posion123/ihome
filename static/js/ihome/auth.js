function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(document).ready(function(){
       $('#form-auth').submit(function(e){
            e.preventDefault();
            var name = $('#real-name').val()
            var card = $('#id-card').val()
            console.log(name)
            console.log(card)

            $.ajax({
            url:'/user/auth/',
            dataType:'json',
            type:'PATCH',
            data: {'real_name': name, 'id_card': card},
            success:function(data){
                console.log(data)
                if (data.code == '1001'){
                    $('.error-msg i ').text(data.msg)
                    $('.error-msg').show()
                }
                if (data.code == '1002'){
                    $('.error-msg i ').text(data.msg)
                    $('.error-msg').show()
                }

                if (data.code == '200'){
                    location.href = '/user/my/'
                }
            }
           });

        });
    function info(){
                $.ajax({
             url:'/user/info/',
             dataType:'json',
             type:'GET',
             success:function(data){
                if (data.code == 200){
                    $('#real-name').val(data.data.id_name)
                    $('#real-name').attr('disabled',true)
                    $('#id-card').val(data.data.id_card)
                    $('#id-card').attr('disabled',true)
                    $('.btn-success').hide()
                }
             }
        })
    }

    info()

    })

