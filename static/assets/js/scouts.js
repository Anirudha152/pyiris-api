ScoutGlobals = {
    "ifc": "",
    "scoutButtonInFocus": false,
    "nameSentToServer": false,
    "reloadedPage": true,
    "isMonitorRunning": "",
    "idOfSelectedButton": "-1",
    "sleepTimeSentToServer": false,
    "canSend": false,
    "$this": undefined,
    "bridgedId": "-1",
    "error": true,
    "shown": {
        "activeWindowsDump": false,
        "browser": false
    }
};
$(document).ready(function () {
    // SCOUTS INTERFACE !!
    function onStart () {
        $("#div_scouts_table_heading").hide();
        $("#div_scouts_table").hide();
        $("#div_direct").hide();
        loader("-1");
        ScoutGlobals.ifc = "Scouts";
    }
    onStart();

    $(document).on('focusout', '.td_scouts_table_name', function () {
        if ($(this).text() !== "" && !ScoutGlobals.scoutButtonInFocus) {
            if (!ScoutGlobals.nameSentToServer) {
                ScoutGlobals.nameSentToServer = true;
                triggerAjax("rename " + $(this).attr('id').split('_')[4] + " " + $(this).text(), true, '/scouts_process', pauseCB, {});
            }
        }
    });
    function pauseCB(data) {
        if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $(".button_scouts_table").click(function() {
        ScoutGlobals.scoutButtonInFocus = true;
        ScoutGlobals.canSend = true;
        tableRowClickable(true);
        loader($(this).attr('id').split('_')[4]);
        ScoutGlobals.$this = $(this);
        $("body").off("click", "#table_scouts tr");
        $("body").on("click", "#table_scouts tr", function(){
            if (ScoutGlobals.canSend && ScoutGlobals.$this.attr('id') !== "button_scouts_table_bridge_0") {
                ScoutGlobals.canSend = false;
                $(".button_scouts_table").prop('disabled', true);
                ScoutGlobals.idOfSelectedButton = ScoutGlobals.$this.attr('id').split('_')[4];
                let command = ScoutGlobals.$this.attr('id').split('_')[3];
                let rowId = $(this).attr('id').split('_')[3];
                $("#i_scouts_table_spinner_" + rowId).show();
                if (command === "sleep") {
                    $("#div_scouts_table_sleep").show();
                    $("#button_scouts_table_scout_sleep_time").click(function() {
                        let time;
                        if ($("#input_scouts_table_scout_sleep_time").val() !== "") {
                            if (parseInt($("#input_scouts_table_scout_sleep_time").val(), 10) > 0) {
                                time = String($("#input_scouts_table_scout_sleep_time").val());
                            }
                            else {
                                time = "10";
                            }
                        } else {
                            time = "10";
                        }
                        $("#input_scouts_table_scout_sleep_time").val("");
                        $("#div_scouts_table_sleep").hide();
                        triggerAjax(command +  " " + rowId + " " + time, true, '/scouts_process', sleepScoutFunctionCB, {"rowId": rowId});
                    });
                    $(".button_scouts_table").prop('disabled', false);
                    return;
                }
                triggerAjax(command +  " " + rowId, true, '/scouts_process', standardScoutFunctionCB, {'command': command, "rowId": rowId});
            }
        });
    });
    function sleepScoutFunctionCB(data, extra_input) {
        ScoutGlobals.idOfSelectedButton = "-1";
        ScoutGlobals.scoutButtonInFocus = false;
        tableRowClickable(false);
        loader("-1");
        $("#i_scouts_table_spinner_" + extra_input.rowId).hide();
        $("body").off("click", "#table_scouts tr")
    }
    function standardScoutFunctionCB(data, extra_input) {
        ScoutGlobals.scoutButtonInFocus = false;
        tableRowClickable(false);
        loader("-1");
        $("#i_scouts_table_spinner_" + extra_input.rowId).hide();
        if (extra_input.command === "ping") {
            if (data.output === "Success") {
                ScoutGlobals.error = false;
                showMessage(data.output_message);
                scrollToTop();
            } else {
                ScoutGlobals.error = true;
                showMessage(data.output_message);
                scrollToTop();
            }
        }
        $(".button_scouts_table").prop('disabled', false);
        ScoutGlobals.idOfSelectedButton = "-1";
        $("body").off("click", "#table_scouts tr")
    }

    // BRIDGING STUFF !!
    $('#button_scouts_table_bridge_0').click(function() {
        ScoutGlobals.idOfSelectedButton = "0";
        ScoutGlobals.scoutButtonInFocus = true;
        ScoutGlobals.canSend = true;
        tableRowClickable(true);
        loader("0");
        $("body").off("click", "#table_scouts tr");
        $("body").on("click", "#table_scouts tr", function(){
            if (ScoutGlobals.idOfSelectedButton === "0") {
                let rowId = $(this).attr('id').split('_')[3];
                $("#i_scouts_table_spinner_" + rowId).show();
                console.log("triggered");
                triggerAjax("bridge " + rowId, true, '/scouts_process', bridgeScoutFunctionCB, {});
            }
        });
    });
    function bridgeScoutFunctionCB(data){
        if (data.output === "Success") {
            ScoutGlobals.scoutButtonInFocus = false;
            ScoutGlobals.idOfSelectedButton = "-1";
            $("#h1_scouts_heading").text("Scout >> " + data.data[1]);
            ScoutGlobals.bridgedId = data.data[0];
            ScoutGlobals.ifc = "Direct";
            $("#div_scouts_table").hide();
            $("#div_scouts_table_heading").hide();
            $("#div_direct").show();
            $("#div_direct_main_load").hide();
            loaderDirect("-1");
            loader("-1");
            $(".i_scouts_table_spinner").hide();

            activeWindowsDumpVisible("0");
            browserVisible("0");

            $("#div_direct_main_load").show();
            triggerAjaxDirectInterface("help", true, loadScoutFunctionsCB, undefined)
        } else {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
            ScoutGlobals.ifc = "Scouts";
        }
    }
    function loadScoutFunctionsCB(data) {
        $("body").off("click", "#table_scouts tr");
        $("#div_direct_main_load").hide();
        if (jQuery.inArray("windows/control/active_windows_dump", data.data) > -1) {
            if(ScoutGlobals.shown.activeWindowsDump) {
                rotate(0, "#img_active_windows_dump_arrow");
                if ($("#table_active_windows_dump tr").length > 1){
                    activeWindowsDumpVisible("2");
                } else {
                    activeWindowsDumpVisible("3");
                }
            } else {
                rotate(270, "#img_active_windows_dump_arrow");
                activeWindowsDumpVisible("1");
            }

        }
        if (jQuery.inArray("windows/control/browser", data.data) > -1) {
            if(ScoutGlobals.shown.browser) {
                rotate(0, "#img_browser_arrow");
                browserVisible("2");

            } else {
                rotate(270, "#img_browser_arrow");
                browserVisible("1");
            }

        }
    }

    // DIRECT FUNCTIONS !!
    $(".button_direct").click(function () {
        let command = $(this).attr('id').split('_')[2];
        let id = $(this).attr('id').split('_')[3];
        loaderDirect(id);
        if (command === "sleep") {
            if (!ScoutGlobals.sleepTimeSentToServer) {
                ScoutGlobals.sleepTimeSentToServer = true;
                $("#div_direct_sleep").show();
                $("#button_direct_scout_sleep_time").unbind("click").click(function () {
                    let time;
                    if ($("#input_direct_scout_sleep_time").val() !== "") {
                        if (parseInt($("#input_direct_scout_sleep_time").val(), 10) > 0) {
                            time = String($("#input_direct_scout_sleep_time").val());
                        } else {
                            time = "10";
                        }
                    } else {
                        time = "10";
                    }
                    $("#input_direct_scout_sleep_time").val("");
                    $("#div_direct_sleep").hide();
                    triggerAjaxDirectInterface(command + " " + time, true, sleepDirectButtonCB, {});
                });
                $(".button_direct").prop('disabled', false);
            }
            return;
        }
        triggerAjaxDirectInterface(command, true, standardDirectButtonCB, {"command": command});
    });
    function standardDirectButtonCB(data, extra_input) {
        if (data.output === "Success") {
            if (data.output_message === "return") {
                if (extra_input.command === "ping"){
                    ScoutGlobals.error = true;
                    showMessage("Scout is dead, removing from database...");
                    scrollToTop();
                }
                ScoutGlobals.ifc = "Scouts";
                loaderDirect("-1");
            } else {
                if (extra_input.command === "ping"){
                    ScoutGlobals.error = false;
                    showMessage(data.output_message);
                    scrollToTop();
                }
                loaderDirect("-1");
            }
        }
    }
    function sleepDirectButtonCB(data) {
        if (data.output_message === "return") {
            ScoutGlobals.sleepTimeSentToServer = false;
            ScoutGlobals.ifc = "Scouts";
            loaderDirect("-1");
        }
    }

    $(".img_arrow").click(function(){
        if ($(this).attr('id') === "img_active_windows_dump_arrow") {
            if (ScoutGlobals.shown.activeWindowsDump) {
                rotate(270, "#img_active_windows_dump_arrow");
                ScoutGlobals.shown.activeWindowsDump = false;
                activeWindowsDumpVisible("1");
            } else {
                rotate(0, "#img_active_windows_dump_arrow");
                ScoutGlobals.shown.activeWindowsDump = true;
                if ($("#table_active_windows_dump tr").length > 1){
                    activeWindowsDumpVisible("2");
                } else {
                    activeWindowsDumpVisible("3");
                }
            }
        } else if ($(this).attr('id') === "img_browser_arrow") {
            if (ScoutGlobals.shown.browser) {
                rotate(270, "#img_browser_arrow");
                ScoutGlobals.shown.browser = false;
                browserVisible("1");
            } else {
                rotate(0, "#img_browser_arrow");
                ScoutGlobals.shown.browser = true;
                browserVisible("2");
            }
        }
    });

    $("#button_active_windows_dump").click(function () {
        $("#i_active_windows_dump_spinner").show();
        triggerAjaxDirectInterface("active", true, activeWindowsDumpCB, undefined )
    });
    function activeWindowsDumpCB(data) {
        $("#i_active_windows_dump_spinner").hide();
        $("#table_active_windows_dump").find("tr:gt(0)").remove();
        if (data.data.length > 1) {
            activeWindowsDumpVisible("2");
            for (let i = 0; i < data.data.length; i++) {
                if (data.data[i] !== "") {
                    $("#table_active_windows_dump").append("<tr><td> - " + data.data[i] + "</td></tr>")
                }
            }
        }
    }


    // SCOUT FUNCTIONS !!
    function loader(toLoad) {
        if (toLoad === "0") {
            $("#i_scouts_table_bridge_0_spinner").show();
        }
        else {
            $("#i_scouts_table_bridge_0_spinner").hide();
        }
        if (toLoad === "1") {
            $("#i_scouts_table_disconnect_1_spinner").show();
        }
        else {
            $("#i_scouts_table_disconnect_1_spinner").hide();
        }
        if (toLoad === "2") {
            $("#i_scouts_table_kill_2_spinner").show();
        }
        else {
            $("#i_scouts_table_kill_2_spinner").hide();
        }
        if (toLoad === "3") {
            $("#i_scouts_table_ping_3_spinner").show();
        }
        else {
            $("#i_scouts_table_ping_3_spinner").hide();
        }
        if (toLoad === "4") {
            $("#i_scouts_table_sleep_4_spinner").show();
        }
        else {
            $("#i_scouts_table_sleep_4_spinner").hide();
        }
    }


    // DIRECT FUNCTIONS !!
    function loaderDirect(toLoad) {
        if (toLoad === "0") {
            $("#i_direct_disconnect_0_spinner").show();
        }
        else {
            $("#i_direct_disconnect_0_spinner").hide();
        }
        if (toLoad === "1") {
            $("#i_direct_kill_1_spinner").show();
        }
        else {
            $("#i_direct_kill_1_spinner").hide();
        }
        if (toLoad === "2") {
            $("#i_direct_ping_2_spinner").show();
        }
        else {
            $("#i_direct_ping_2_spinner").hide();
        }
        if (toLoad === "3") {
            $("#i_direct_sleep_3_spinner").show();
        }
        else {
            $("#i_direct_sleep_3_spinner").hide();
        }
    }

    function activeWindowsDumpVisible(mode) {
        if (mode === "0") {
            $("#div_active_windows_dump").hide();
        } else if (mode === "1") {
            $("#div_active_windows_dump").show();
            $("#div_active_windows_dump_heading").show();
            $("#div_active_windows_dump_content").hide();
            $("#table_active_windows_dump").hide();
            $("#i_active_windows_dump_spinner").hide();
        } else if (mode === "2") {
            $("#div_active_windows_dump").show();
            $("#div_active_windows_dump_heading").show();
            $("#div_active_windows_dump_content").show();
            $("#table_active_windows_dump").show();
            $("#i_active_windows_dump_spinner").hide();
        } else if (mode === "3") {
            $("#div_active_windows_dump").show();
            $("#div_active_windows_dump_heading").show();
            $("#div_active_windows_dump_content").show();
            $("#table_active_windows_dump").hide();
            $("#i_active_windows_dump_spinner").hide();
        }
    }

    function browserVisible(mode) {
        if (mode === "0") {
            $("#div_browser").hide()
        } else if (mode === "1") {
            $("#div_browser").show();
            $("#div_browser_content").hide();
        } else if (mode === "2") {
            $("#div_browser").show();
            $("#div_browser_content").show();
        }
    }


    // GLOBAL FUNCTIONS !!
    function showMessage(msg){
        let elmt;
        if (ScoutGlobals.error) {
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
                if (extra_input !== undefined) {
                    callback(recvData, extra_input);
                }
                else {
                    callback(recvData);
                }
            }
        });
    }

    function triggerAjaxDirectInterface(data, async, callback, extra_input) {
        $.ajax({
            data: {
                command: data,
                scoutId: ScoutGlobals.bridgedId
            },
            type: 'POST',
            async: async,
            url: '/direct_process',
            success: function (recvData) {
                if (extra_input !== undefined) {
                    callback(recvData, extra_input);
                }
                else {
                    callback(recvData);
                }
            }
        });
    }

    function rotate(degree, arrow_id) {
        $(arrow_id).css({ WebkitTransform: 'rotate(' + String(degree) + 'deg)'});
    }
});

function tableRowClickable(clickable){
        if(clickable) {
            $("#table_scouts tr").not(":first").each(function() {
                $(this).addClass('clickable');
            })
        }
        else {
            $("#table_scouts tr").not(":first").each(function() {
                $(this).removeClass('clickable');
            })
        }
    }

function closeMessage(){
    let elmt;
    if (ScoutGlobals.error) {
        elmt = document.getElementById("error");
    } else {
        elmt = document.getElementById("success");
    }
    elmt.innerHTML = "";
    elmt.classList.remove('show');
    elmt.classList.add('hide');
}