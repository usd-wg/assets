# TimeCodesPerSecond

These files show the behavior of an animation for different `timeCodesPerSecond` values set, especially edge cases.

The animated prim has time samples from `0` to `100`:

```usda
double3 xformOp:translate.timeSamples = {
    0: (0, 0, 0),
    100: (100, 0, 0),
}
```

- `timeCodesPerSecond = -1` : [timeCodesPerSecond_-1.usda](timeCodesPerSecond_-1.usda)
- `timeCodesPerSecond = 0` : [timeCodesPerSecond_0.usda](timeCodesPerSecond_0.usda)
- `timeCodesPerSecond = 1` : [timeCodesPerSecond_1.usda](timeCodesPerSecond_1.usda)
- `timeCodesPerSecond = 24` : [timeCodesPerSecond_24.usda](timeCodesPerSecond_24.usda)
- `timeCodesPerSecond = 48` : [timeCodesPerSecond_48.usda](timeCodesPerSecond_48.usda)
- `timeCodesPerSecond = 100` : [timeCodesPerSecond_100.usda](timeCodesPerSecond_100.usda)
- `timeCodesPerSecond = 101` : [timeCodesPerSecond_101.usda](timeCodesPerSecond_101.usda)
- `timeCodesPerSecond = 128` : [timeCodesPerSecond_128.usda](timeCodesPerSecond_128.usda)
