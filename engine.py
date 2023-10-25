import uniModel as model

import json
import sys
import argparse


class engine:
    def __init__(self, defaultMainKey='mainKey'):
        self.parser = parser = argparse.ArgumentParser(
            description='Engine for handling data.')
        parser.add_argument('commands', metavar='C', type=str,
                            nargs='*', help='commands to execute')
        parser.add_argument('--main-key', dest='mainKey', action='store',
                            default=defaultMainKey, help='sets the main-key to be read from JSON')
        parser.add_argument('-q', '--query', dest='query',
                            action='store', help='passes a query string', default='')
        parser.add_argument('-s', '--sort-by', dest='sortBy',
                            action='store', help='sorts results by a key', default='')
        parser.add_argument('-m', '--modify', dest='modify',
                            action='store_true', help='modification/modifier')
        parser.add_argument('-d', '--delete', dest='delete',
                            action='store_true', help='record remove operation modifier')
        parser.add_argument('-k', '--keys', dest='keys',
                            action='store_true', help='shows accessible keys')
        parser.add_argument('-a', '--all', dest='all',
                            action='store_true', help='gets saved data')
        parser.add_argument('--save', dest='save',
                            action='store_true', help='saves data')

        args = parser.parse_args()
        self.mainKey = args.mainKey
        self.argquery = args.query
        self.argsortBy = args.sortBy
        self.argmodify = args.modify
        self.argdelete = args.delete
        self.argkeys = args.keys
        self.argall = args.all
        self.argsave = args.save
        self.argcommands = args.commands

        self.read()
        self.writeable = json.load(self.fileObj)
        has = False
        for key in self.writeable.keys():
            if key == self.mainKey:
                has = True
        if not has:
            self.writeable[self.mainKey] = []

    def run(self):
        if 'help' in self.argcommands:
            print(self.parser.format_help())
            sys.exit()

        if self.argquery:
            self.search(self.argquery, self.argsortBy)

        if self.argmodify:
            self.modify(self.argquery, self.argsortBy)

        if self.argdelete:
            self.delete(self.argquery, self.argsortBy)

        if self.argall or 'all' in self.argcommands:
            self.all(self.argsortBy)

        if self.argkeys or 'keys' in self.argcommands:
            print(model.uniModel().onlyLetterDict().keys())

        if self.argsave or 'save' in self.argcommands:
            self.save()

    def check(self):
        for element in self.writeable[self.mainKey]:
            uni = model.uniModel()
            uni.fromJson(element)
            index = self.writeable[self.mainKey].index(element)
            if uni.searchMissing(element):
                self.writeable[self.mainKey][index] = uni.toJson()
                self.overwrite()

    def all(self, order):
        res = []
        for element in self.writeable[self.mainKey]:
            uni = model.uniModel()
            uni.fromJson(element)
            res.append(uni)
        print(len(res), 'results found')

        return self.sortBy(res, order)

    def sortBy(self, res, order):
        if not (len(res) > 0):
            return
        onlyLetter = res[0].onlyLetterDict()
        if order in onlyLetter.keys():
            res.sort(key=lambda x: x.__dict__[onlyLetter[order]])
        for uni in res:
            print(f'result index {str(res.index(uni))}')
            uni.show()

    def search(self, q, order):

        res = []
        for element in self.writeable[self.mainKey]:
            uni = model.uniModel()
            uni.fromJson(element)
            if q in uni.name:
                res.append(uni)
        print(len(res), 'results found')
        if self.sortBy is not None:
            return self.sortBy(res, order)
        else:
            return res

    def modify(self, q, order):
        if q != '' and q != ' ':
            results = self.search(q, order)
        else:
            results = self.all(order)
        if results == []:
            print('Nothing to modify')
            exit()
        index = int(
            input('Please enter index of result that modification needed: '))
        old = self.writeable[self.mainKey].index(results[index].toJson())
        new = results[old].inputFromUser()
        print('='*10)
        self.writeable[self.mainKey][old] = new.toJson()
        self.overwrite()
        print('Modified to:')
        new.show()
        print('Successfully Modified')

    def delete(self, q, order):
        if q != '' and q != ' ':
            results = self.search(q, order)
        else:
            results = self.all(order)
        if results == []:
            print('Nothing to delete')
            exit()
        index = int(
            input('Please enter index of result that delete operation needed: '))
        selected = results[index]
        named = selected.name
        print(named)
        self.writeable[self.mainKey].remove(selected.toJson())
        print('=' * 20)
        self.overwrite()
        print(f'{named} named and {str(index)} indexed result successfully deleted')

    def modifyPoints(self, q, order):
        if q != '' and q != ' ':
            results = self.search(q, order)
        else:
            results = self.all(order)
        if results == []:
            print('Not found')
            exit()
        index = int(
            input('Please enter index of result that point addition operation needed: '))
        selected = results[index]
        index = self.writeable[self.mainKey].index(selected.toJson())
        selected.show()
        while True:
            points = input(
                f'change points ({selected.points}) start with + or -: ')
            selected.points += int(points)
            print('=' * 10)
            print('new point value:', selected.points)
            self.writeable[self.mainKey][index] = selected.toJson()
            self.overwrite()

    def append(self, mem):
        self.writeable[self.mainKey] = self.writeable[self.mainKey] + mem
        f = open(self.fileName, 'w')
        f.write(json.dumps(self.writeable))

    def overwrite(self):
        f = open(self.fileName, 'w')
        f.write(json.dumps(self.writeable))
        self.read()

    def read(self):
        self.fileObj = ''
        self.fileName = 'data.json'
        self.fileObj = open(self.fileName, 'r')

    def save(self):
        mem = []
        while True:
            uni = model.uniModel()
            uni.inputFromUser()
            isDone = input('Save more (y/n): ')
            mem.append(uni.toJson())
            print('=' * 20)
            if isDone == 'y' or isDone == 'yes':
                continue
            elif isDone == 'n' or isDone == 'no':
                save = input('Save all (if no print no): ')
                if save == 'n' or save == 'no':
                    break
                self.append(mem)
                break


if __name__ == '__main__':
    engine().run()
