function logout() {
    $.get("/user/logout", function(data){
        if (200 == data.code) {
            location.href = "/user/login/";
            console.log(1)
        }
    })
}

$(document).ready(function(){

    $.ajax({
        url:'/user/user_info/',
        type:'GET',
        dataType:'json',
        success:function(data){
            console.log(data)
            console.log(data.data.name)
            if(data.code == '200'){
            $('#user-name').text(data.data.name)
            $('#user-mobile').text(data.data.phone)
            $('#user-avatar').attr('src', '/static/media/' + data.data.avatar)
            }
        }


})

})