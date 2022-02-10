const user_input_staff = $("#user-input_staff")
const search_icon_staff = $('#search_icon_staff')
const artists_div_staff = $('#studenttable_staff')
const endpoint_staff = '/appURL/staffrecord/'
const delay_by_in_ms_staff = 700
let scheduled_function_staff = false

let ajax_call_staff = function (endpoint_staff, request_parameters_staff) {
	$.getJSON(endpoint, request_parameters_staff)
		.done(response => {
			// fade out the artists_div, then:
			
				// replace the HTML contents
				artists_div_staff.html(response['html_from_view'])
				// fade-in the div with new contents
				
				// stop animating search icon
				search_icon_staff.removeClass('blink')
			
		})
}


user_input_staff.on('keyup', function () {

	const request_parameters_staff = {
		q: $(this).val() // value of user_input: the HTML element with ID user-input
	}

	// start animating the search icon with the CSS class
	search_icon_staff.addClass('blink')

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function_staff) {
		clearTimeout(scheduled_function_staff)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function_staff = setTimeout(ajax_call_staff, delay_by_in_ms_staff, endpoint_staff, request_parameters_staff)
})
