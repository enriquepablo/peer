(function($) {
    $(document).ready(function(){
        $("#accordion").accordion();
        var active = parseInt($("#active_fold").val(), 10);
        $('#accordion').accordion("activate", active);
    });
})(jQuery);
