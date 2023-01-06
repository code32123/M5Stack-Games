# M5Stack games
 Some m5stack games

Run with [micropython 1.18](https://micropython.org/download/) with [this ili9342 library](https://github.com/russhughes/ili9342c_mpy) on the [M5stack core grey with the gameboy face](https://shop.m5stack.com/products/face?_pos=8&_sid=92afaea02&_ss=r&variant=17290437623898), which seems to have been discontinued.
You will need to build the firmware from scratch (I did on using linux for windows, which was a challenge but possible).

If you have any issues, need any more information, etc... just add an issue!
I've tried to keep my code relativly clear and well-labeled, but if there is anything I need to add, again, just post an issue!

Includes a bootloader that uses cwd to switch to a directory and run the `main.py` file within

### Planned games (unordered):
- [x] Snakey
- [x] 3D Maze
- [ ] Tetris
- [ ] 3D spinning cube demo
- [ ] 2048
- [ ] tic-tac-toe
