"use strict";
/**
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = preset;
function makePluginConfig(source, options) {
    if (options) {
        return [require.resolve(source), options];
    }
    return require.resolve(source);
}
function preset(context, opts = {}) {
    const { siteConfig } = context;
    const { themeConfig } = siteConfig;
    const { algolia } = themeConfig;
    const isProd = process.env.NODE_ENV === 'production';
    const { debug, kv, cs, ts, blog, community, pages, sitemap, svgr, theme, googleAnalytics, gtag, googleTagManager, ...rest } = opts;
    const themes = [];
    themes.push(makePluginConfig('@docusaurus/theme-classic', theme));
    if (algolia) {
        themes.push(require.resolve('@docusaurus/theme-search-algolia'));
    }
    if ('gtag' in themeConfig) {
        throw new Error('The "gtag" field in themeConfig should now be specified as option for plugin-google-gtag. For preset-openriak, simply move themeConfig.gtag to preset options. More information at https://github.com/facebook/docusaurus/pull/5832.');
    }
    if ('googleAnalytics' in themeConfig) {
        throw new Error('The "googleAnalytics" field in themeConfig should now be specified as option for plugin-google-analytics. For preset-openriak, simply move themeConfig.googleAnalytics to preset options. More information at https://github.com/facebook/docusaurus/pull/5832.');
    }
    const plugins = [];
    // TODO Docusaurus v4: temporary due to the opt-in flag
    // In v4 we'd like to use layers everywhere natively
    if (siteConfig.future.v4.useCssCascadeLayers) {
        plugins.push(makePluginConfig('@docusaurus/plugin-css-cascade-layers'));
    }
    if (kv !== false) {
        const kvConfig = makePluginConfig('@docusaurus/plugin-content-docs', kv);
        //console.log(kvConfig);
        plugins.push(kvConfig);
    }
    if (cs !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-content-docs', cs));
    }
    if (ts !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-content-docs', ts));
    }
    if (blog !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-content-blog', blog));
    }
    if (pages !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-content-pages', pages));
    }
    if (community !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-content-pages', community));
    }
    if (googleAnalytics) {
        plugins.push(makePluginConfig('@docusaurus/plugin-google-analytics', googleAnalytics));
    }
    if (debug || (debug === undefined && !isProd)) {
        plugins.push(require.resolve('@docusaurus/plugin-debug'));
    }
    if (gtag) {
        plugins.push(makePluginConfig('@docusaurus/plugin-google-gtag', gtag));
    }
    if (googleTagManager) {
        plugins.push(makePluginConfig('@docusaurus/plugin-google-tag-manager', googleTagManager));
    }
    if (sitemap !== false && (isProd || debug)) {
        plugins.push(makePluginConfig('@docusaurus/plugin-sitemap', sitemap));
    }
    if (svgr !== false) {
        plugins.push(makePluginConfig('@docusaurus/plugin-svgr', svgr));
    }
    if (Object.keys(rest).length > 0) {
        throw new Error(`Unrecognized keys ${Object.keys(rest).join(', ')} found in preset-openriak configuration. The allowed keys are debug, docs, blog, pages, sitemap, theme, googleAnalytics, gtag, and googleTagManager. Check the documentation: https://docusaurus.io/docs/using-plugins#docusauruspreset-openriak for more information on how to configure individual plugins.`);
    }
    return { themes, plugins };
}
