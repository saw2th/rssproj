
$(document).ready(function(){
    // flag an rss item
    $(".flag").click(function(){
        var button = $(this);
        $.ajax({
            url: "/flag_item/" + $(this).data('itemid') + "/",
            method: "POST",
            headers: {'X-CSRFToken': $(this).data('csrf')}
        }).done(function(response) {
            button.text('Flagged');
        }).fail(function (error) {
            console.log(error);
        });
    });

});
