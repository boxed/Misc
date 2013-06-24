# -*- coding: utf-8 -*-
"""
    astutil.mapping_objc
    ~~~~~~~~~~~~~~~

    Various mappings of common Objective-C names to AST symbols.

    :copyright: (c) Copyright 2011 by Armin Ronacher.
    :copyright: (c) Copyright 2011 by Anders Hovmöller.
    :copyright: (c) Copyright 2012 by Jan Weiß.
    :license: BSD, see LICENSE for more details.
"""
import ast


BOOLOP_SYMBOLS = {
    ast.And:        '&&',
    ast.Or:         '||'
}

BINOP_SYMBOLS = {
    ast.Add:        '+',
    ast.Sub:        '-',
    ast.Mult:       '*',
    ast.Div:        '/',
    ast.FloorDiv:   '//',
    ast.Mod:        '%',
    ast.LShift:     '<<',
    ast.RShift:     '>>',
    ast.BitOr:      '|',
    ast.BitAnd:     '&',
    ast.BitXor:     '^'
    ast.Pow:        '**' # CHANGEME: pow is not an operator in ObjC!
}

CMPOP_SYMBOLS = {
    ast.Eq:         '==',
    ast.Gt:         '>',
    ast.GtE:        '>=',
    ast.In:         'in',
    ast.Is:         'is',
    ast.IsNot:      'is not',
    ast.Lt:         '<',
    ast.LtE:        '<=',
    ast.NotEq:      '!=',
    ast.NotIn:      'not in'
}

UNARYOP_SYMBOLS = {
    ast.Invert:     '~',
    ast.Not:        '!',
    ast.UAdd:       '+',
    ast.USub:       '-'
}

ALL_SYMBOLS = {}
ALL_SYMBOLS.update(BOOLOP_SYMBOLS)
ALL_SYMBOLS.update(BINOP_SYMBOLS)
ALL_SYMBOLS.update(CMPOP_SYMBOLS)
ALL_SYMBOLS.update(UNARYOP_SYMBOLS)


def lookup_node(name):
    rv = getattr(ast, name, None)
    if rv is not None:
        try:
            if issubclass(rv, ast.AST):
                return rv
        except TypeError:
            pass
    raise LookupError('Node %r not found' % name)
