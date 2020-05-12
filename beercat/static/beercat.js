$(document).ready(function() {

  /**
   * Check whether selects are big-ish. If so, add filter.
   */
  $("select").each(function(idx, elt) {
    if ($(elt).find("option").length > 20) {
      var filter = $(elt).before("<input type='text' placeholder='filter' class='form-control fs'>");
      $(elt).addClass("filtered");
    }
  });

  $(".filtered").on("change", function(e) {

    $(e.target).attr('size', 0);
  });
  
  $(".fs").on("change keyup", function(e) {
    var filter = $(e.target).val();

    var regex = new RegExp(filter, "gi");
    var sel = $(e.target).next();
    var cnt = 1;
    
    $(sel).find('option').each(function(idx, elt) {
      if ($(elt).text().match(regex) === null) {
        $(elt).hide();
      } else {
        $(elt).show();
        cnt++;
      }
    });

    $(sel).attr('size', cnt);
  });

  $(".listingfilter").on('keyup', function(e) {

    var li;
    var text = $(e.target).val().toLowerCase();
    var listing = $(e.target).parents(".listing").eq(0);

    //if(text.length < 3) {
    //  return false;
    //}

    if (!text) {
      listing.find(".list-group-item").show();
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

        li = $(elt);

        if (li.text().toLowerCase().indexOf(text) == -1) {
          li.hide();
        } else {
          li.show();
        }
      });
    }
  });

  $(".listingfilter").submit(function(e) {

    var form = $(e.target);
    var listing = form.parents(".listing").eq(0);
    var li;
    var text = form.find("[name=filter]").val().toLowerCase();

    if (!text) {
      listing.find(".list-group-item").show("slow");
    } else {

      listing.find(".list-group-item").each(function(idx, elt) {

        li = $(elt);

        if (li.text().toLowerCase().indexOf(text) == -1) {
          li.hide("slow");
        } else {
          li.show("slow");
        }
      });
    }

    e.preventDefault();

    return false;
  });
});
