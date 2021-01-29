# API
# done


def main(self, to_show):
    try:
        if to_show == 'options':
            header = [['    Option', 'Value', 'Info'], ['    ======', '=====', '====']]
            for o, v in self.config.listener_values.items():
                header.append(['    ' + o, str(v[0]), v[1]])
            self.log.blank('\n')
            l = [len(max(i, key=len)) for i in zip(*header)]
            self.log.blank('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l))) for item in header) + '\n')
            return {"status": "ok", "message": "", "data": {"listener_values": self.config.listener_values}}
        elif to_show == 'listeners':
            header = [['    ID', 'Name', 'Socket Address'],
                      ['    ==', '====', '==============']]
            tmp_list = []
            for i in self.config.listener_database:
                tmp_list.append([i, self.config.listener_database[i][2],
                                 self.config.listener_database[i][0] + ':' + str(self.config.listener_database[i][1])])
            tmp_list.sort()
            for i in tmp_list:
                header.append(['    ' + i[0], i[1], i[2]])
            l = [len(max(i, key=len)) for i in zip(*header)]
            self.log.blank('\n')
            self.log.blank('\n'.join('     '.join(item[i].ljust(l[i]) for i in range(len(l)))
                            for item in header) + '\n')
            return {"status": "ok", "message": "", "data": {"listener_database": self.config.listener_database}}
        else:
            self.log.err('Please specify a valid argument to show, ["options"|"listeners"]')
            return {"status": "error", "message": 'Please specify a valid argument to show, ["options"|"listeners"]', "data": None}
    except IndexError as e:
        self.log.err('Please specify a valid argument to show, ["options"|"listeners"]')
        return {"status": "error", "message": 'Please specify a valid argument to show, ["options"|"listeners"]', "data": None}
