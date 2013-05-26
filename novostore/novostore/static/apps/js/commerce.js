function addproducttocart(){
    var product_id = $("#productid").attr('value');
    var productquantity = $("#productquantity").val();
    var datasend = { product_id: product_id, productquantity : productquantity };
    $.post(addtocarturl, datasend, function(data) {
      var n = parseInt(data['cart']);
      resetitemsincart(n,'add')
    });
}
function deletefrombag(element_id){
    var datasend = { element_id: element_id };
    $.post(deletefromcarturl, datasend, function(data) {
    	var ajax_status = data['ajax_status'];
    	if (ajax_status == 'deleted'){
    	  $('#product_tr_'+element_id).fadeOut('slow', function() {
         	  recalculateprice();
    	  });
    	  resetitemsincart(data['cartitems'],'delete');
    	}
    });
}
function resetitemsincart(n,mode){
      console.log(n);
      if (n==0){
        $("#cart_nitems").html(currentlyThereNoStr+itemsInStr);
      }
      if (n==1){
        $("#cart_nitems").html(n+' '+itemInStr);
      }
      var settedrus = false;
      if (lanuage_code == 'ru'){
        if (n%10 ==1 && n != 11){
          $("#cart_nitems").html(n+' товар в');
          settedrus = true;
        }
        if ( ( n%10==2 || n%10 == 3 || n%10 == 4 ) && n != 12 && n != 13 && n != 14){
          $("#cart_nitems").html(n+' товара в');
          settedrus = true;
        }
      }
      if (n>1 && !settedrus){
        $("#cart_nitems").html(n+' '+itemsInStr);
      }
      if (n>0){
        if (mode == 'add' ){
          $('#cart_nitems_a').popover('show');
          $('.popover').css('background-color','#00aff0').css('color','#fff');
          var fstr = "$('.popover').fadeOut()";
          setTimeout(fstr,1500);
        }
      }
      if(n>0){
        //$("#cart_nitems_a").addClass('btn btn-small');
      }
}
function increase(element_id){
  modifyelement(element_id, 'increase');
}
function decrease(element_id){
  modifyelement(element_id, 'decrease');
}

function modifyelement(element_id, modify){
    var datasend = { element_id: element_id, modify: modify };
    var datasend = { element_id: element_id, modify: modify };
    $.post(changeelementincarturl, datasend, function(data) {
    	var ajax_status = data['ajax_status'];
    	if (ajax_status == 'deleted'){
    	  //	console.log('deleted');
    	  var element_id = data['element_id'];
    	  $('#product_tr_'+element_id).fadeOut('slow', function() {
         	  recalculateprice();
    	  });
    	  resetitemsincart(data['total_quantity'],'');
    	}
    	else if (ajax_status != 'error') {
    	  var element_id = data['element_id'];
    	  var quant = data['quantity'];
    	  $("#quant_"+element_id).val(quant);
    	  var price = $("#product_price_"+element_id).html();
    	  $("#product_sum_"+element_id).html(price*quant);
          recalculateprice();
    	  resetitemsincart(data['total_quantity'],'');
    	}
    });
}

function recalculateprice(){
      var elements = $(".product_sum:visible");
      total_sum = 0;
      $.each(elements, function(index,value){
        total_sum += parseFloat($(value).html());
      });
      $("#total_sum").html(total_sum);
}
