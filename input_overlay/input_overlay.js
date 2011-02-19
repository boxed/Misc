$j = jQuery;
function updateInputOverlays() {
	function setupDefaultHandling(i) {
		var defaultValue = $j(this).attr('default_value');
		$j(this).val(defaultValue);
		$j(this).attr('defaultValue', defaultValue);
		$j(this).addClass("defaultIdleField");
   		$j(this).focus(function() {
   			$j(this).removeClass("idleField").removeClass("defaultIdleField").addClass("focusField");
		    if (this.value == this.defaultValue) { 
		    	this.value = '';
			}
			if(this.value != this.defaultValue) {
    			this.select();
    		}
		});
		$j(this).blur(function() {
		    if ($j.trim(this.value) == '') {
		    	this.value = (this.defaultValue ? this.defaultValue : '');
		    	$j(this).removeClass("focusField").addClass("defaultIdleField");
			}
			else {
			    $j(this).removeClass("focusField").addClass("idleField");
			}
		});
	}
	$j('input[type="text"]').each(setupDefaultHandling);
	$j('input[type="password"]').each(setupDefaultHandling);
}
$j(document).ready(function() {
	updateInputOverlays();
});			
