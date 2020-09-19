import argparse


parser = argparse.ArgumentParser(
    description='Generates a rope race map for the game Worms Armageddon')

parser.add_argument('-o', '--output',
    help='The output file (default: ./rrgen.png)',
    default='./rrgen.png')
parser.add_argument('-c', '--color',
    help='The color of the map. Can be any of the CSS color keywords except black. '
    'Try --colors to see all available colors '
    '(default: randomly chosen keyword color)')
parser.add_argument('--colors',
    help='Lists all available keyword colors. '
    'A map is not generated if --colors is passed',
    action='store_true')
parser.add_argument('--hide-arrows',
    help='Hides the arrows',
    action='store_true')
parser.add_argument('--hide-start',
    help='Hides the S in the start cell',
    action='store_true')
parser.add_argument('--hide-finish',
    help='Hides the F in the end cell',
    action='store_true')
parser.add_argument('--hide-github',
    help='Hides the github link T.T',
    action='store_true')
parser.add_argument('--cell-size',
    help='The size of each square cell in pixels (default: 200)',
    type=int, default=200)
parser.add_argument('--wall-thickness',
    help='The thickness of the wall in pixels (default: 5)',
    type=int, default=5)
parser.add_argument('--width',
    help='The width of the map in number of cells/squares (default: 30)',
    type=int, default=30)
parser.add_argument('--height',
    help='The height of the map in number of cells/squares (default: 20)',
    type=int, default=20)
parser.add_argument('--padding',
    help='The padding around the whole map in pixels (default: 32)',
    type=int, default=32)
parser.add_argument('--seed',
    help='The seed used to generate the map',
    type=int)
parser.add_argument('--show-seed',
    help='Show the seed used to generate the map',
    action='store_true')
parser.add_argument('--show-path',
    help='Show the string version of the generated path',
    action='store_true')
parser.add_argument('--path',
    help='[NOT IMPLEMENTED] '
        'Use a string to generate a path instead of randomizing one. '
        'The path must be a string composed only of the letters: r, l, u, and d '
        '(meaning right, left, up, and down, respectively). '
        'If --path is passed, all options related to random generation are ignored')
