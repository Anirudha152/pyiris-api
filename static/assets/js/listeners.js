ListenerGlobals = {
    "isMonitorRunning": "",
    "reloadedPage": true,
    "sent": false,
    "listenersShown": false,
    "mainSettingsShown": false,
    "bindShown": false,
    "error": true
};
$(document).ready(function () {
    // load settings from server memory
    triggerAjax("show options", true, '/listeners_process', showOptionsCB, undefined);
    function showOptionsCB(data) {
        if (data.output === "Success") {
            $("#i_bind_spinner").hide();
            $("#td_main_settings_interface_value").html(data.data["Interface"][0]);
            $("#td_main_settings_port_value").html(data.data["Port"][0]);
            $("#td_main_settings_name_value").html(data.data["Name"][0]);
            $("#td_main_settings_reply_value").html(data.data["Reply"][0]);
            if(ListenerGlobals.mainSettingsShown) {
                rotate(0, "#img_main_settings_arrow");
                $("#div_main_settings").show();
            }
            else {
                rotate(270, "#img_main_settings_arrow");
                $("#div_main_settings").hide();
            }

            if(ListenerGlobals.bindShown) {
                rotate(0, "#img_bind_arrow");
                $("#div_bind").show();
            }
            else {
                rotate(270, "#img_bind_arrow");
                $("#div_bind").hide();
            }

            if (ListenerGlobals.listenersShown) {
                rotate(0, "#img_listeners_arrow");
                listenerSettings();
            }
            else {
                rotate(270, "#img_listeners_arrow");
                listenerSettings();
            }
        }
    }

    // pause trigger function to rename
    $(document).on('focusout', '.td_listeners_name', function () {
        if ($(this).text() !== "") {
            if (!ListenerGlobals.sent) {
                ListenerGlobals.sent = true;
                triggerAjax("rename " + $(this).attr('id').split('_')[3] + " " + $(this).text(), true, '/listeners_process', pauseCB, undefined);
            }
        }
    });
    function pauseCB(data) {
        if (data.output === "Fail") {
            ListenerGlobals.error = true;
            showMessage(data.output_message);
        }
    }

    // arrow click event
    $(".img_arrow").click(function(){
        if ($(this).attr('id') === "img_main_settings_arrow") {
            if (ListenerGlobals.mainSettingsShown) {
                rotate(270, "#img_main_settings_arrow");
                $("#div_main_settings").hide();
                ListenerGlobals.mainSettingsShown = false;
            } else {
                rotate(0, "#img_main_settings_arrow");
                $("#div_main_settings").show();
                ListenerGlobals.mainSettingsShown = true;
            }
        } else if ($(this).attr('id') === "img_bind_arrow") {
            if(ListenerGlobals.bindShown) {
                rotate(270, "#img_bind_arrow");
                $("#div_bind").hide();
                ListenerGlobals.bindShown = false;
            }
            else {
                rotate(0, "#img_bind_arrow");
                $("#div_bind").show();
                ListenerGlobals.bindShown = true;
            }
        } else if ($(this).attr('id') === "img_listeners_arrow") {
            if (ListenerGlobals.listenersShown) {
                rotate(270, "#img_listeners_arrow");
                ListenerGlobals.listenersShown = false;
                listenerSettings();
            }
            else {
                rotate(0, "#img_listeners_arrow");
                ListenerGlobals.listenersShown = true;
                listenerSettings();
            }
        }
    });

    // main settings update event
    $(".button_main_settings").click(function () {
        let option = $(this).attr('id').split('_')[3][0].toUpperCase() + $(this).attr('id').split('_')[3].slice(1);
        if ($("#input_main_settings_" + option.toLowerCase()).val() !== "" || option === "Reply") {
            triggerAjax("set " + option + " " + $("#input_main_settings_" + option.toLowerCase()).val(), true, '/listeners_process', mainSettingsUpdateCB, {'option': option});
        }
    });
    function mainSettingsUpdateCB(data, extra_input){
        if (data.output === "Success") {
            $("#td_main_settings_" + extra_input["option"].toLowerCase() + "_value").html(data.data[extra_input["option"]][0]);
            $("#input_main_settings_" + extra_input["option"].toLowerCase()).val("");
        }
    }

    // bind event
    $("#button_bind").click(function () {
        $("#i_bind_spinner").show();
        if ($("#input_bind_interface").val() !== "" && $("#input_bind_port").val() !== "") {
            triggerAjax("bind " + $("#input_bind_interface").val() + " " + $("#input_bind_port").val(), true, '/listeners_process', bindClickCB, undefined);
        }
        else {
            ListenerGlobals.error = true;
            showMessage("Please enter valid interface and port values");
            scrollToTop();
            $("#i_bind_spinner").hide();
        }
    });
    function bindClickCB(data) {
        if (data.output === "Success") {
            ListenerGlobals.error = false;
            $("#input_bind_interface").val("");
            $("#input_bind_port").val("");
            showMessage(data.output_message);
            scrollToTop();
            $("#i_bind_spinner").hide();
        }
        else {
            ListenerGlobals.error = true;
            $("#input_bind_interface").val("");
            $("#input_bind_port").val("");
            showMessage(data.output_message);
            scrollToTop();
            $("#i_bind_spinner").hide();
        }
    }

    // click run event
    $("#button_run").click(function (){
        triggerAjax("run", true, '/listeners_process', undefined, undefined);
    });

    // kill listener event
    $(document).on('click', '.td_remove_listener', function() {
        let id = $(this).attr('id').split("_")[3];
        if (id !== "main") {
            $("#i_remove_listener_spinner_" + id).show();
            triggerAjax("kill " + id, true, '/listeners_process', undefined, undefined);
        }
    });

    // kill all listeners event
    $("#td_remove_listener_main").click(function () {
        $("#i_remove_listener_spinner_main").show();
        triggerAjax("kill all", true, '/listeners_process', undefined, undefined);
    });

    //reset
    $(".button_main_settings_reset").click(function () {
        let command = "reset ";
        if ($(this).attr('id') === "button_main_settings_reset_all") {
            command = command + "all";
        }
        else {
            command = command + $(this).attr('id').split('_')[4][0].toUpperCase() + $(this).attr('id').split('_')[4].slice(1);
        }
        triggerAjax(command, true, '/listeners_process', resetCB, {});
    });
    function resetCB(data) {
        if (data.output === "Success") {
            $("#td_main_settings_interface_value").html(data.data["Interface"][0]);
            $("#td_main_settings_port_value").html(data.data["Port"][0]);
            $("#td_main_settings_name_value").html(data.data["Name"][0]);
            $("#td_main_settings_reply_value").html(data.data["Reply"][0]);
        } else {
            ListenerGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    // other functions
    function rotate(degree, arrow_id) {
        $(arrow_id).css({ WebkitTransform: 'rotate(' + String(degree) + 'deg)'});
    }

    function showMessage(msg){
        let elmt;
        if (ListenerGlobals.error) {
            elmt = document.getElementById("error");
        } else {
            elmt = document.getElementById("success");
        }
        elmt.innerHTML = esc(msg) + "<a onclick='closeMessage()' id='closeError'>x</a>";
        elmt.classList.remove('hide');
        elmt.classList.add('show');
    }

    function esc(str) {
        if(str){
            return str.toString()
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/\"/g, '&quot;')
                .replace(/\'/g, '&#39;')
                .replace(/\//g, '&#x2F;');
        }
        return "";
    }

    function scrollToTop() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
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

function closeMessage(){
    let elmt;
    if (ListenerGlobals.error) {
        elmt = document.getElementById("error");
    } else {
        elmt = document.getElementById("success");
    }
    elmt.innerHTML = "";
    elmt.classList.remove('show');
    elmt.classList.add('hide');
}

function listenerSettings() {
    if ($("#table_listeners tr").length === 1){
        $("#div_listeners_heading").hide();
        $("#div_listeners").hide();
    }
    else {
        $("#div_listeners_heading").show();
        if (ListenerGlobals.listenersShown) {
            $("#div_listeners").show();
        }
        else {
            $("#div_listeners").hide();
        }
    }
}