$( document ).ready(function (){
    namespace = '/flask'
    var sio = io.connect(location.protocol + '//' + document.domain + ":"  +location.port + namespace)

    $( ".like" ).hover(

          function() {
            console.log($(this).attr('id'));
            if (article_obj1.liked == 0){
                $( this ).css('background-image', path_2_heart_on);
            }
            else{
                $( this ).css('background-image', path_2_heart_off);
            }
            console.log("Hovered!");
          }, function() {
            if (article_obj1.liked == 0){
                $( this ).css('background-image', path_2_heart_off);
            }
            else{
                $( this ).css('background-image', path_2_heart_on);
            }
            console.log("Left!");
          }
    );

    $(".like").on('click', function (){
            console.log("sio testing");
            sio.emit('change_likes', {'_id': article_obj1._id, 'user_id': user_id});
            return false;
        });

    sio.on('change_heart', function(msg){

        console.log($(".like"))
        if (msg.liked == 1){
            $(".like").css('background-image', path_2_heart_on);
            article_obj1.liked = 1
        }
        else {
            $(".like").css('background-image', path_2_heart_off);
            article_obj1.liked = 0
        }
    });

});
