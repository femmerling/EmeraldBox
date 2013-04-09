$(document).ready(function(){
	$('#delete-link').click(function(e){
		e.preventDefault();
		url = $(e.currentTarget).data('url');
		callback = $(e.currentTarget).data('callback');
		if (confirm('Are you sure that you want to delete this record?'))
		{
			$.ajax({
				url:url,
				type:'DELETE',
				success: function(data){
					location.href = callback;
				}
			});
		}
	});

	$('#submit-put').click(function(e){
		e.preventDefault();
		url = $("#url").val();
		console.log(url)
		formData = $('#edit-form').serializeArray(); 
		$.ajax({
			url:url,
			type:'PUT',
			data:$('#edit-form').serializeArray(),
			success: function(data){
				location.href = url;
			}
		});
	});
});