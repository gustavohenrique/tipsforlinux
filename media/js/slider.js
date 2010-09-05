	$(document).ready(function(){
		$(".info-link").click(function(){
		$(this).parent().find(".ibox").slideToggle("" );
			$(this).toggleClass("active"); return false;
		});
		
		$(".ibox .delete").click(function(){
		  $(this).parents(".ibox").animate({ opacity: "hide" }, "slow");
		});
		
	});
	

	
	
	
	
	
	
	

