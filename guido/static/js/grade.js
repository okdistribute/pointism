function getSelectedText() {
    var iframe = document.getElementById("studentframe");
    var idoc= iframe.contentDocument || iframe.contentWindow.document;
    var iwin= iframe.contentWindow || iframe.contentDocument.defaultView;
    if (idoc.getSelection) {
        return idoc.getSelection();
    }
    else if (iwin.getSelection()) {
        return ''+iwin.getSelection();
    }
    return '';
}

$(function() {

    $("#searchbutton").button({
        icons: {
            secondary:"ui-icon-search"
        }
    });

    $("button").button();

    $("#code").bind("contextmenu",function(e){
        return false;
    }); 


    $("#code").qtip({
	content: { prerender: true, url: '/grading/entercomment' },
	show: { solo: true, when: { event: 'mousedown' } },
	hide: { when: { event: 'click' } },
	position: {
	    target: 'mouse',
	    adjust: { mouse: false }
	}
    });

            
    var student = $("#student").attr("value"),
    assignment = $("#assignment").attr("value"),
    problem = $("#problem").attr("value");
    
    $( "#entercomment" ).submit(function() {
	var code = getSelectedText();
        $.post("/grading/entercomment",
	       {
		   'student' : student,
		   'assignment' : assignment,
		   'problem' : problem,
                   'comment':$("input:#comment").val(),
                   'code': code
	       },
	       function(data) {
		   window.open();
		   document.write(data);
	       });

    });


    $( "#formGrade" ).submit(function() {

        $.post(window.location.pathname,
               {'grade':$("#submit_grade").attr("value")},
               function(data) {
                   window.open();
                   document.write(data);
               });
        return false;
    });

    $( "#grades" ).selectable({
	stop: function() {
            var result = $("input:#submit_grade");
            $(".ui-selected", this).each(function() {	
		grade = $(this).text();
		result.attr("value" , grade);
		$(this).siblings().removeClass("ui-selected");
            });
        }
    });
    


});