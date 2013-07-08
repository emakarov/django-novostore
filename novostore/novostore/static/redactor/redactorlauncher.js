Suit.$(function(){
  Suit.$('textarea').redactor({
    focus: true,
    imageUpload: '/blog/uploadimagejson/',
    fileUpload: '../demo/scripts/file_upload.php',
    imageGetJson: '/blog/redactorimagejson/'
  });
});