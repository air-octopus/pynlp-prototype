def load_file(file_name):
    s = open(file_name).read()

    s = s.replace('\n', ' ')
    s = s.replace('.', ' ')
    s = s.replace(',', ' ')
    s = s.replace(':', ' ')
    s = s.replace(';', ' ')
    s = s.replace('?', ' ')
    s = s.replace('!', ' ')
    s = s.replace('-', ' ')
    s = s.replace('"', ' ')
    s = s.replace('(', ' ')
    s = s.replace(')', ' ')
    s = s.replace('0', ' ')
    s = s.replace('1', ' ')
    s = s.replace('2', ' ')
    s = s.replace('3', ' ')
    s = s.replace('4', ' ')
    s = s.replace('5', ' ')
    s = s.replace('6', ' ')
    s = s.replace('7', ' ')
    s = s.replace('8', ' ')
    s = s.replace('9', ' ')
    s = s.replace('I', ' ')
    s = s.replace('V', ' ')
    s = s.replace('X', ' ')
    s = s.replace('L', ' ')
    s = s.replace('C', ' ')
    s = s.replace('M', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
#    s = s.replace('  ', ' ')
    s = s.lower()

    dat = [ sub for sub in s.split(' ') if sub != '']
    return dat



