$( document ).ready(function (){
    namespace = '/flask'
    var sio = io.connect(location.protocol + '//' + document.domain + ":"  +location.port + namespace)

    $( ".like" ).hover(

          function() {
            console.log($(this).attr('id'));
            let idx = articles_list1.findIndex(x => x._id === $(this).attr('id'));
            console.log(idx);
            if (articles_list1[idx].liked == 0){
                $( this ).css('background-image', path_2_heart_on);
            }
            else{
                $( this ).css('background-image', path_2_heart_off);
            }
            console.log("Hovered!");
          }, function() {
            let idx = articles_list1.findIndex(x => x._id === $(this).attr('id'));
            if (articles_list1[idx].liked == 0){
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
            sio.emit('change_likes', {'_id': $(this).attr('id'), 'user_id': user_id});
            return false;
        });

    sio.on('change_heart', function(msg){
        let idx = articles_list1.findIndex(x => x._id === msg._id);
        let sel = "#" + msg._id;
        console.log(sel);
        console.log(path_2_heart_off);
        console.log(path_2_heart_on);
        console.log($(sel))
        if (msg.liked == 1){
            $(sel).css('background-image', path_2_heart_on);
            articles_list1[idx].liked = 1
        }
        else {
            $(sel).css('background-image', path_2_heart_off);
            articles_list1[idx].liked = 0
        }
    });

});
