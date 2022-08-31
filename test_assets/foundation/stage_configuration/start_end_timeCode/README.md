# Start End TimeCode

These files show how animated stages behave for different combinations of `startTimeCode` and `endTimeCode` stage metadata.

The animated prim has time samples from `0` to `100`:

```usda
double3 xformOp:translate.timeSamples = {
    0: (0, 0, 0),
    100: (100, 0, 0),
}
```

## Large values

[large_start_end_timeCodes.usda](./large_start_end_timeCodes.usda)

```usda
endTimeCode = 10000000
startTimeCode = -10000000
```

## Missing both values

[missing_start_end_timeCodes.usda](./missing_start_end_timeCodes.usda)

Neither `endTimeCode` nor `startTimeCode` is set.

## Missing startTimeCode

[missing_startTimeCode.usda](./missing_startTimeCode.usda)

`startTimeCode` is not set.

## Missing endTimeCode

[missing_endTimeCode.usda](./missing_endTimeCode.usda)

`endTimeCode` is not set.

## Value subset

[start_end_timeCodes_subset.usda](./start_end_timeCodes_subset.usda)

```usda
endTimeCode = 70
startTimeCode = 40
```

## Value superset

[start_end_timeCodes_superset.usda](./start_end_timeCodes_superset.usda)

```usda
endTimeCode = -10
startTimeCode = 110
```

## Swapped values

[start_end_timeCodes_swapped.usda](./start_end_timeCodes_swapped.usda)

```usda
endTimeCode = 0
startTimeCode = 100
```
