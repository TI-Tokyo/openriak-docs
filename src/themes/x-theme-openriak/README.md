# Docusaurus Theme openriak

The OpenRiak theme for Docusaurus.

## Installation

Add `openriak/theme-openriak` to your package:

```bash
npm i @openriak/theme-openriak
# or
yarn add @openriak/theme-openriak
```

Modify your `docusaurus.config.js`:

```diff
module.exports = {
  ...
+ themes: ['@openriak/theme-openriak'],
  ...
}
```

## Swizzling components

```bash
$ npm swizzle @openriak/theme-openriak [component name]
```

All components used by the source theme can be found [here](https://github.com/facebook/docusaurus/tree/main/packages/openriak-theme-openriak/src/theme)
