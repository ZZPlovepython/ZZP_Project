function sendData(){
	var date = $('#date').val();
	var operate = $('#operate').val();
	var standard = $('#standard').val();
	var zero = $('#zero').val();
    var data = {"date": date, "operate": operate, "stadnard": standard, "zero": zero};
    $.ajax({
        type:"POST",
        url: "/scale/engineer/insertOperation",
        DataType:"json",
        data:data,
        success:function(data){
        	if (data.success) {
        		alert('上传参数成功！');
        		$('#submit').removeAttr("disabled");
        	}
        	else{
        		alert('上传参数失败！');
        		$('#submit').removeAttr("disabled");
        	}
        }
    });
}

$(document).ready(function(){
	$('form').on('submit', function(e){
		e.preventDefault();
		sendData();
	})
})