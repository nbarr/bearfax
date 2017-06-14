this.ProcessModel = function(_config) {
  var self = this;
  var defaultConfig = {

  };
  var config = $.extend(true, {}, defaultConfig, _config);

  var $cards = $('[data-set]');
  var currentCardIndex = 0;
  var socket = io('http://' + document.domain + ':' + location.port + '/task_status', {
    'transports': ['websocket', 'polling']  // Werkzeug = polling,
  });
  var maxTimeout = 32;
  var throttlingTimeout = 1;
  var throttlingMultiplier = 2;

  function getDataset() {
    return $cards[currentCardIndex] ? $cards[currentCardIndex].getAttribute('data-set') : null;
  }

  function getToken() {
    var parts = location.pathname.split('/');
    return parts[parts.length-1];
  }

  function init() {
    function onError(message) {
      $($cards[currentCardIndex]).removeClass('processing').addClass('error')
        .find('.error-message')
        .html(message || 'Unable to get information about this step. Try again later.');
    }

    $($cards[currentCardIndex]).removeClass('unprocessed').addClass('processing');

    socket.on('connect', function() {
      console.log('namespace connect');
      if (getDataset()) {
        socket.emit('check_task_status', {dataset: getDataset(), token: getToken()});
      }
    });

    socket.on('task_status_response', function(response) {
      console.log('Task Status Response received: ', response);

      if (!response.success) {
        onError(response.message);
      } else {
        if (response.data && response.data.in_progress) {
          throttlingTimeout *= throttlingMultiplier;
          if (throttlingTimeout > maxTimeout) throttlingTimeout = 1;
          console.log('Response for dataset ' + getDataset() +
                      ' still not ready, throttling pending request for ' + throttlingTimeout +
                      ' seconds...');
        } else {
          $($cards[currentCardIndex]).removeClass('processing').addClass('done');
          currentCardIndex++;
          throttlingTimeout = 1;
        }

        if (getDataset()) {
          $($cards[currentCardIndex]).removeClass('unprocessed').addClass('processing');

          setTimeout(function() {
            var data = {dataset: getDataset(), token: getToken()};
            console.log('Emitting check_task_status for dataset ', data);
            socket.emit('check_task_status', data);
          }, throttlingTimeout * 1000);
        }
      }
    });

    socket.on('disconnect', function() {
      console.log('DISCONNECTED');
    });

    socket.on('connect_failed', function() {
      console.log('CONNECT_FAILED');
    });

  }

  init();
};
