Suit.$(function(){
  Suit.$('textarea').redactor({
    focus: true,
    imageUpload: '../demo/scripts/image_upload.php',
    fileUpload: '../demo/scripts/file_upload.php',
    imageGetJson: '/blog/redactorimagejson/'
  });
});