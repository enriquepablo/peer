(function($) {
    $(document).ready(function(){
        $("#accordion").accordion();
        var active = parseInt($("#active_fold").val());
        $('#accordion').accordion("activate", active);
    });
})(jQuery);
