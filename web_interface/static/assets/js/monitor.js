MonitorGlobals = {
    "error": true,
    "currentLocation": undefined
};
$(document).ready(function () {
    MonitorGlobals.currentLocation = location.href.split("/").slice(-1)[0];
    if (MonitorGlobals.currentLocation.includes("listeners")) {
        MonitorGlobals.currentLocation = "listeners";
    } else {
        MonitorGlobals.currentLocation = "scouts";
    }

    // start live loading of listener values
    function monitor() {
        let reloadedPage;
        if (MonitorGlobals.currentLocation === "listeners") {
            reloadedPage = ListenerGlobals.reloadedPage;
        } else if (MonitorGlobals.currentLocation === "scouts") {
            reloadedPage = ScoutGlobals.reloadedPage;
        }
        if (!reloadedPage) {
            triggerAjax("monitor normal", true, '/monitor_process', afterDataReceived, undefined);
        } else {
            if (MonitorGlobals.currentLocation === "listeners") {
                ListenerGlobals.reloadedPage = false;
            } else if (MonitorGlobals.currentLocation === "scouts") {
                ScoutGlobals.reloadedPage = false;
            }
            triggerAjax("monitor reload", true, '/monitor_process', afterDataReceived, undefined);
        }
    }
    function afterDataReceived(recvData) {
        let output = recvData["output"];
        let message = recvData["output_message"];
        let data = recvData["data"];
        if (message === "Msg") {
            if (output === "Success") {
                MonitorGlobals.error = false;
                showMessage(data);
                scrollToTop();
            } else {
                MonitorGlobals.error = true;
                showMessage(data);
                scrollToTop();
            }
        } else {
            if (output === "Success") {
                if (MonitorGlobals.currentLocation === "listeners") {
                    if (message.includes("Li Data")) {
                        updateListeners(data[0], false);
                    } else if (message.includes("Li Empty")) {
                        updateListeners(undefined, true);
                    }
                } else if (MonitorGlobals.currentLocation === "scouts") {
                    if (message.includes("Sc Data")) {
                        updateScouts(data[1], false);
                    } else if (message.includes("Sc Empty")) {
                        updateScouts(undefined, true);
                    }
                }
            } else if (output === "Fail") {
                MonitorGlobals.error = true;
                showMessage(message);
                scrollToTop();
            }
        }
        monitor();
    }
    monitor();

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

    function showMessage(msg){
        let elmt;
        if (MonitorGlobals.error) {
            elmt = $("#error");
        } else {
            elmt = $("#success");
        }
        elmt.html(esc(msg) + "<a onclick='closeMessageMonitor()' id='closeError'>x</a>");
        elmt.show();
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

    function updateScouts(scouts_db, is_empty) {
        if (!is_empty) {
            if (ScoutGlobals.ifc === "Scouts") {
                $("#h1_scouts_heading").text("Scouts");
                $("#div_direct_win").hide();
                $("#div_direct_lin").hide();
                $("#p_fail_text").hide();
                $("#div_scouts_table_heading").show();
                $("#div_scouts_table").show();
                $("#div_scouts").show();
                $("#div_console").hide();
                if ($("#table_scouts :focus").attr('id') === undefined) {
                    ScoutGlobals.nameSentToServer = false;
                    $("#table_scouts").find("tr:gt(0)").remove();
                    for (const value of Object.values(scouts_db)) {
                        $("#table_scouts").append("<tr id='tr_scouts_table_" + String(value[0]) + "'><td>" + String(value[0]) + "</td><td>" + String(value[1]) + "</td><td>" + String(value[2]) + "</td><td>" + String(value[3]) + "</td><td contenteditable='true' class='td_scouts_table_name' id='td_scouts_table_name_" + String(value[0]) + "'>" + String(value[4]) + "</td><td>" + String(value[5]) + "</td><td>" + String(value[6]) + "</td><td><i class='fa fa-circle-o-notch fa-spin i_scouts_table_spinner' id='i_scouts_table_spinner_" + String(value[0]) + "'></i></td></tr>");
                        $("#i_scouts_table_spinner_" + String(value[0])).hide();
                    }
                    if (ScoutGlobals.scoutButtonInFocus) {
                        tableRowClickable(true)
                    } else {
                        tableRowClickable(false)
                    }
                }
            }
        } else {
            ScoutGlobals.ifc = "Scouts"
            $("#h1_scouts_heading").text("Scouts");
            $("#div_direct_win").hide();
            $("#div_direct_lin").hide();
            $("#div_scouts_table_heading").hide();
            $("#div_scouts_table").hide();
            $("#p_fail_text").show();
            $("#div_console").hide();
        }
    }

    function updateListeners(listeners_db, is_empty) {
        if (!is_empty) {
            if ($("#table_listeners :focus").attr('id') === undefined) {
                ListenerGlobals.sent = false;
                $("#i_remove_listener_spinner_main").hide();
                $("#table_listeners").find("tr:gt(0)").remove();
                for (const [key, value] of Object.entries(listeners_db)) {
                    let connections = false;
                    let toAppend = "<tr id='tr_listeners_" + String(key) + "'><td>" + String(key) + "</td><td>" + String(value[0]) + "</td><td>" + String(value[1]) + "</td><td contenteditable='true' class='td_listeners_name' id='td_listeners_name_" + String(key) + "'>" + String(value[2]) + "</td><td>" + String(value[3]) + "</td>";
                    if (value[4].length > 0) {
                        connections = true;
                        toAppend = toAppend + "<td>";
                        for (let connection of value[4]) {
                            if (value[4].length > 1) {
                                toAppend = toAppend + connection + "<wbr>";
                            } else {
                                toAppend = toAppend + connection;
                            }
                        }
                        toAppend = toAppend + "</td>";
                    } else {
                        toAppend = toAppend + "<td></td>";
                    }
                    toAppend = toAppend + "<td class='td_remove_listener' id='td_remove_listener_" + String(key) + "'><button class='red'>X</button>   <i class='fa fa-circle-o-notch fa-spin' id='i_remove_listener_spinner_" + String(key) + "'></i></td></tr>";
                    $("#table_listeners").append(toAppend);
                }
                $("#table_listeners tr:gt(0)").each(function () {
                    let id = $(this).find("td").eq(6).attr('id').split("_")[3];
                    $("#i_remove_listener_spinner_" + id).hide();
                    if ($(this).find("td").eq(5).text() !== "") {
                        $(this).css("background-color", "#4974a9");
                    } else {
                        $(this).css("background-color", "#36393e");
                    }
                });
                listenerSettings();
            }
        } else {
            if ($("#table_listeners :focus").attr('id') === undefined) {
                $("#table_listeners").find("tr:gt(0)").remove();
                listenerSettings();
            }
        }
    }
});
function closeMessageMonitor() {
    let elmt;
    if (MonitorGlobals.error) {
        elmt = $("#error");
    } else {
        elmt = $("#success");
    }
    elmt.html("");
    elmt.hide();
}