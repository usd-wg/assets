# FramesPerSecond and timeCodesPerSecond mixed

These files show the behavior of an animation for a mix of different `framesPerSecond` and `timeCodesPerSecond` values.

The animated prim has time samples from `0` to `100`:

```usda
double3 xformOp:translate.timeSamples = {
    0: (0, 0, 0),
    100: (100, 0, 0),
}
```

## 24 + 24

[24_24.usda](24_24.usda)

```usda
framesPerSecond = 24
timeCodesPerSecond = 24
```

## 24 + 48

[24_48.usda](24_48.usda)

```usda
framesPerSecond = 24
timeCodesPerSecond = 48
```

## 48 + 24

[48_24.usda](48_24.usda)

```usda
framesPerSecond = 48
timeCodesPerSecond = 24
```

## 48 + 48

[48_48.usda](48_48.usda)

```usda
framesPerSecond = 48
timeCodesPerSecond = 48
```
