(function( $ ){

    $.fn.load_delegates = function(entity_id) {
        $.get('/entity/'+entity_id+'/list_delegates/',
            function (html) {
                $('#delegates-list').html(html);
                $('form.change-owner-form').submit($.fn.change_owner);
            }
        );
    };

    $.fn.select_first_user = function() {
        var q = $('input#q').val();
        $.getJSON('/accounts/search_users_auto/?term='+q,
            function (resp) {
                for (i in resp) {
                    if (resp[i]["value"] == q) {
                        $.fn.add_selected_delegate();
                        $('button#add-delegate').attr('disabled', true);
                        return;
                    }
                }
                $('input#q').val(resp[0]["value"]);
                $('#q').autocomplete("close");
                $('button#add-delegate').attr('disabled', false);
            }
        );
        return false;
    };

    $.fn.remove_delegate = function(entity_id, user_id) {
        $.get('/entity/'+entity_id+'/remove_delegate/'+user_id,
            function (html) {
                $('div#delegates-list').html(html);
                $('form.change-owner-form').submit($.fn.change_owner);
            }
        );
        return false;
    };

    $.fn.add_selected_delegate = function() {
        var entity_id = $('input#entity_id').val()
        var username = $('input#q').val()
        $.get('/entity/'+entity_id+'/add_delegate/'+username,
            function (html) {
                if (html == 'delegate') {
                    $.fn.team_perm_message(username+' can already edit this entity');
                } else if (html == 'owner') {
                    $.fn.team_perm_message(username+' is the owner this entity');
                } else {
                    $('div#delegates-list').html(html);
                    $('button#add-delegate').attr('disabled', true);
                    $('form.change-owner-form').submit($.fn.change_owner);
                }
            }
        );
        return false;
    };

    $.fn.enable_add_delegate = function () {
        $('button#add-delegate').attr('disabled', false);
    };

    $.fn.disable_add_delegate = function (event) {
        if (event.keyCode != 13) {
            $('button#add-delegate').attr('disabled', true);
        }
    };

    $.fn.change_owner = function () {
        if (confirm('Only the owner can edit the team permissions of an entity,\n'+
                   'and there can be only one owner for each entity.\n'+
                   'Therefore, you will not be able to undo this action.\n\n'+
                   'Do you confirm that you want to hand over the ownership of this entity? ')) {
            return true;
        } else {
            return false;
        }
    };

    $.fn.team_perm_message = function (msg) {
        $('ul#messages').html('<li>'+msg+'</li>')
                        .fadeIn()
                        .delay(3000)
                        .fadeOut();
    }

})( jQuery );
