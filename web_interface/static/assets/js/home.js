$(document).ready(function () {
	$('body').append('<div style="" id="div_loading"><div class="loader">Loading...</div></div>');
	//load key value
	triggerAjax("show key", true, '/home_process', showKeyCB, undefined);
	function showKeyCB(data) {
		if (data.output === "Success") {
			$("#input_key").val(data.data);
		}
	}

	//load initial blacklist and whitelist values
	triggerAjax("show all", true, '/home_process', showAllCB, undefined);
	function showAllCB(data){
		if (data.output === "Success") {
			$("#table_whitelist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data[0].length; i++)
			{
				$('#table_whitelist').append("<tr><td>" + data.data[0][i] + "</td><td class='td_remove_whitelist' id='td_remove_whitelist_" + String(i) + "'><button class='red'>X</button></td></tr>");
			}
			$("#input_whitelist").val("");
			$("#table_blacklist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data[1].length; i++) {
				$('#table_blacklist').append("<tr><td>" + data.data[1][i] +"</td><td class='td_remove_blacklist' id='td_remove_blacklist_" + String(i) + "'><button class='red' >X</button></td></tr>");
			}
			$("#input_blacklist").val("");
		}
		removeLoader();
	}

	//whitelist add function
	$(document).on("click", "#button_whitelist", function () {
		if ($("#input_whitelist").val() !== "") {
			triggerAjax("add wh " + $("#input_whitelist").val(), true, '/home_process', addWhitelistCB, undefined);
		}
	});
	function addWhitelistCB(data){
		if (data.output === "Success") {
			$("#table_whitelist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data.length; i++) {
				$('#table_whitelist').append("<tr><td>" + data.data[i] + "</td><td class='td_remove_whitelist' id='td_remove_whitelist_" + String(i) + "'><button class='red'>X</button></td></tr>");
			}
			$("#input_whitelist").val("");
		}
	}

	//blacklist add function
	$(document).on("click", "#button_blacklist", function () {
		triggerAjax("add bl " + $("#input_blacklist").val(), true, '/home_process', addBlacklistCB, undefined);
	});
	function addBlacklistCB(data) {
		if (data.output === "Success") {
			$("#table_blacklist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data.length; i++) {
				$('#table_blacklist').append("<tr><td>" + data.data[i] + "</td><td class='td_remove_blacklist' id='td_remove_blacklist_" + String(i) + "'><button class='red' >X</button></td></tr>");
			}
			$("#input_blacklist").val("");
		}
	}

	//remove element from whitelist
	$(document).on("click", ".td_remove_whitelist", function () {
		if ($(this).attr('id') === "td_remove_whitelist_main") {
			triggerAjax("reset wh", true, '/home_process', undefined, undefined);
			$("#table_whitelist").find("tr:gt(1)").remove();
		} else {
			let id = parseInt($(this).attr('id').split("_")[3], 10);
			triggerAjax("rm wh " + String(id), true, '/home_process', removeWhitelistCB, undefined);
		}
	});
	function removeWhitelistCB(data) {
		if (data.output === "Success") {
			$("#table_whitelist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data.length; i++) {
				$('#table_whitelist').append("<tr><td>" + data.data[i] + "</td><td class='td_remove_whitelist' id='td_remove_whitelist_" + String(i) + "'><button class='red'>X</button></td></tr>");
			}
			$("#input_whitelist").val("");
		}
	}

	//remove element from blacklist
	$(document).on("click", ".td_remove_blacklist", function () {
		if ($(this).attr('id') === "td_remove_blacklist_main") {
			triggerAjax("reset bl", true, '/home_process', undefined, undefined);
			$("#table_blacklist").find("tr:gt(1)").remove();
		} else {
			let id = parseInt($(this).attr('id').split("_")[3], 10);
			triggerAjax("rm bl " + String(id), true, '/home_process', removeBlacklistCB, undefined);
		}
	});
	function removeBlacklistCB(data) {
		if (data.output === "Success") {
			$("#table_blacklist").find("tr:gt(1)").remove();
			for (let i = 0; i < data.data.length; i++) {
				$('#table_blacklist').append("<tr><td>" + data.data[i] + "</td><td class='td_remove_blacklist' id='td_remove_blacklist_" + String(i) + "'><button class='red' >X</button></td></tr>");
			}
			$("#input_blacklist").val("");
		}
	}

	//show / hide key
	$("#input_key").hover(function () {
		$(this).attr('type', 'text');
	}, function () {
		$(this).attr('type', 'password');
	});

	//random key generation
	$(document).on("click", "#button_key_random", function () {
		triggerAjax("regen", true, '/home_process', showKeyCB, undefined);
	});

	//set key
	$(document).on("click", "#button_key_set", function () {
		if ($("#input_key").val() !== "") {
			triggerAjax("regen " + $("#input_key").val(), true, '/home_process', showKeyCB, undefined);
		}
	});

	function removeLoader() {
        $("#div_loading").fadeOut(750, function() {
            $("#div_loading").remove();
        });
        $(".container").removeClass("hide")
    }

	function triggerAjax (data, async, url, callback, extra_input){
        $.ajax({
            data: {
                command: data
            },
            type: 'POST',
            async: async,
            url: url,
            success: function (recvData) {
                if (callback !== undefined) {
                    if (extra_input !== undefined) {
                        callback(recvData, extra_input);
                    } else {
                        callback(recvData);
                    }
                }
            }
        });
    }
});