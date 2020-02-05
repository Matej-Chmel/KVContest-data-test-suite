from random import randint
from src.common import storage
from src.dataset_generator import data

class Implementation:
    cyc_cmd = None

I = Implementation

def add_line() -> str:
    key, val = None, None
    while True:
        cmd_tuple = next(I.cyc_cmd)
        if cmd_tuple[0] == 'H':
            h_len = next(data.cyc_H_len)
            key = ' '.join([
                next(data.new_key_generator())
                if next(data.cyc_key_is_new)
                else data.existing_key_else_new()
                for i in range(h_len)
            ])
        else:
            try:
                key = next(data.new_key_generator()) if cmd_tuple[1] else data.existing_key()
            except KeyError:
                continue
            if cmd_tuple[0] == 'S':
                val = data.rnd_value(next(data.cyc_val_len))
            elif cmd_tuple[0] == 'A':
                current_len = len(storage[key])
                available_len = data.value_len.max - current_len
                if available_len < data.append_len.min:
                    continue
                val = data.rnd_value(randint(data.append_len.min, min([available_len, data.append_len.max])))
        return f"{cmd_tuple[0]} {key}{' ' + val if val else ''}"
