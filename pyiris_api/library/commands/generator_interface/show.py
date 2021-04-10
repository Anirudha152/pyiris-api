# API
# done


def main(self, to_show):
    try:
        if to_show == 'options':
            header = [['    Option', 'Value', 'Info'], ['    ======', '=====', '====']]
            for o, v in self.config.scout_values.items():
                header.append(['    ' + o, str(v[0]), v[1]])
            l = [len(max(i, key=len)) for i in zip(*header)]
            to_print = '\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                            for item in header)
            for line in to_print.split("\n"):
                self.log.blank(line.strip())
            return {"status": "ok", "message": "", "data": {"scout_values": self.config.scout_values}}
        elif to_show == "bases":
            if self.config.scout_values['Windows'][0] == 'True':
                self.log.blank('\n')
                self.log.inf('Generator is set to generate Windows scout')
                self.log.inf('All loadable Windows bases :')
                for i in self.config.win_bases:
                    self.log.blank('   [' + i + '] ' + self.config.win_bases[i])
                self.log.blank('')
                return {"status": "ok", "message": "", "data": {"win_bases": self.config.win_bases}}
            else:
                self.log.blank('\n')
                self.log.inf('Generator is set to generate Linux scout')
                self.log.inf('All loadable Linux bases :')
                for i in self.config.lin_bases:
                    self.log.blank('   [' + i + '] ' + self.config.lin_bases[i])
                self.log.blank('')
                return {"status": "ok", "message": "", "data": {"lin_bases": self.config.lin_bases}}
        elif to_show == "components":
            if self.config.scout_values['Windows'][0] == 'True':
                self.log.blank('\n')
                self.log.inf('Generator is set to generate Windows scout')
                self.log.inf('All loadable Windows components :')
                for i in self.config.win_components:
                    self.log.blank('   [' + i + '] ' + self.config.win_components[i])
                self.log.blank('')
                return {"status": "ok", "message": "", "data": {"win_components": self.config.win_components}}
            else:
                self.log.blank('\n')
                self.log.inf('Generator is set to generate Linux scout')
                self.log.inf('All loadable Linux components :')
                for i in self.config.lin_components:
                    self.log.blank('   [' + i + '] ' + self.config.lin_components[i])
                self.log.blank('')
                return {"status": "ok", "message": "", "data": {"lin_components": self.config.lin_components}}
        elif to_show == 'encoders':
            self.log.blank('')
            self.log.inf('All encoders :')
            for i in self.config.encoders:
                self.log.blank('   [' + i + '] ' + self.config.encoders[i])
            self.log.blank('')
            return {"status": "ok", "message": "", "data": {"encoders": self.config.encoders}}
        elif to_show == 'loaded':
            if self.config.scout_values['Windows'][0] == 'True':
                self.log.inf('Generator is set to generate Windows specific scout')
            else:
                self.log.inf('Generator is set to generate Linux specific scout')
            self.log.inf('Loaded base : \n[base] ' + self.config.loaded_base)
            self.log.inf('Loaded components : ')
            for i in self.config.loaded_components:
                self.log.blank('   [' + i + '] ' + self.config.loaded_components[i])
            self.log.blank('\n')
            self.log.inf('Encoder stack (Scout is encoded by the top encoder first then the next all the way to the bottom) : ')
            for i in range(len(self.config.loaded_encoders)):
                self.log.blank('   [' + str(i) + '] ' + self.config.loaded_encoders[i])
            self.log.blank('')
            return {"status": "ok", "message": "", "data": {"loaded_base": self.config.loaded_base, "loaded_components": self.config.loaded_components, "loaded_encoders": self.config.loaded_encoders}}
        else:
            self.log.err('Please specify a valid argument, ["options"|"bases"|"components"|"loaded"|"encoders"]')
            return {"status": "error", "message": "Please specify a valid argument, [\"options\"|\"bases\"|\"components\"|\"loaded\"|\"encoders\"]", "data": None}
    except IndexError as e:
        self.log.err("Please specify a valid argument, [\"options\"|\"bases\"|\"components\"|\"loaded\"|\"encoders\"]")
        return {"status": "error", "message": "Please specify a valid argument, [\"options\"|\"bases\"|\"components\"|\"loaded\"|\"encoders\"]", "data": None}
