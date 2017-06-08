function processStep($card, callback) {
  $card.removeClass('unprocessed').addClass('processing');

  var dataset = $card.attr('data-set');
  var token = location.pathname.split('/');
  token = token[token.length-1];

  var onerror = function(message) {
    $card.removeClass('processing').addClass('error')
      .find('.error-message')
      .html(message || 'Unable to get information about this step. Try again later.');
  };

  console.log('Polling status endpoint for dataset ' + dataset);

  $.ajax({
    type: 'GET',
    url: '/api/fax_status/',
    data: {token: token, dataset: dataset},
    success: function(response) {
      if (!response.success) {
        onerror(response.message);
      } else {
        if (response.data && response.data.in_progress) {
          console.log('Response for dataset ' + dataset + ' still not ready, throttling pending request...');
          setTimeout(function() { processStep($card, callback); }, 7000);
        } else {
          $card.removeClass('processing').addClass('done');
          if (callback) callback();
        }
      }
    },
    error: onerror,
    always: function() {
    }
  });
}

$(function() {
  processStep($('[data-set="fax_requested"]'), function() {
    processStep($('[data-set="email_verified"]'), function() {
      processStep($('[data-set="fax_queued"]'), function() {
        processStep($('[data-set="fax_being_transmitted"]'), function() {
          processStep($('[data-set="fax_sent"]'));
        });
      });
    });
  });
});
