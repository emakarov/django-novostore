var intervals=new Array();
var previousid = 0;
$('.dropdown-toggle').click(
  function(){
    window.location.href=$(this).attr('slug');
  }
);
$('.dropdown-toggle').hover(
  function(){
    var id = $(this).attr('dropdown_node_id');
    $('#dropdown_node_menu_'+id).show();
    if (previousid != id){
      window.clearTimeout(intervals[previousid])
      $('#dropdown_node_menu_'+previousid).hide();
      previousid = id;
    }
    window.clearTimeout(intervals[id])
  },
  function(){
    var id = $(this).attr('dropdown_node_id');
    var str_fadeout = "$('#dropdown_node_menu_"+id+"').hide()";
    intervals[id] = setTimeout(str_fadeout,500);
  }
);
$('.dropdown-menu').hover(
  function(){
    var id = $(this).attr('dropdown_node_id');
    window.clearTimeout(intervals[id])
    $(this).show();
  },
  function(){
    $(this).hide();
  }
);