# WEB + COM
# done
# Version 1.0.0
import library.modules.bootstrap as bootstrap
import time
import argparse
import library.modules.config as config
import os
import logging
import click

config.main()
parser = argparse.ArgumentParser(description='GUI / CUI')
parser.add_argument('-g', action="store_true", required=False)
parser.add_argument('-c', action="store_true", required=False)
args = parser.parse_args()
if args.g:
    config.interface = "GUI"
elif args.c:
    config.interface = "CUI"

if __name__ == '__main__':
    try:
        start = bootstrap.main()
        interface = config.interface
        if start:
            import library.commands.global_interface.clear as clear
            if interface == "CUI":
                import library.interfaces.home_interface as home_interface
                clear.main()
                home_interface.main()
            elif interface == "GUI":
                import library.interfaces.listener_interface as listener_interface
                import library.interfaces.generator_interface as generator_interface
                import library.interfaces.home_interface as home_interface
                import library.interfaces.scout_interface as scout_interface
                import library.interfaces.direct_interface as direct_interface
                import library.modules.monitor_listeners as monitor_listeners
                from flask import Flask, redirect, url_for, send_from_directory, render_template, request, jsonify
                import sys
                clear.main()
    except EOFError:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            print('[!]User aborted bootstrap, requesting shutdown...')
            quit()
    except KeyboardInterrupt:
        print('[!]User aborted bootstrap, requesting shutdown...')
        quit()
    except Exception as e:
        print('[!]Unexpected Error : ' + str(e))


try:
    import logging
    app = Flask(__name__, static_folder="web_interface/static", template_folder="web_interface/templates")
    app.secret_key = os.urandom(24)
    config.app = app
    logging.getLogger('werkzeug').disabled = True
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    app.logger.info("PyIris Web Interface Started on \033[35mlocalhost\033[0m:\033[35m5000\033[0m")
except Exception as e:
    print(e)
    quit()


@app.route('/')
def redirect_from_root():
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/home', methods=['GET', 'POST'])
def home():
    config.AbruptEnd = True
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    app.logger.info("\n--------------------------------------")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s > %(message)s")
    app.logger.info("[\033[92mHome\033[0m] - " + "Loading page...")
    return render_template('home.html')


@app.route('/generator', methods=['GET', 'POST'])
def generator():
    config.AbruptEnd = True
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    app.logger.info("\n--------------------------------------")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s > %(message)s")
    app.logger.info("[\033[92mGenerator\033[0m] - " + "Loading page...")
    return render_template('generator.html')


@app.route('/listeners', methods=['GET', 'POST'])
def listener():
    config.AbruptEnd = True
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    app.logger.info("\n--------------------------------------")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s > %(message)s")
    app.logger.info("[\033[92mListeners\033[0m] - " + "Loading page...")
    return render_template('listeners.html')


@app.route('/scouts', methods=['GET', 'POST'])
def scouts():
    config.AbruptEnd = True
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    app.logger.info("\n--------------------------------------")
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s > %(message)s")
    app.logger.info("[\033[92mScouts\033[0m] - " + "Loading page...")
    return render_template('scouts.html')


@app.route('/home_process', methods=['GET', 'POST'])
def home_process():
    config.toBridge = False
    config.bridgedTo = None
    app.logger.info("[\033[94mHome_Process\033[0m] - " + request.form['command'])
    output = home_interface.main(request.form['command'])
    return output


@app.route('/generator_process', methods=['GET', 'POST'])
def generator_process():
    config.toBridge = False
    config.bridgedTo = None
    app.logger.info("[\033[94mGenerator_Process\033[0m] - " + request.form['command'])
    output = generator_interface.main(request.form['command'])
    return output


@app.route('/listeners_process', methods=['GET', 'POST'])
def listener_process():
    app.logger.info("[\033[94mListeners_Process\033[0m] - " + request.form['command'])
    if request.form['command'] != None:
        config.toBridge = False
        config.bridgedTo = None
        output = listener_interface.main(request.form['command'])
        return output


@app.route('/scouts_process', methods=['GET', 'POST'])
def scouts_process():
    app.logger.info("[\033[94mScouts_Process\033[0m] - " + request.form['command'])
    output = scout_interface.main(request.form['command'])
    if output is None:
        try:
            if config.toBridge == True:
                output = jsonify({"output": "Success", "output_message": "Bridging successful", "data": config.bridgedTo})
        except Exception as e:
            output = jsonify({"output": "Fail", "output_message": str(e), "data": ""})
    return output


@app.route('/direct_process', methods=['GET', 'POST'])
def direct_process():
    app.logger.info("[\033[94mDirect_Process\033[0m] - " + request.form['command'])
    output = direct_interface.main(request.form['scoutId'], request.form['command'])
    if output == "back":
        output = jsonify({"output": "Success", "output_message": "return", "data": ""})
    return output


@app.route('/monitor_process', methods=['GET', 'POST'])
def monitor_process():
    app.logger.info("[\033[94mMonitor_Process\033[0m] - " + request.form['command'])
    if request.form['command'].split(' ')[0] == "monitor":
        if request.form['command'].split(' ')[1] == "normal":
            output = monitor_listeners.main()
        elif request.form['command'].split(' ')[1] == "reload":
            output = monitor_listeners.check()
        return output



if __name__ == '__main__' and interface == "GUI":
    app.run(debug=True)
