(function( $ ){

    $.fn.load_delegates = function(entity_id) {
        $.get('/entity/'+entity_id+'/list_delegates/',
            function (html) {
                $('#delegates-list').html(html);
            }
        );
    };

    $.fn.search_users = function() {
        $('#q').autocomplete('close');
        $('button#add-delegate').attr('disabled', true);
        var entity_id = $('input#entity_id').val()
        var q = $('input#q').val()
        $.get('/entity/'+entity_id+'/search_users/?q='+q,
            function (html) {
                $('div#searchusers-results').html(html);
            }
        );
        return false;
    };

    $.fn.remove_delegate = function(entity_id, user_id) {
        $.get('/entity/'+entity_id+'/remove_delegate/'+user_id,
            function (html) {
                $('div#delegates-list').html(html);
            }
        );
        return false;
    };

    $.fn.add_delegate = function(entity_id, username) {
        $.get('/entity/'+entity_id+'/add_delegate/'+username,
            function (html) {
                $('div#delegates-list').html(html);
                $('div#searchusers-results').html('');
            }
        );
        return false;
    };

    $.fn.add_selected_delegate = function() {
        var entity_id = $('input#entity_id').val()
        var username = $('input#q').val()
        $.get('/entity/'+entity_id+'/add_delegate/'+username,
            function (html) {
                $('div#delegates-list').html(html);
            }
        );
        return false;
    };

    $.fn.enable_add_delegate = function () {
        $('div#searchusers-results').html('');
        $('button#add-delegate').attr('disabled', false);
    };

    $.fn.disable_add_delegate = function () {
        $('button#add-delegate').attr('disabled', true);
    };

    $.fn.change_owner = function () {
        if (confirm('Change ownership for this entity?')) {
            return true;
        } else {
            return false;
        }
    };

})( jQuery );
