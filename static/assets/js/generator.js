GeneratorGlobals = {
    "encoderArray": [],
    "mainSettingsShown": false,
    "componentsShown": true,
    "availableEncodersShown": true,
    "miscellaneousSettingsShown": false,
    "loadedEncodersShown": true,
    "modulesArray": [],
    "globalEncoders": undefined,
    "error": true
};
$(document).ready(function () {

    //load all available encoders and components into tables & update all values from server memory
    function reloadAll() {
        $("#table_components").find("tr:gt(0)").remove();
        $("#table_available_encoders").find("tr:gt(0)").remove();
        triggerAjax("more_com all", false, '/generator_process', reloadCompCB, undefined);
        triggerAjax("more_enc all", false, '/generator_process', reloadEncCB, undefined);
        triggerAjax("show loaded", true, '/generator_process', showLoadedCB, undefined);
        MiscSettings();
    }
    function reloadCompCB(data) {
        for (const [key, value] of Object.entries(data.data)) {
            if (data.output === "Success") {
                $('#table_components').append("<tr id='tr_components_" + String(key) + "'><th>" + String(key) + "</th><td>" + value.Name + "</td><td>" + value.Description + "</td><td><label class='label_checkbox_container'><input class = 'input_checkbox_components' id = 'input_checkbox_components_" + String(key) + "' type='checkbox'><span class='checkmark'></span></label></td></tr>");
            }
        }
    }
    function reloadEncCB(data) {
        for (const [key, value] of Object.entries(data.data)) {
            if (data.output === "Success") {
                $('#table_available_encoders').append("<tr id='tr_available_encoders_" + String(key) + "'><th>" + String(key) + "</th><td>" + value.Name + "</td><td>" + value.Description + "</td><td class='td_add_encoder' id='td_add_encoder_" + String(key) + "'><button style='font-size: x-large;'>+</button></td></tr>");
            }
        }
    }
    function showLoadedCB(data){
        if (data.output === "Success") {
            let loaded_encoders = data.data[0];
            let available_encoders = data.data[2];
            for (let i = 0; i < loaded_encoders.length; i++) {
                GeneratorGlobals.encoderArray.push(parseInt(getKeyByValue(available_encoders, loaded_encoders[i]), 10));
            }
            for (let i = 0; i < loaded_encoders.length; i++) {
                $("#table_loaded_encoders").append("<tr id='tr_loaded_encoders_" + String(i) + "'><td>" + String(i) + "</td><td>" + getKeyByValue(available_encoders, loaded_encoders[i]) + "</td><td>" + loaded_encoders[i] + "</td><td class='td_remove_loaded_encoder' id='td_remove_loaded_encoder_" + String(i) + "'><button class='red'>X</button></td></tr>");
            }
            if (data.data[1]["base"] === "windows/bases/reverse_tcp_base") {
                $("#input_checkbox_components_1").prop('checked', true);
                $("#tr_components_1").css("background-color", "#4974a9");
            } else {
                $("#input_checkbox_components_0").prop('checked', true);
                $("#tr_components_0").css("background-color", "#4974a9");
            }

            for (let key in data.data[1]) {
                $("#input_checkbox_components_" + String(key)).prop('checked', true);
                $("#tr_components_" + String(key)).css("background-color", "#4974a9");
            }
            LoadedEncodersSettings();
        }
    }
    reloadAll();

    //load all options from server memory
    triggerAjax("show options", true, '/generator_process', showOptionsCB, undefined);
    function showOptionsCB(data) {
        $("#i_generate_spinner").hide();
        if (data.output === "Success"){
            let host_array = splitString(data.data["Host"][0]);
            for (let i = 0; i < host_array.length; i++) {
                if (host_array.length === 1) {
                    $('#table_host').append("<tr><td class='host'>" + host_array[i] +"</td></tr>");
                } else {
                    $('#table_host').append("<tr><td class='host'>" + host_array[i] +"</td><td class='td_remove_host' id='td_remove_host_" + String(i) + "'><button class='red' >X</button></td></tr>");
                }
            }
            $("#td_port_value").val(data.data["Port"][0]);
            $("#td_timeout_value").val(data.data["Timeout"][0]);

            if (data.data["Windows"][0] === "True") {
                $("#input_checkbox_windows").prop('checked', true);
            } else {
                $("#input_checkbox_windows").prop('checked', false);
            }

            if (data.data["Compile"][0] === "True") {
                $("#input_checkbox_compile").prop('checked', true);
                showCompilerSettings();
            } else {
                $("#input_checkbox_compile").prop('checked', false);
                hideCompilerSettings();
            }

            //arrow stuff
            if(GeneratorGlobals.mainSettingsShown) {
                rotate(0, "#img_main_settings_arrow");
                $("#div_main_settings").show();
            } else {
                rotate(270, "#img_main_settings_arrow");
                $("#div_main_settings").hide();
            }

            if(GeneratorGlobals.componentsShown) {
                rotate(0, "#img_components_arrow");
                $("#table_components").show();
            } else {
                rotate(270, "#img_components_arrow");
                $("#table_components").hide();
            }

            if(GeneratorGlobals.availableEncodersShown) {
                rotate(0, "#img_available_encoders_arrow");
                $("#table_available_encoders").show();
            } else {
                rotate(270, "#img_available_encoders_arrow");
                $("#table_available_encoders").hide();
            }

            if(GeneratorGlobals.miscellaneousSettingsShown) {
                rotate(0, "#img_miscellaneous_settings_arrow");
            } else {
                rotate(270, "#img_miscellaneous_settings_arrow");
            }
            MiscSettings();

            if (GeneratorGlobals.loadedEncodersShown) {
                rotate(0, "#img_loaded_encoders_arrow");
            } else {
                rotate(270, "#img_loaded_encoders_arrow");
            }
            LoadedEncodersSettings();
        }
    }

    //arrow click event
    $(".img_arrow").click(function(){
        if ($(this).attr('id') === "img_main_settings_arrow") {
            if (GeneratorGlobals.mainSettingsShown) {
                rotate(270, "#img_main_settings_arrow");
                GeneratorGlobals.mainSettingsShown = false;
                $("#div_main_settings").hide();
            } else {
                rotate(0, "#img_main_settings_arrow");
                GeneratorGlobals.mainSettingsShown = true;
                $("#div_main_settings").show();
            }
        } else if ($(this).attr('id') === "img_components_arrow"){
            if(GeneratorGlobals.componentsShown) {
                rotate(270, "#img_components_arrow");
                GeneratorGlobals.componentsShown = false;
                $("#table_components").hide();
            } else {
                rotate(0, "#img_components_arrow");
                GeneratorGlobals.componentsShown = true;
                $("#table_components").show();
            }
        }
        else if ($(this).attr('id') === "img_available_encoders_arrow") {
            if (GeneratorGlobals.availableEncodersShown) {
                rotate(270, "#img_available_encoders_arrow");
                GeneratorGlobals.availableEncodersShown = false;
                $("#table_available_encoders").hide();
            } else {
                rotate(0, "#img_available_encoders_arrow");
                GeneratorGlobals.availableEncodersShown = true;
                $("#table_available_encoders").show();
            }
        }
        else if ($(this).attr('id') === "img_miscellaneous_settings_arrow") {
            if (GeneratorGlobals.miscellaneousSettingsShown) {
                rotate(270, "#img_miscellaneous_settings_arrow");
                GeneratorGlobals.miscellaneousSettingsShown = false;
            } else {
                rotate(0, "#img_miscellaneous_settings_arrow");
                GeneratorGlobals.miscellaneousSettingsShown = true;
            }
            MiscSettings();
        }
        else if ($(this).attr('id') === "img_loaded_encoders_arrow") {
            if (GeneratorGlobals.loadedEncodersShown) {
                rotate(270, "#img_loaded_encoders_arrow");
                GeneratorGlobals.loadedEncodersShown = false;
            } else {
                rotate(0, "#img_loaded_encoders_arrow");
                GeneratorGlobals.loadedEncodersShown = true;
            }
            LoadedEncodersSettings();
        }
     });

    //hostname_button click event
    $("#button_host").click(function () {
        if ($("#input_host").val() !== "") {
            let command = "set Host " + getColumn("String") + ", " + $("#input_host").val();
            triggerAjax(command, true, '/generator_process', addHostCB, undefined);
        }
    });
    function addHostCB(data) {
        if (data.output === "Success") {
            $("#table_host").find("tr:gt(1)").remove();
            let hostArray = splitString(data.data["Host"][0]);
            if (hostArray.length === 1) {
                $('#table_host').append("<tr><td class='host'>" + hostArray +"</td></tr>");
            } else {
                for (let i = 0; i < hostArray.length; i++) {
                    $('#table_host').append("<tr><td class='host'>" + hostArray[i] + "</td><td class='td_remove_host' id='td_remove_host_" + String(i) + "'><button class='red' >X</button></td></tr>");
                }
            }
            $("#input_host").val("");
        }
    }

    //port_button click event
    $("#button_port").click(function () {
        if($("#input_port").val() !== "") {
            triggerAjax("set Port " + $("#input_port").val(), true, '/generator_process', setPortCB, undefined);
        }
    });
    function setPortCB(data) {
        if (data.output === "Success") {
            $("#td_port_value").html(data.data["Port"][0]);
            $("#input_port").val("");
        } else {
            GeneratorGlobals.error = true;
            showMessage("Invalid Port Number. Please enter a new one");
            $("#input_port").val("");
            scrollToTop();
        }
    }

    //timeout_button click event
    $("#button_timeout").click(function () {
        if($("#input_timeout").val() !== "") {
            triggerAjax("set Timeout " + $("#input_timeout").val(), true, '/generator_process', setTimeoutCB, undefined);
        }
    });
    function setTimeoutCB(data) {
        if (data.output === "Success") {
            $("#td_timeout_value").html(data.data["Timeout"][0]);
            $("#input_timeout").val("");
        } else {
            GeneratorGlobals.error = true;
            showMessage("Invalid Timeout. Please enter a valid time");
            $("#input_timeout").val("");
            scrollToTop();
        }
    }

    //compile_checkbox click event
    $("#input_checkbox_compile").on('change', function () {
        if ($(this).is(':checked')) {
            showCompilerSettings();
            triggerAjax("set Compile True", true, '/generator_process', undefined, undefined);
        } else {
            hideCompilerSettings();
            triggerAjax("set Compile False", true, '/generator_process', undefined, undefined);

        }
    });

    //window_checkbox click event
    $("#input_checkbox_windows").on('change', function () {
        if ($(this).is(':checked')) {
            triggerAjax("set Windows True", true, '/generator_process', undefined, undefined);
        } else {
            triggerAjax("set Windows False", true, '/generator_process', undefined, undefined);
        }
        scrollToTop();
        location.reload(true);
    });

    //customFileIconPath
    $("#input_checkbox_compile_custom_icon").click(function () {
        if ($(this).is(':checked')) {
            $("#tr_compile_custom_icon_path").show();
        } else {
            $("#tr_compile_custom_icon_path").hide();
        }
    });

    //hostname_delete click event
    $(document).on("click", ".td_remove_host", function () {
        let id = parseInt($(this).attr('id').split("_")[3], 10);
        let columnArray = getColumn("Array");
        columnArray.splice(id, 1);
        let command = "set Host ";
        for (let i = 0; i < columnArray.length; i++) {
            if (i === columnArray.length - 1) {
                command = command + columnArray[i];
            } else {
                command = command + columnArray[i] + ", ";
            }
        }
        triggerAjax(command, true, '/generator_process', addHostCB, undefined);
    });

    //on component checkbox click event
    $(".input_checkbox_components").click(function () {
        let id = parseInt($(this).attr('id').split("_")[3], 10);
        MiscSettings();
        if ($(this).is(':checked')) {
            $("#tr_components_" + id).css("background-color", "#4974a9");
            if (id === 0) {
                $("#tr_components_1").css("background-color", "#36393e");
                $("#input_checkbox_components_1").prop('checked', false);
            } else if (id === 1) {
                $("#tr_components_0").css("background-color", "#36393e");
                $("#input_checkbox_components_0").prop('checked', false);
            }
            triggerAjax("load_com " + String(id), true, '/generator_process', undefined, undefined);
        } else {
            if (id === 0) {
                $("#input_checkbox_components_0").prop('checked', true);
                $("#tr_components_0").css("background-color", "#4974a9");
            } else if (id === 1) {
                $("#input_checkbox_components_1").prop('checked', true);
                $("#tr_components_1").css("background-color", "#4974a9");
            } else {
                $("#tr_components_" + id).css("background-color", "#36393e");
                triggerAjax("unload_com " + String(id), true, '/generator_process', undefined, undefined);
            }
        }
    });

    //on add encoder click event
    $(".td_add_encoder").click(function () {
        let id = $(this).attr('id').split("_")[3];
        GeneratorGlobals.encoderArray.push(parseInt(id, 10));
        let command = "load_enc ";
        for (let i = 0; i < GeneratorGlobals.encoderArray.length; i++) {
            if (i === GeneratorGlobals.encoderArray.length - 1) {
                command = command + String(GeneratorGlobals.encoderArray[i]);
            } else {
                command = command + String(GeneratorGlobals.encoderArray[i]) + ",";
            }
        }
        triggerAjax(command, true, '/generator_process', addEncoderCB, undefined);
    });
    function addEncoderCB(data) {
        $("#table_loaded_encoders").find("tr:gt(0)").remove();
        let loaded_encoders = data.data[0];
        let available_encoders = data.data[1];
        for (let i = 0; i < loaded_encoders.length; i++){
            $("#table_loaded_encoders").append("<tr id='tr_loaded_encoders_" + String(i) + "'><td>" + String(i) + "</td><td>" + getKeyByValue(available_encoders, loaded_encoders[i]) + "</td><td>" + loaded_encoders[i] + "</td><td class='td_remove_loaded_encoder' id='td_remove_loaded_encoder_" + String(i) + "'><button class='red' >X</button></td></tr>");
        }
        LoadedEncodersSettings();
    }

    //on click of select / deselect all components button
    $("#input_checkbox_components_all").click(function () {
        if ($(this).is(':checked')) {
            triggerAjax("load_com all", true, '/generator_process', undefined, undefined);
            let checkboxes = $("input:checkbox:not(:checked)[class='input_checkbox_components'][id!='input_checkbox_components_0'][id!='input_checkbox_components_1']").not(this);
            checkboxes.parent().parent().parent().css("background-color", "#4974a9");
            checkboxes.prop('checked', true);
        } else {
            triggerAjax("unload_com all", true, '/generator_process', undefined, undefined);
            let checkboxes = $("input:checkbox:checked[class='input_checkbox_components'][id!='input_checkbox_components_0'][id!='input_checkbox_components_1']").not(this);
            checkboxes.parent().parent().parent().css("background-color", "#36393e");
            checkboxes.prop('checked', false);
        }
        MiscSettings();
    });

    //on click of reload all button
    $("#button_reload_all").click(function () {
        location.reload(true);
    });

    //module adder
    $("#button_modules").click(function () {
        if ($("#input_modules").val() !== "") {
            $("#table_modules").find("tr:gt(1)").remove();
            GeneratorGlobals.modulesArray.push($("#input_modules").val());
            GeneratorGlobals.modulesArray = [...new Set(GeneratorGlobals.modulesArray)];
            for (let i = 0; i < GeneratorGlobals.modulesArray.length; i++) {
                $('#table_modules').append("<tr><td class='td_module_to_load'>" + GeneratorGlobals.modulesArray[i] +  "</td><td class='td_remove_module' id='td_remove_module_" + String(i) + "'><button class='red' >X</button></td></tr>");
            }
            $("#input_modules").val("");
        }
    });

    //module remover
    $(document).on("click", ".td_remove_module", function () {
        let id = parseInt($(this).attr('id').split("_")[3], 10);
        GeneratorGlobals.modulesArray.splice(id, 1);
        $("#table_modules").find("tr:gt(1)").remove();
        for (let i = 0; i < GeneratorGlobals.modulesArray.length; i++) {
            $('#table_modules').append("<tr><td class='td_module_to_load'>" + GeneratorGlobals.modulesArray[i] +  "</td><td class='td_remove_module' id='td_remove_module_" + String(i) + "'><button class='red' >X</button></td></tr>");
        }
    });

    //encoder remover
    $(document).on("click", ".td_remove_loaded_encoder", function () {
        let id = parseInt($(this).attr('id').split("_")[4], 10);
        GeneratorGlobals.encoderArray.splice(id, 1);
        let command = "load_enc ";
        for (let i = 0; i < GeneratorGlobals.encoderArray.length; i++) {
            if (i === GeneratorGlobals.encoderArray.length - 1) {
                command = command + String(GeneratorGlobals.encoderArray[i]);
            }
            else {
                command = command + String(GeneratorGlobals.encoderArray[i]) + ",";
            }
        }
        triggerAjax(command, true, '/generator_process', addEncoderCB, undefined);
    });

    //generate
    $("#button_generate").click(function () {
        $("#i_generate_spinner").show();
        let command = "generate ";
        if ($("#input_checkbox_compile").is(":checked")) {
            if ($("#input_checkbox_compile_onefile").is(":checked")) {
                command = command + "1 ";
            } else {
                command = command + "0 ";
            }
            if ($("#input_checkbox_compile_windowed").is(":checked")) {
                command = command + "1 ";
            } else {
                command = command + "0 ";
            }
            if ($("#input_checkbox_compile_custom_icon").is(":checked") && $("#input_compile_custom_icon_path").val() !== "") {
                command = command + "1 " + $("#input_compile_custom_icon_path").val() + " ";
            } else {
                command = command + "0 ";
            }
        } else {
            command = command + "0 0 0 ";
        }
        if (GeneratorGlobals.modulesArray.length > 0) {
            command = command + "1 ";
        } else {
            command = command + "0 ";
        }
        for (let i = 0; i < GeneratorGlobals.modulesArray.length; i++) {
            if (i !== GeneratorGlobals.modulesArray.length - 1){
                command = command + GeneratorGlobals.modulesArray[i] + ",";
            } else {
                command = command + GeneratorGlobals.modulesArray[i] + " ";
            }
        }
        if ($("#input_scout_sleep").val() !== "") {
            let time = parseInt(String($("#input_scout_sleep").val()), 10);
            if (time >= 0) {
                command = command + String(time);
            }
        } else {
            command = command + "60";
        }
        command = command.trim();
        triggerAjax(command, true, '/generator_process', generateCB, undefined);
    });
    function generateCB(data) {
        $("#i_generate_spinner").hide();
        if (data.output === "Fail") {
            GeneratorGlobals.error = true;
            showMessage(data.output_message);
            scrollToTop();
        } else {
            GeneratorGlobals.error = false;
            showMessage(data.output_message);
            scrollToTop();
        }
    }

    // extra functions
    function getKeyByValue(object, value) {
        return Object.keys(object).find(key => object[key] === value);
    }

    function getColumn(p) {
        let arr = [];
        $("#table_host .host").each(function () {
            let val1 = $(this).html();
            arr.push(val1);
        });
        if (p === "String") {
            let string = "";
            for (let i = 0; i < arr.length; i++) {
                if (i === arr.length - 1) {
                    string = string + arr[i];
                } else {
                    string = string + arr[i] + ", ";
                }
            }
            return string;
        } else {
            return arr;
        }
    }

    function splitString(string) {
        let arr = string.split(",");
        for (let i = 0; i < arr.length; i++) {
            arr[i] = arr[i].trim();
        }
        arr = [ ...new Set(arr) ];
        return arr;
    }

    function showMessage(msg){
        let elmt;
        if (GeneratorGlobals.error) {
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

    function showCompilerSettings() {
        $("#tr_compile_onefile").show();
        $("#tr_compile_windowed").show();
        $("#tr_compile_custom_icon").show();
        if ($("#input_checkbox_compile_custom_icon").is(":checked")) {
            $("#tr_compile_custom_icon_path").show();
        } else {
            $("#tr_compile_custom_icon_path").hide();
        }
    }

    function hideCompilerSettings() {
        $("#tr_compile_onefile").hide();
        $("#tr_compile_windowed").hide();
        $("#tr_compile_custom_icon").hide();
        $("#tr_compile_custom_icon_path").hide();
    }

    function rotate(degree, arrow_id) {
        $(arrow_id).css({ WebkitTransform: 'rotate(' + String(degree) + 'deg)'});
    }

    function rowByModuleName(module) {
        return $("#table_components td").filter(function() {
            return $(this).text() === module;
        }).closest("tr").attr('id');
    }

    function MiscSettings() {
        let row_for_modules_id = rowByModuleName("Execute python component").split("_")[2];
        let row_for_sleep_scout_id = rowByModuleName("Sleep startup component").split("_")[2];
        if (!$("#input_checkbox_components_" + String(row_for_sleep_scout_id)).is(":checked") && !$("#input_checkbox_components_" + String(row_for_modules_id)).is(":checked")) {
            $("#div_miscellaneous_settings_heading").hide();
            $("#table_modules").hide();
            $("#table_scout_sleep").hide();
        } else {
            $("#div_miscellaneous_settings_heading").show();
            if (GeneratorGlobals.miscellaneousSettingsShown) {
                if ($("#input_checkbox_components_" + String(row_for_modules_id)).is(":checked")) {
                    $("#table_modules").show();
                } else {
                    $("#table_modules").hide();
                }
                if ($("#input_checkbox_components_" + String(row_for_sleep_scout_id)).is(":checked")) {
                    $("#table_scout_sleep").show();
                } else {
                    $("#table_scout_sleep").hide();
                }
            } else {
                $("#table_modules").hide();
                $("#table_scout_sleep").hide();
            }
        }
    }

    function LoadedEncodersSettings() {
        if ($("#table_loaded_encoders tr").length === 1){
            $("#div_loaded_encoders_heading").hide();
            $("#table_loaded_encoders").hide();
        } else {
            $("#div_loaded_encoders_heading").show();
            if (GeneratorGlobals.loadedEncodersShown) {
                $("#table_loaded_encoders").show();
            } else {
                $("#table_loaded_encoders").hide();
            }
        }
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
    if (GeneratorGlobals.error) {
        elmt = document.getElementById("error");
    } else {
        elmt = document.getElementById("success");
    }
    elmt.innerHTML = "";
    elmt.classList.remove('show');
    elmt.classList.add('hide');
}

