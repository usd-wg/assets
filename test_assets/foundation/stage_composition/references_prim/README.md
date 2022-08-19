# References prim

These files show how to reference prims directly.

## References prim in other file

![screenshot](screenshots/reference_prim_in_other_file_usdrecord_22.08.png)
_reference_prim_in_other_file.usda, usdrecord 22.08_

[reference_prim_in_other_file.usda](reference_prim_in_other_file.usda) contains three prim references in other files:

- `Cube_with_reference` references an existing mesh
- `Cube_invalid_reference` references a non existing mesh in a valid file
- `Cube_invalid_file_reference` references an non existing mesh in an invalid file

## References prims in same file

![screenshot](screenshots/reference_prim_in_same_file_usdrecord_22.08.png)
_reference_prim_in_same_file.usda, usdrecord 22.08_

[reference_prim_in_same_file.usda](reference_prim_in_same_file.usda) contains two prim references within the same file:

- `Cube_with_reference` references an existing mesh
- `Cube_with_invalid_reference` references an non existing mesh
