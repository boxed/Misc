import sys
import os
import re

def split_respecting_parens(string, tokenizers=' \t'):
    result = []
    cur_str = ''
    paren_count = 0
    square_paren_count = 0
    for c in string:
        if c == '(':
            paren_count += 1
        elif c == ')':
            paren_count -= 1
        elif c == '[':
            square_paren_count += 1
        elif c == ']':
            square_paren_count -= 1
        elif c in tokenizers and paren_count == 0 and square_paren_count == 0:
            result.append(cur_str)
            cur_str = ''
            continue
        cur_str += c
    result.append(cur_str)
    return result

def split_list(list, chunk_size):
    return [list[offset:offset+chunk_size] for offset in range(0, len(list), chunk_size)]

def fix_method_call(line):
    # method call, these can be nested, that's why I loop here
    while True:
        m = re.match(r'(?P<pre>.*)\[\s*(?P<a>\w*)\s*(?P<b>\w*)\s*(?P<bar>[^]]*)\s*\](?P<post>.*)', line)
        if m and m.groupdict()['b'].strip() != 'for' and not m.groupdict()['bar'].strip().startswith(','):
            line = '%s%s%s' % (m.groupdict()['pre'], convert_to_python_call('%(a)s %(b)s%(bar)s' % m.groupdict()), m.groupdict()['post'])
            m = re.match(r'def self\.(?P<middle>[^(]*\()(?P<rest>.*)', line)
            if m:
                if m.groupdict()['rest'] == ') :':
                    line = 'def %(middle)sself):' % m.groupdict()
                else:
                    line = 'def %(middle)sself, %(rest)s' % m.groupdict()
        else:
            return line

def convert_to_python_call(method_call, add_self=False):
    if re.match(r".*'[^']*(?P<foo>\:).*'", method_call): # if a function has a string as argument with a : in it we ignore it instead of trying to handle this case
        return method_call # pragma: no cover
    m = re.match(r'(?P<object>[^\s]*)\s*(?P<rest>.*)', method_call)
    method_parts = [x for x in split_respecting_parens(m.groupdict()['rest'], ' \t:') if x != '']
    if len(method_parts) == 1:
        return '%s.%s(%s) ' % (m.groupdict()['object'], method_parts[0], 'self' if add_self else '')
    
    keys = []
    values = []
    if add_self:
        values.append('self')

    for key, value in split_list(method_parts, 2):
        keys.append(key)
        values.append(value)

    return '%s.%s_(%s)' % (m.groupdict()['object'], '_'.join(keys), ', '.join(values))

def convert_opy_to_py(source_filename, destination_filename):
    src = open(source_filename, 'r')
    dst = open(destination_filename, 'w')
    for line in src.readlines():
        m = re.match(r'(?P<spaces>\s*)(?P<rest>.*)', line)
        if m:
            foo = m.groupdict()['spaces']+fix_method_call(m.groupdict()['rest'])
            dst.write(foo)
            if not foo.endswith('\n'):
                dst.write('\n')
        else:
            dst.write(line)
    src.close()
    dst.close()

class MetaImporter(object):
    def find_module(self, fullname, path=None):
        lastname = fullname.rsplit('.', 1)[-1]
        for d in (path or sys.path):
            filename = os.path.join(d, lastname + '.opy')
            if os.path.exists(filename):
                convert_opy_to_py(filename, os.path.join(d, lastname+'.py'))

        return None

sys.meta_path = [MetaImporter()]

if __name__ == '__main__':
    import opy_test