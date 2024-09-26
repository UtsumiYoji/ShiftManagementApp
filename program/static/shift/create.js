// Start making a shift
$('.make-calendar').on('click', function() {
    var start_datetime = $('#start_datetime').val();
    var end_datetime = $('#end_datetime').val();
    
    start_datetime = new Date(start_datetime);
    end_datetime = new Date(end_datetime);

    diff = (end_datetime - start_datetime) / (1000 * 60);
    count = diff / 30 + 1;
    
    datetimes = [];
    for (i = 0; i < count/2; i++) {
        datetimes.push(new Date(start_datetime.getTime() + (i * 60 * 60 * 1000)));
    }
    
    var element = '<table class="datetimes">\n<tbody>\n<tr>';
    datetimes.forEach(datetime => {
        element += '<td>' + datetime.getHours() + ':00</td>';
    });
    element += '\n</tr>\n</tbody>\n</table>';

    element += '<table class="shift overflow-x-scroll">\n<tbody>\n<tr>';
    element += '\n<td class="most-left-cell"><select class="work-locations">\n<option></option>';
    users.forEach(user => {
        element += '\n<option value="' + user.id + '">' + user.first_name + '</option>';
    });
    element += '\n</select></td>';

    count -= 1;
    for (var i = 0; i < count; i++) {
        datetime = new Date(start_datetime.getTime() + (i * 60 * 30 * 1000))
        element += '\n<td class="shift_cell" value="'+datetime+'" work_location_id=""></td>';
    }
    element += '\n</tr>\n</tbody>\n</table>';

    $('.calendar-container').append(element);
});

// adding a row
$(document).on('change', '.most-left-cell>select' , function() {
    // judge if it is the last row
    if (!($(this).closest('tr').is(':last-child'))) {
        return;
    }

    var row = this.closest('tr');
    var clone = row.cloneNode(true);
    row.parentNode.appendChild(clone);
});

function date_to_string(date) {
    return (date.getHours()+':'+date.getMinutes().toString().padStart(2, '0'))
}

function paint_out_cell(work_location_id=null) {
    // Retain datetimes
    var card = $('.shift_detail').first()
    var start_at = card.find('.start-at').attr('value');
    var finish_at = card.find('.finish-at').attr('value');

    // Retain color
    var color = card.find('option:selected').attr('color');

    // Paint out cells
    var tr = card.closest('tr');
    if (finish_at == "") {
        tr.find('td[value="'+start_at+'"]').css('background-color', color)
        return
    }

    var start_cell = tr.find('td[value="'+start_at+'"]');
    var finish_cell = tr.find('td[value="'+finish_at+'"]');
    start_cell.css('background-color', color);
    start_cell.nextUntil(finish_cell).css('background-color', color);

    // Save work location id
    if (work_location_id != null) {
        start_cell.attr('work_location_id', work_location_id);
        start_cell.nextUntil(finish_cell).attr('work_location_id', work_location_id);
    }
}

ADDING_BREAK_TEXT = 'Click calendar to add break or here to cancel';
WAITING_BREAK_TEXT = 'Add break time';

