$(function() {
    $('.alert').alert()
    $(document).pjax('a[data-pjax]', '#pjax-container');

    $('a[data-confirm], button[data-confirm]').click( function(e) {
        var $el = $(this);
        e.preventDefault();

        bootbox.confirm($el.data('dialogue'), function(result) {
            if(result) {
                if($el.is('button')) {
                    $el.closest('form').submit();
                } else {
                    window.location.href = $el.attr('href');
                }
            }
        }); 
    });
});
