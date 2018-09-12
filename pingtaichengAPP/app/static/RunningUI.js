function setpicCSS(){
	height = $(window).height();
	width = $(window).width();
	$('#picture5').css({
		'height' : height / 2.4,
		'width' : width / 3,
		'margin': '0 auto',
	});
	height2 = $('#picture5').height();
	$('.tablerow').height(height2 / 3);
	height1 = $('.tablerow').height();
	$('img').height(height1 / 2);
	height3 = $('.tablerow').height() - $('img').height();
	$('img').css({
		'margin-top' : height3 / 3
	});
	height4 = 300 - $('div.weight').height();
	$('div.weight').css({
		'margin-top' : height4 / 2
	});
}

function judge(data,tag){
	if (data['Tag' + tag + 'Forced'] || data['Tag' + tag + 'tempOver']) {
		$('td.' + tag).css({
			'background-color': 'yellow',
		});
	}
	else {
		$('td.' + tag).css({});
	}

	if (data['Tag' + tag + 'Loss'] || data['Tag' + tag + 'Over']) {
		$('td.' + tag).css({
			'background-color': 'red',
		});
	}
	else {
		$('td.' + tag).css({});
	}

	if (data['Tag' + tag + 'Partial']) {
		$('img.img' + tag).show()
	}
	else {
		$('img.img' + tag).hide();
	}

}

function getData(){
	$.ajax({
    	type:"POST",
		url: "/scale/data",
		success:function(data){
			if(data){
				$('#Tag1').text(data.Tag1);
	            $('#Tag2').text(data.Tag2);
	            $('#Tag3').text(data.Tag3);
	            $('#Tag4').text(data.Tag4);
	            $('#weight').text(data.weight);
	            $('#runtime').text(data.run_time);
				$('#normal').text(data.normal_time);
				$('#alarm').text(data.alarm_time);
				$('#fault').text(data.fault_time);
	            var date = data.timestr;
	            var reason = data.falutmsg;
	            var str = '故障时间：'+ '<br/>' + date + '<br/>' + '故障原因：' + '<br/>' + reason;
	            if (data.state == 'alarm') {
	                $('button:gt(0)').removeAttr('class');
	                $('button:gt(0)').attr('class', 'light');
	                $('button:gt(0)').addClass('alarm');
	                $('button:gt(0)').attr('data-content', str)
	            }
	            else if (data.state == 'fault') {
	                $('button:gt(0)').removeAttr('class');
	                $('button:gt(0)').attr('class', 'light');
	                $('button:gt(0)').addClass('fault');
	                $('button:gt(0)').attr('data-content', str)
	            }
	            else{
	                $('button:gt(0)').removeAttr('data-content');
	                $('button:gt(0)').removeAttr('class');
	                $('button:gt(0)').attr('class', 'light');
	            }
	            
	            judge(data,1);
	            judge(data,2);
	            judge(data,3);
	            judge(data,4);
	            
			}
		}
	});
}


$(document).ready(function(){
	$('[data-toggle="popover"]').popover();
	$('img.img1').hide();
	$('img.img2').hide();
	$('img.img3').hide();
	$('img.img4').hide();
	setpicCSS();
	window.onresize = function(){
		setpicCSS();
	};
	window.setTimeout("getData()",0);
    window.setInterval("getData()",1000);

})