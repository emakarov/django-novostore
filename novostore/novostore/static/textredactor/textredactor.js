var latestrange = '';
var currentimgurl = '';

$(function(){
    // on page load...

//    $('textarea').html('');


    var buttonhtml = '<div class="inputimg btn">Insert Image</div>';
    
    var modalhtml = ' <div id="myModal" class="modal hide fade" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">';
    modalhtml += '<div class="modal-header">';
    modalhtml += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>';
    modalhtml += '<h3 id="myModalLabel">{% trans "Request for a product" %}</h3>';
    modalhtml += '</div>';
    modalhtml += '<div class="modal-body">';
    modalhtml += '<input id="imageurl" type="text" style="margin-bottom:10px;">';
    modalhtml += '<button onclick="insertimage()" class="btn btn-primary" data-dismiss="modal" aria-hidden="true">Insert image</button>';
    modalhtml += '</div>';
    modalhtml += '<div class="modal-footer">';
    modalhtml += '<button class="btn" data-dismiss="modal" aria-hidden="true">{% trans "Close" %}</button>';
    modalhtml += '</div>';
    modalhtml += '</div>';
    
    var buttonboldhtml = "<button class='inputbold btn'><b>B</b></button>";

    var textareas = Suit.$('textarea');
    for (var i=0;i<textareas.length;i++){
      var resulthtml = "<div class='contentedit' contenteditable id='textredactor_area_"+i+"' style='background:#fff;height:200px;overflow-y:auto;overflow-x:none;padding:10px;border:1px solid #eee;'>";
      resulthtml += "</div>";
      var txta = textareas[i];
      Suit.$(buttonhtml).insertBefore(txta);
      Suit.$(buttonboldhtml).insertBefore(txta);
      Suit.$(resulthtml).insertAfter(txta);
      Suit.$(txta).hide();
      Suit.$("#textredactor_area_"+i).html(Suit.$(txta).val());
    }
    Suit.$(modalhtml).insertAfter(Suit.$('body'));

    Suit.$(".inputimg").on('click', function(){
      Suit.$('#myModal').modal('show');
    });
    
    var currentrange = '';

    Suit.$(".inputbold").on('click', function(e){
      e.preventDefault();
      document.execCommand('bold',false,null);
      var contentedits = Suit.$('.contentedit');
      refreshcontents();
      
    });
    
    Suit.$('.contentedit').on("keyup click", function(e){
        latestrange = saveSelection()
    	Suit.$(this).prev().val(Suit.$(this).html());
    });

});

function insertimage(){
  restoreSelection(latestrange);
  document.execCommand("insertimage",false,$("#imageurl").val() );
  refreshcontents();
}

function saveSelection() {
    if (window.getSelection) {
        sel = window.getSelection();
        if (sel.getRangeAt && sel.rangeCount) {
            return sel.getRangeAt(0);
        }
    } else if (document.selection && document.selection.createRange) {
        return document.selection.createRange();
    }
    return null;
}

function restoreSelection(range) {
    if (range) {
        if (window.getSelection) {
            sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
        } else if (document.selection && range.select) {
            range.select();
        }
    }
}

function refreshcontents(){
      var contentedits = Suit.$('.contentedit');
      for (var i=0;i<contentedits.length;i++){
      	var ce = contentedits[i];
      	console.log(Suit.$(ce).html());
        Suit.$(ce).prev().val(Suit.$(ce).html());
      }
}