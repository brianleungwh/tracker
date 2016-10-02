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

    $.post('/api/1.0/user-tracker/', requestBody, function(res) {
      console.log(res);
    });

  });

  $('form#delete').submit(function(e) {
    e.preventDefault();
    console.log('delete submit detected');
  });

});
