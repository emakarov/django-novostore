$('#fp').on('click', function (){
  $('#restorediv').fadeIn();	
});
    function sendlostlogin(){
    var text = $("#email_restore").val();
    var datasend = { email_restore: text };
      $.post('/accounts/restorepasswd/', datasend, function(data) {
	$("#restorepasswd").show(); //html('{% trans "Thanks for your question. You will receive the answer by email." %}');
      });
    }
