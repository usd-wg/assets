# Assets
USD Working Group Assets

This repository will contain USD assets provided under the umbrella of the [ASWF USD WG](https://wiki.aswf.io/display/WGUSD).
At this point the main focus is on assets to be used for basic unit tests.

## Schema-Specific Assets

Schema-specific assets are designed to to aid developers in correctly implementing the handling of various USD schema. The
motivation behind this is that it's often unclear exactly how a specific schema should be imported or exported based on the
schema alone and the unit tests provided by the schema typically don't include written descriptions of intent or reference images
to show how a given asset should appear.

A minimal starting point for schema test assets would be one representative asset per schema, with qualitative & quantitative
descriptions, along with screenshots of what the asset should look like when correctly imported and exported. In addition, the test
asset should offer high-level guidance on round-trip concerns or common issues specific to the schema.
