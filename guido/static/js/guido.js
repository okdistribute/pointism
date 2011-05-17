function getSelectedText() {
    if (window.getSelection) {
        return window.getSelection();
    }
    else if (document.selection) {
        return document.selection.createRange().text;
    }
    return '';
}

$(function() {
    $( "#grade" ).selectable({
	stop: function() {
            var result = $("input:#submit_grade");
            $(".ui-selected", this).each(function() {
                var index = $("#grade li").index(this);
		var grade = 7 - index;
		result.attr("value" , grade);
		$(this).siblings().removeClass("ui-selected");
                var refreshVal = $(this).attr("value");
            });
        }
    });
    
    $.ajaxSetup ({
	cache: false
    });
    var ajax_load = "<img src='/static/images/load.gif' alt='loading...' />";

    var comment = $( "textarea#editablecomment"),
    tips = $(".validateTips"),
    prevcomments = $("#prevcomments"),
    submitting = $("input:#editedcomment");
    
    function updateTips( t ) {
	tips
	    .text( t )
	    .addClass( "ui-state-highlight" );
	setTimeout(function() {
	    tips.removeClass( "ui-state-highlight", 1500 );
	}, 500 );
    }
    
    function checkLength( o, n, min ) {
	if ( o.val().length <= min ) {
	    o.addClass( "ui-state-error" );
	    updateTips( "Length of " + n + " must be greater than " + min + "." );
	    return false;
	} else {
	    return true;
	}
    }

    function updateStatus( s ) {
	var status = $( "#commentdbstatus" );
	status.empty();
	status.append(s).show().fadeOut(1500, "linear");
	status.addClass("ui-state-highlight");
	setTimeout(function() {
	    status.removeClass( "ui-state-highlight", 1500 );
	}, 1500 );
    }
    
    $( "#comment-dialog" ).dialog({
	autoOpen: false,
	height: 320,
	width: 625,
	position: ['left', 'bottom'],
	show: 'slide',
	hide: 'slide',
	open: function(event, ui) {
	    commentid = $("#prevcomments option:selected").attr("value");
	    $.get("/commenttext.ajax", {commentid: commentid}, function(data) {
		comment.val(data);
	    });
	},
	buttons: {
	    "Edit!": function() {
		var bValid = true;
		bValid = bValid && checkLength(comment, "comment" , 1);
		if ( bValid ) {
		    commentid = $("#prevcomments option:selected").attr("value");
		    $("#divprevcomments")
			.html(ajax_load)
			.load("/commentedit.ajax", {commentid: commentid, text: comment.val()},
			      function(responseText){ 
				  updateStatus("Success! Comment edited.");
				  return responseText; });
		    $( this ).dialog( "close" );
		}
	    },
	    Cancel: function() {
		$( this ).dialog( "close" );
	    },
	    "Delete Comment": function() {
		$( "#confirm-delete" ).dialog( "open" );
		$( this ).dialog( "close" );
	    }
	},
	close: function() {
	    comment.val( "" ).removeClass( "ui-state-error" );
	}
    });

    $( "#btnEditcomment" )
	.button()
	.click(function() {
	    if($("#prevcomments option:selected").text() !== '') {		
		$( "#comment-dialog" ).dialog( "open" );
	    }
	    else {
		updateStatus("No comment selected");
	    }
	});

    $( "#confirm-delete" ).dialog({
	autoOpen: false,
	resizable: false,
	height:280,
	position: ['left', 'bottom'],
	modal: true,
	hide: 'slide',
	buttons: {
	    "Delete Comment": function() {
		$("#divprevcomments")
		    .html(ajax_load)
		    .load("/commentdelete.ajax", {commentid: commentid},
			  function(responseText){ 
			      updateStatus("Comment deleted.");
			      return responseText; });
		$( this ).dialog( "close" );
	    },
	    Cancel: function() {
		$( this ).dialog( "close" );
		$( "#btnEditcomment" ).click();
	    }
	}
    });
});

