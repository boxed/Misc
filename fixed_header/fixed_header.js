$j = jQuery;
function create_fixed_header(html)
{
	body = $j('body');
	if ($j('#fixed_top_header').length == 0)
	{
		body.append('<div id="fixed_top_header"></div>');
		body.addClass('body_offset');
    	header = $j('#fixed_top_header');
    	header.addClass('fixed_header');
    	header.html(html);
	}
}
function remove_fixed_header()
{
	$j('#fixed_top_header').remove();
	$j('body').removeClass('body_offset')
}