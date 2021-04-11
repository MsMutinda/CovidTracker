function send_value() {
    $.ajax({
             url: '',
             method : 'POST',
             data: {search_item: $('#filter-data').val()},
    });
}
}