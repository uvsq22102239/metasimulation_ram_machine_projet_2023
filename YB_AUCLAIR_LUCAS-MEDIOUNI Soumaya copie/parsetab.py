
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD BREAK DIV IF LIGNE MOD MULT WHILEcode : LIGNEcode : code LIGNEcode : code WHILEcode : code IF'
    
_lr_action_items = {'LIGNE':([0,1,2,3,4,5,],[2,3,-1,-2,-3,-4,]),'$end':([1,2,3,4,5,],[0,-1,-2,-3,-4,]),'WHILE':([1,2,3,4,5,],[4,-1,-2,-3,-4,]),'IF':([1,2,3,4,5,],[5,-1,-2,-3,-4,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'code':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> code","S'",1,None,None,None),
  ('code -> LIGNE','code',1,'p_code_ligne','ram_to_python.py',148),
  ('code -> code LIGNE','code',2,'p_code_code_ligne','ram_to_python.py',152),
  ('code -> code WHILE','code',2,'p_code_code_WHILE','ram_to_python.py',156),
  ('code -> code IF','code',2,'p_code_code_IF','ram_to_python.py',167),
]
