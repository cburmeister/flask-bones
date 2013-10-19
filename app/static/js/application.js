$(function() {
    $('.alert').alert()

    $(document).pjax('a[data-pjax]', '#pjax-container');

    $(document).on('click', 'a[data-confirm], button[data-confirm]', function(event) {
        event.preventDefault();
        var $el = $(this);

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
