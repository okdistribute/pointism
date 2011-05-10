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
});

