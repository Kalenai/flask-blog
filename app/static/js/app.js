$(document).foundation();
  $(document).on('close.fndtn.alert-box', function(event) {
    console.info('An alert box has been closed!');
  });