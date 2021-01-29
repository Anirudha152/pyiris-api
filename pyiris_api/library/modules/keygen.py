# API
# done
import pyiris_api.library.modules.return_random_string as return_random_string
import os


def main(self, overwrite=False, key=None):
    try:
        if key is None:
            key = return_random_string.main(50)
        if not os.path.exists("resources"):
            os.mkdir(os.path.join(os.getcwd(), "resources"))
        if os.path.isfile(os.path.join(os.getcwd(), 'resources', 'PyIris.cred')):
            if overwrite:
                with open('resources/PyIris.cred', 'w') as f:
                    f.write(key)
                    self.log.pos('Overwrote PyIris.cred key file with key as : ' + key)
            else:
                self.log.pos('PyIris.cred key file located - OK')
        else:
            with open('resources/PyIris.cred', 'w') as f:
                f.write(key)
                self.log.pos('Generated PyIris.cred key file with key as : ' + key)
        self.config.key = key
        return {"status": "ok", "message": "Successfully wrote new key", "data": {"key": key}}
    except Exception as e:
        return {"status": "error", "message": str(e), "data": None}
