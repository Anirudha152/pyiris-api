# API
# done


def main(self, to_show):
    try:
        if to_show == 'scouts':
            header = [['    ID', 'Name', '[Scout] -> [Listener]', 'Connection Type'],
                      ['    ==', '====', '=====================', '===============']]
            tmp_list = []
            for i in self.config.scout_database:
                tmp_list.append([i, self.config.scout_database[i][4],
                                 self.config.scout_database[i][1] + ':' + self.config.scout_database[i][2] + ' -> ' +
                                 self.config.scout_database[i][3], self.config.scout_database[i][6]])
            tmp_list.sort()
            for i in tmp_list:
                header.append(['    ' + str(i[0]), i[1], i[2], i[3]])
            l = [len(max(i, key=len)) for i in zip(*header)]
            self.log.blank('\n')
            self.log.blank('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                            for item in header) + '\n')
            return {"status": "ok", "message": "", "data": {"scout_database": self.config.scout_database}}
        elif to_show == 'reverse':
            header = [['    ID', 'Name', '[Scout] -> [Listener]', 'Connection Type'],
                      ['    ==', '====', '=====================', '===============']]
            tmp_list = []
            for i in self.config.scout_database:
                if self.config.scout_database[i][6] == 'Reverse':
                    tmp_list.append([i, self.config.scout_database[i][4],
                                     self.config.scout_database[i][1] + ':' + self.config.scout_database[i][2] + ' -> ' +
                                     self.config.scout_database[i][3], self.config.scout_database[i][6]])
            tmp_list.sort()
            for i in tmp_list:
                header.append(['    ' + str(i[0]), i[1], i[2], i[3]])
            l = [len(max(i, key=len)) for i in zip(*header)]
            self.log.blank('\n')
            self.log.blank('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                            for item in header) + '\n')
            return {"status": "ok", "message": "", "data": {"scout_database": {key: val for key, val in self.config.scout_database.items() if val[6] == "Reverse"}}}
        elif to_show == 'bind':
            header = [['    ID', 'Name', '[Scout] -> [Listener]', 'Connection Type'],
                      ['    ==', '====', '=====================', '===============']]
            tmp_list = []
            for i in self.config.scout_database:
                if self.config.scout_database[i][6] == 'Bind':
                    tmp_list.append([i, self.config.scout_database[i][4],
                                     self.config.scout_database[i][1] + ':' + self.config.scout_database[i][2] + ' -> ' +
                                     self.config.scout_database[i][3], self.config.scout_database[i][6]])
            tmp_list.sort()
            for i in tmp_list:
                header.append(['    ' + str(i[0]), i[1], i[2], i[3]])
            l = [len(max(i, key=len)) for i in zip(*header)]
            self.log.blank('\n')
            self.log.blank('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                            for item in header) + '\n')
            return {"status": "ok", "message": "", "data": {"scout_database": {key: val for key, val in self.config.scout_database.items() if val[6] == "Bind"}}}
        else:
            self.log.err('Please specify a valid argument, ["bind"|"reverse"|"scouts"]')
            return {"status": "error", "message": 'Please specify a valid argument, ["bind"|"reverse"|"scouts"]', "data": None}
    except IndexError as e:
        self.log.err('Please specify a valid argument, ["bind"|"reverse"|"scouts"]')
        raise e
        #return {"status": "error", "message": 'Please specify a valid argument, ["bind"|"reverse"|"scouts"]', "data": None}
