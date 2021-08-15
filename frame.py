import uniModel as model

import json

import sys
import getopt


class engine:
    def __init__(self):
        self.argv = sys.argv
        self.read()
        self.writeable = json.load(self.fileObj)
        has = False
        for key in self.writeable.keys():
            if key == 'unis':
                has = True
        if not has:
            self.writeable['unis'] = []

    def main(self):
        query = ''
        sortByArg = ''
        helper = 'frame.py' + '\nall: gets saved data' + '\nsave: saves data' + '\n-q, --query <query_string>: passes a query string' + '\n-m, --modify: modification modifier' + \
            '\n-m, --modify: record modification operation modifier' + '\n-d, --delete: record remove operation modifier' + \
            '\n-k, --keys, keys: shows accessible keys' + \
            '\n-s, --sort-by <key>: sorts results by a key'
        self.check()
        try:
            opts, args = getopt.getopt(
                self.argv[1:], "hmq:dps:ak", ["help", "query=", "modify", "delete", "point", "sort-by=", "all", "keys"])
        except getopt.GetoptError:
            print(helper)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print(helper)
                sys.exit()
            if opt in ("-q", "--query"):
                query = arg
            if opt in ("-s", "--sort-by"):
                sortByArg = arg.lower().replace(" ", "")
            if opt in ("-m", "--modify"):
                self.modify(query, sortByArg)
            if opt in ("-d", "--delete"):
                self.delete(query, sortByArg)
            if opt in ("-p", "--point"):
                self.modifyPoints(query, sortByArg)
            if opt in ("-a", "--all"):
                self.all()
            if opt in ("-k", "--keys"):
                print(model.uniModel().onlyLetterDict().keys())
        if query != '':
            self.search(query, sortByArg)

        if 'save' in self.argv[1:]:
            self.save()

        if 'all' in self.argv[1:]:
            self.all(sortByArg)

        if 'keys' in self.argv[1:]:
            self.all(sortByArg)

    def check(self):
        for element in self.writeable['unis']:
            uni = model.uniModel()
            uni.fromJson(element)
            index = self.writeable['unis'].index(element)
            if uni.searchMissing(element):
                self.writeable['unis'][index] = uni.toJson()
                self.overwrite()

    def all(self, order):
        res = []
        for element in self.writeable['unis']:
            uni = model.uniModel()
            uni.fromJson(element)
            res.append(uni)
        print(len(res), 'results found')
        return self.sortBy(res, order)

    def sortBy(self, res, order):
        onlyLetter = res[0].onlyLetterDict()
        if order in onlyLetter.keys():
            res.sort(key=lambda x: x.__dict__[onlyLetter[order]])
        for uni in res:
            print(f'result index {str(res.index(uni))}')
            uni.show()

    def search(self, q, order):
        res = []
        for element in self.writeable['unis']:
            uni = model.uniModel()
            uni.fromJson(element)
            if q in uni.name:
                res.append(uni)
        print(len(res), 'results found')
        return self.sortBy(res, order)

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
        old = self.writeable['unis'].index(results[index].toJson())
        new = results[old].inputFromUser()
        print('='*10)
        self.writeable['unis'][old] = new.toJson()
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
        self.writeable['unis'].remove(selected.toJson())
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
        index = self.writeable['unis'].index(selected.toJson())
        selected.show()
        while True:
            points = input(
                f'change points ({selected.points}) start with + or -: ')
            selected.points += int(points)
            print('=' * 10)
            print('new point value:', selected.points)
            self.writeable['unis'][index] = selected.toJson()
            self.overwrite()

    def append(self, mem):
        self.writeable['unis'] = self.writeable['unis'] + mem
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
    run = engine()
    run.main()
