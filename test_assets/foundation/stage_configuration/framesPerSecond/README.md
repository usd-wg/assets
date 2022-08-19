# FramesPerSecond

These files show the behavior of an animation for different `framesPerSecond` values set, especially edge cases.

The animated prim has time samples from `0` to `100`:

```usda
double3 xformOp:translate.timeSamples = {
    0: (0, 0, 0),
    100: (100, 0, 0),
}
```

- `framesPerSecond = -1` : [framesPerSecond_-1.usda](framesPerSecond_-1.usda)
- `framesPerSecond = 0` : [framesPerSecond_0.usda](framesPerSecond_0.usda)
- `framesPerSecond = 1` : [framesPerSecond_1.usda](framesPerSecond_1.usda)
- `framesPerSecond = 24` : [framesPerSecond_24.usda](framesPerSecond_24.usda)
- `framesPerSecond = 48` : [framesPerSecond_48.usda](framesPerSecond_48.usda)
- `framesPerSecond = 100` : [framesPerSecond_100.usda](framesPerSecond_100.usda)
- `framesPerSecond = 101` : [framesPerSecond_101.usda](framesPerSecond_101.usda)
- `framesPerSecond = 128` : [framesPerSecond_128.usda](framesPerSecond_128.usda)
