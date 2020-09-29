# rrgen

A rope-race map generator for the game Worms Armageddon (v3.6.28.0 and later)

## Dependencies

The only dependency is pypng

```
pip install -r requirements.txt
```

## Usage

```
usage: rrgen.py [-h] [-o OUTPUT] [-c COLOR] [--colors] [--hide-arrows]
                [--hide-start] [--hide-finish] [--hide-github]
                [--cell-size CELL_SIZE] [--wall-thickness WALL_THICKNESS]
                [--width WIDTH] [--height HEIGHT] [--padding PADDING]
                [--seed SEED] [--show-seed] [--show-path] [--ignore-warning]
                [--method {1,2}] [--tolerance TOLERANCE] [--path PATH]
                [--start {bottom_left,top_left,top_right,bottom_right} | --start-at X Y]

Generates a rope race map for the game Worms Armageddon

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        The output file (default: ./rrgen.png)
  -c COLOR, --color COLOR
                        The color of the map. Can be any of the CSS color
                        keywords except black. Try --colors to see all
                        available colors (default: randomly chosen keyword
                        color)
  --colors              Lists all available keyword colors. A map is not
                        generated if --colors is passed
  --hide-arrows         Hides the arrows
  --hide-start          Hides the S in the start cell
  --hide-finish         Hides the F in the end cell
  --hide-github         Hides the github link T.T
  --cell-size CELL_SIZE
                        The size of each square cell in pixels (default: 200)
  --wall-thickness WALL_THICKNESS
                        The thickness of the wall in pixels (default: 5)
  --width WIDTH         The width of the map in number of cells/squares
                        (default: 30)
  --height HEIGHT       The height of the map in number of cells/squares
                        (default: 20)
  --padding PADDING     The padding around the whole map in pixels (default:
                        32)
  --seed SEED           The seed used to generate the map
  --show-seed           Show the seed used to generate the map
  --show-path           Show the string version of the generated path
  --ignore-warning      Supresses the warning about big maps
  --method {1,2}        Choses the method to generate the path. Method 1
                        randomly walks until it becomes trapped, then it
                        performs backbite moves until it finds an exit. Method
                        2 first generates a naive path, then applies 20
                        backbites for each cell in the map to randomize the
                        path. Method 2 can' be used with --start-at. Both
                        methods have similar execution times (default: 1)
  --tolerance TOLERANCE
                        Indicates the amount of "holes" in the map in
                        percentage. For example, a tolerance of 0.2 will
                        accept a map with 20% of holes instead of backbiting
                        when it becomes trapped. The holes are not uniformly
                        distributed, though. This options only works with
                        method 1 (default: 0.0)
  --path PATH           Use a string to generate a path instead of randomizing
                        one. The path must be a string composed only of the
                        letters: r, l, u, and d (meaning right, left, up, and
                        down, respectively). If --path is passed, all options
                        related to random generation are ignored
  --start {bottom_left,top_left,top_right,bottom_right}
                        Sets one of the four corners as the starting position
                        (default: bottom_left)
  --start-at X Y        Sets the start at a custom location. X and Y must be
                        within boundaries (counted in cells/squares, not
                        pixels): 0 <= X < WIDTH and 0 <= Y < HEIGHT
```

## Defaults

The default settings were chosen by simple testing. A cell size of 200px with a wall thickness of 5px felt the best for a BigRR map. Another good configuration is 100px cell size with 1px wall thickness, for an old-style rr map. From my experience, the start is usually at the bottom left corner, so I kept that as a default.

The default grid dimensions are 30 cells wide by 20 tall. This amount takes around 7 minutes to complete alone, so a game with 3 players might take around 20 minutes. These dimensions can be randomly generated pretty quickly. When I played a 50x50 map alone, it took me upwards of 30 minutes to finish it playing alone and my hands got pretty tired. So take that into consideration when deciding the size of the grid.


## Arrows

I decided to put arrows only on the top corners to avoid becoming too cluttered. But I might consider adding the bottom ones

## Methods

### Method 1

This method randomly walks through the grid until it has no available neighbors. Then it performs a movement called 'backbite' in which it chooses one of the neighbors, removes the original edge of that neighbor and invert every edge from the cycle that was formed. After a backbite, the new end might already be "trapped", so a new backbite must be made until it finds an opening. Sometimes it takes several backbites to find a continuation and since it's random, it means that filling the whole grid might take a long time for very large grids.

There's a tolerance parameter that can be passed to allow for cells in the grid to be unvisited. However, the "holes" in the map aren't evenly distributed across the map because of the way the path building works. This means the map isn't too pretty with large tolerances.

This algorithm is explained in more detail in these links:

* https://web.archive.org/web/20170707133535/https://www.princeton.edu/~achaney/tmve/wiki100k/docs/Hamiltonian_path_problem.html
* https://stackoverflow.com/a/15904295/1694726 -- but without the diagonal edges


### Method 2

This method first generates a naive map to fill the whole grid and then performs 20 backbite moves for each cell in the grid, as suggested by the paper *Secondary Structures in Long Compact Polymers* (Berdorf, R.; Ferguson, A.; Jacobsen, J.L.; Kondev, J.). This method has more of a definite amount of runtime, but it seems to be comparable to method 1. For maps up to 50x50, the times seem to be very similar. And I did generate a 100x100 map with method 2 and it took 48 minutes on a 2010-ish i3-350M processor.

Links:

* https://stackoverflow.com/a/20056736/1694726 -- The .initComplexMap() method
* https://stackoverflow.com/a/27110551/1694726


### Custom path

You can provide a custom path with the `--path` parameter. This was one of the things I wanted to do initially, but ended up being pretty much the last thing I implemented. The custom path needs to be a string of movements with the letters 'r', 'l', 'u', and 'd' (meaning right, left, up, and down, respectively). The path must not overlap. For example: `--path rrrrrrrrrrullllllllllurrrrrrrrrrullllllllll` generates a horizontal zig-zag map.

It can also be used if you want an external path generation method. You just have to output the string representation of your path and pass into this parameter.
