#!/usr/bin/env python3

import argparse
import json


def get_gambit_matrix(payoffs):
    rows = len(payoffs)
    cols = len(payoffs[0])
    payoff_list = []
    indices = []
    for j in range(cols):
        for i in range(rows):
            ele = payoffs[i][j]
            if ele == 0:
                indices.append(0)
            else:
                payoff_list.append(("", ele, -ele))
                indices.append(len(payoff_list))
    # print(payoff_list, indices)
    return payoff_list, indices

def convert_json_to_gbt(json) -> str:
    template = """
<?xml version="1.0" encoding="UTF-8"?>
<gambit:document xmlns:gambit="http://gambit.sourceforge.net/" version="0.1">
<colors>
<player id="-1" red="0" green="0" blue="0" />
<player id="0" red="154" green="205" blue="50" />
<player id="1" red="255" green="0" blue="0" />
<player id="2" red="0" green="0" blue="255" />
</colors>
<font size="10" family="74" face="Arial" style="90" weight="400" />
<numbers decimals="4"/>
<game>
<nfgfile>
NFG 1 R "{title}" {{ "{P1}" "{P2}" }}

{{ {{ {P1-strats-str} }}
{{ {P2-strats-str} }}
}}
"{comment}"

{{
{payoff-list-str}
}}
{indices-str}
</nfgfile>
</game>
</gambit:document>
"""

    json['P1-strats-str'] = ' '.join(f'"{strat}"' for strat in json["P1-strats"])
    json['P2-strats-str'] = ' '.join(f'"{strat}"' for strat in json["P2-strats"])
    payoff_list, indices = get_gambit_matrix(json["payoffs"])
    json['payoff-list-str'] = '\n'.join(f'{{ "{payoff[0]}" {payoff[1]}, {payoff[2]} }}' for payoff in payoff_list)
    # print(json['payoff-list-str'])
    json['indices-str'] = ' '.join([str(index) for index in indices])
    gbt = template.format(**json)
    return gbt

def parse_args():
    parser = argparse.ArgumentParser(description='Convert Tekken mixup zero-sum game into Gambit file.')
    parser.add_argument(dest='input', type=str, help='Input file')
    parser.add_argument('-o', '--output', dest='output_file', type=str, help='Output file destination')
    return parser.parse_args()

def main():
    args = parse_args()
    with open(args.input) as input:
        contents = input.read()
    input_json = json.loads(contents)
    gbt = convert_json_to_gbt(input_json)
    with open(args.output_file, 'w') as output:
        output.write(gbt)

if __name__ == '__main__':
    main()