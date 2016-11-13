Zepto(function($) {

  $('.form').find('input, textarea').on('keyup blur focus', function (e) {
    
    var $this = $(this),
        label = $this.prev('label');

      if (e.type === 'keyup') {
        if ($this.val() === '') {
            label.removeClass('active highlight');
          } else {
            label.addClass('active highlight');
          }
      } else if (e.type === 'blur') {
        if( $this.val() === '' ) {
          label.removeClass('active highlight'); 
        } else {
          label.removeClass('highlight');   
        }   
      } else if (e.type === 'focus') {
        
        if( $this.val() === '' ) {
          label.removeClass('highlight'); 
        } 
        else if( $this.val() !== '' ) {
          label.addClass('highlight');
        }
      }

  });

  $('.tab a').on('click', function (e) {
    
    e.preventDefault();
    
    $(this).parent().addClass('active');
    $(this).parent().siblings().removeClass('active');
    
    target = $(this).attr('href');
    
    $('.tab-content > div').not(target).hide();
    
    $(target).show();
    
  });

  $('form#create').submit(function(e) {
    e.preventDefault();

    var inputValues = $(this).serializeArray();
    var userEmail = inputValues[0].value;
    var resultsPageUrl = inputValues[1].value;

    var requestBody = {
      'email': userEmail,
      'results_page_url': resultsPageUrl
    };

    $('button#create').text('Done!');

    $.post('/api/1.0/user-tracker/', requestBody)
      .done(function(data) {
        alert('Tracker Created. A confirmation email will be on its way!');
      })
      .fail(function(xhr, errorType, error) {
        alert('Tracker may exist already! Or you have entered an invalid input. Please check.');
      })
      .always(function() {
        $('button#create').text('Create');
      });

  });

  $('form#delete').submit(function(e) {
    e.preventDefault();

    var inputValues = $(this).serializeArray();
    var userEmail = inputValues[0].value;
    var resultsPageUrl = inputValues[1].value;

    var requestBody = {
      'email': userEmail,
      'results_page_url': resultsPageUrl
    };

    $('button#delete').text('Done!');

    $.ajax({
      type: 'DELETE',
      url: '/api/1.0/user-tracker/',
      data: requestBody,
    }).done(function(data) {
      alert('Tracker Deleted.');
    }).fail(function(data) {
      alert('Tracker does not exist! Or you entered invalid inputs. Please check.');
    }).always(function() {
      $('button#delete').text('Delete');
    });

  });

});