// clicking a cell
$(document).on('click', 'td.shift_cell', function() {
    // check if it alreday has a detail card
    if ($('.shift_detail').length == 1) {
        // If clicked row already has work_location_id(color)
        if ($(this).attr('work_location_id')) {
            // find start cell and finish cell
            var work_location_id = $(this).attr('work_location_id');
            var start_cell = $(this).next().prevUntil(
                '.shift_cell[work_location_id!="'+work_location_id+'"]'
            ).last();
            var finish_cell = $(this).prev().nextUntil(
                '.shift_cell[work_location_id!="'+work_location_id+'"]'
            ).last();

            // create time str
            var start_at = new Date(start_cell.attr('value'));
            var finish_at = new Date(finish_cell.attr('value'))
            finish_at.setMinutes(finish_at.getMinutes() + 30);

            // add card
            elm = $(".shift_detail").clone(true).appendTo(this);
            elm.find('.start-at').text(date_to_string(start_at));
            elm.find('.finish-at').text(date_to_string(finish_at));
            elm.find('.start-at').attr('value', start_at);
            elm.find('.finish-at').attr('value', finish_at);
            elm.find('h5').append('form ' + date_to_string(start_at) + ' to ' + date_to_string(finish_at));
            elm.find('select').val(work_location_id);
            elm.find('.work-location-color').css('color', elm.find('option:selected').attr('color'));

            return;
        }

        // show new detail card
        var datetime = new Date($(this).attr('value'));

        elm = $(".shift_detail").clone(true).appendTo(this);
        $(this).find('.start-at').attr('value', datetime);

        datetime = date_to_string(datetime);
        $(this).find('.start-at').text(datetime);
        elm.find('h5').append(datetime);
        
        paint_out_cell();
        
        // disable select and break button
        elm.find('.break').prop('disabled', true);
        $(".most-left-cell>select").prop('disabled', true);
        return;
    }

    // check clicked cell is same row with the detail card
    card = $('.shift_detail').first();
    var clicked_row = $(this).closest('tr');
    var detail_row = card.closest('tr');
    if (!(clicked_row[0] == detail_row[0])) {
        return;
    }

    // If user is making break time
    if (card.find('.break').text() == ADDING_BREAK_TEXT) {
        // Make sure user clicling cell which has work_location_id
        if ($(this).attr('work_location_id')) {
            // If cell is already painted out, it will become normal
            if ($(this).css('background-color') == 'rgb(255, 255, 0)') {
                var color = card.find('option:selected').attr('color');
                $(this).css('background-color', color);
            } else {
                // Paint out a cell
                $(this).css('background-color', 'yellow');
            }
        return;
        }
    }

    // If card alreday has finish time, it cannot be fixed
    if (card.find('.finish-at').attr('value') != "") {
        return;
    }

    // Retain datetimes
    var finish_at = new Date($(this).attr('value'));
    var start_at = new Date(card.closest('td').attr('value'));
    
    // If user clicked cell before start time cell
    if (finish_at < start_at) {
        var tmp = finish_at;
        finish_at = start_at;
        start_at = tmp;
        card.find('.start-at').text(date_to_string(start_at));
        card.find('.start-at').attr('value', start_at);
    }
    finish_at.setMinutes(finish_at.getMinutes() + 30);
    card.find('h5').text("You're selecting from ");
    card.find('h5').append(card.find('.start-at').text() + ' to ' + date_to_string(finish_at));
    card.find('.finish-at').text(date_to_string(finish_at));
    card.find('.finish-at').attr('value', finish_at);
    var work_location_id = card.find('.work-location').find('option:selected').val();
    paint_out_cell(work_location_id);
    elm.find('.break').prop('disabled', false);
});

// clicking a detial card
$(document).on('click', '.shift_detail', function(event) {
    event.stopPropagation();
});

// selecting a work location
$(document).on('change', '.work-location', function() {
    var color = $(this).find('option:selected').attr('color');
    var work_location_id = $(this).find('option:selected').val();
    $(this).closest('.shift_detail').find('.work-location-color').css('color',color);
    paint_out_cell(work_location_id);    
});

// clicking break
$(document).on('click', '.break', function() {
    if ($(this).text() == ADDING_BREAK_TEXT) {
        $(this).text(WAITING_BREAK_TEXT);
    } else {
        $(this).text(ADDING_BREAK_TEXT);
    }
});

// clicking save
$(document).on('click', '.save', function() {
    $(this).closest('.shift_detail').remove();

    // enable select
    $(".most-left-cell>select").prop('disabled', false);
});

// clicking delete
$(document).on('click', '.delete', function() {
    // Retain datetimes
    var card = $('.shift_detail').first()
    var start_at = card.find('.start-at').attr('value');
    var finish_at = card.find('.finish-at').attr('value');

    // Paint off cells
    var tr = card.closest('tr');
    var start_cell = tr.find('td[value="'+start_at+'"]').prev();
    var finish_cell = tr.find('td[value="'+finish_at+'"]');

    // delete color
    start_cell.nextUntil(finish_cell).css('background-color', '');
    start_cell.nextUntil(finish_cell).attr('work_location_id', '');

    // delete card
    $(this).closest('.shift_detail').remove();
    $(".most-left-cell>select").prop('disabled', false);
});