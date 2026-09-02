'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {
  parseSemVer,
  compareSemVer,
  resolveBrand,
  resolveOs,
  resolveValue,
  buildVersionCandidates,
  resolveAssetUrl
} = require('../../layouts/docs-theme/static/js/docs-runtime.js');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const generatedProductsRoot = path.join(repositoryRoot, 'tools', 'generated');
const commonAssets = path.join(repositoryRoot, 'content', 'static', 'common');
const themeRoot = path.join(repositoryRoot, 'layouts', 'docs-theme');
const runtimeSource = fs.readFileSync(path.join(themeRoot, 'static', 'js', 'docs-runtime.js'), 'utf8');
const shellSource = fs.readFileSync(path.join(themeRoot, 'static', 'js', 'docs-shell.js'), 'utf8');
const hugo018ImporterSource = fs.readFileSync(path.join(repositoryRoot, 'tools', 'scripts', 'import_hugo_018.py'), 'utf8');
const searchIndexSource = fs.readFileSync(path.join(themeRoot, 'layouts', '_default', 'section.search.json.json'), 'utf8');
const sharedSearchSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'static', 'js', 'sidebar-search.js'), 'utf8');
const highlightSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'static', 'js', 'search-highlight.js'), 'utf8');
const docsCssSource = fs.readFileSync(path.join(themeRoot, 'static', 'css', 'docs.css'), 'utf8');
const downloadsTemplateSource = fs.readFileSync(path.join(themeRoot, 'layouts', '_default', 'downloads.html'), 'utf8');
const downloadChecksumSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'download-checksum.html'), 'utf8');
const downloadTableSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'download-table.html'), 'utf8');
const downloadCopyIconSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'download-icon-copy.html'), 'utf8');
const downloadHashIconSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'download-icon-hash.html'), 'utf8');
const contactEmailShortcodeSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'shortcodes', 'contactusemail.html'), 'utf8');
const currentVersionShortcodeSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'shortcodes', 'current-version.html'), 'utf8');
const previousVersionShortcodeSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'shortcodes', 'previous-version.html'), 'utf8');
const previousVersionPartialSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'previous-version.html'), 'utf8');
const headerSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'header.html'), 'utf8');
const sharedHeaderSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'layouts', 'partials', 'site-header.html'), 'utf8');
const siteSectionUrlSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'layouts', 'partials', 'site-section-url.html'), 'utf8');
const contextDataSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'context-data.html'), 'utf8');
const sharedSidebarSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'layouts', 'partials', 'sidebar-shell.html'), 'utf8');
const blogBaseSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', '_default', 'baseof.html'), 'utf8');
const mailingListBaseSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-mailing-list', '_default', 'baseof.html'), 'utf8');
const mailingListSearchSource = fs.readFileSync(path.join(repositoryRoot, 'content', 'static', 'archive-mailing-list', 'js', 'mailing-list-search.js'), 'utf8');
const blogIndexSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'index.html'), 'utf8');
const blogByYearSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'by-year.html'), 'utf8');
const blogSingleSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', '_default', 'single.html'), 'utf8');
const blogCategoriesSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'categories.html'), 'utf8');
const blogCategorySource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'category.html'), 'utf8');
const blogDateSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'date.html'), 'utf8');
const blogMenuSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'partials', 'blog-sidebar-tree.html'), 'utf8');
const blogSortSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'partials', 'blog-sort.html'), 'utf8');
const blogAuthorSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'archive-technical-blog', 'author.html'), 'utf8');
const sharedHeaderCss = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'static', 'css', 'site-header.css'), 'utf8');
const sidebarSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'sidebar.html'), 'utf8');
const headSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'partials', 'head.html'), 'utf8');
const baseSource = fs.readFileSync(path.join(themeRoot, 'layouts', 'baseof.html'), 'utf8');
const homepageSource = fs.readFileSync(path.join(repositoryRoot, 'layouts', 'homepage', 'index.html'), 'utf8');
const faviconPath = path.join(commonAssets, 'images', 'ui', 'favicon.png');
const projectLogoPath = path.join(commonAssets, 'images', 'branding', 'openriak-mark.png');
const siteSections = JSON.parse(fs.readFileSync(path.join(repositoryRoot, 'layouts', 'common-docs', 'data', 'site_sections.json'), 'utf8'));
const dockerComposeSource = fs.readFileSync(path.join(repositoryRoot, 'docker', 'compose.yaml'), 'utf8');
const dockerfileSource = fs.readFileSync(path.join(repositoryRoot, 'docker', 'Dockerfile'), 'utf8');
const localRunnerSource = fs.readFileSync(path.join(repositoryRoot, 'docker', 'run.local.sh'), 'utf8');
const staticBuilderSource = fs.readFileSync(path.join(repositoryRoot, 'docker', 'build.static.sh'), 'utf8');
const shellBuilderSource = fs.readFileSync(path.join(repositoryRoot, 'tools', 'scripts', 'build.sh'), 'utf8');
assert.match(dockerComposeSource, /OPENRIAK_DOCS_BUILD_PROFILE:[\s\S]*--include-version "riak-kv=\$\$\{OPENRIAK_DOCS_RIAK_KV_VERSION\}"/, 'development compose must mount one selectable Riak KV release');
assert.match(dockerComposeSource, /archives:[\s\S]*profiles: \['release'\]/, 'the archive Hugo service must run only in the release profile');
assert.match(localRunnerSource, /development\|beta-test\|release[\s\S]*--profile "\$compose_profile"/, 'the local runner must expose all three build profiles');
assert.match(dockerfileSource, /FROM scratch AS core-static[\s\S]*FROM scratch AS static/, 'Docker must expose separate core-only and assembled static targets');
assert.match(staticBuilderSource, /development\|beta-test\)[\s\S]*core-build[\s\S]*release\)[\s\S]*assembled/, 'static builds must use runnable core-only and assembled stages for mounted export');
assert.match(staticBuilderSource, /staging="\$repository_root\/docker-wip"[\s\S]*--mount "type=bind,source=\$staging,target=\/output"[\s\S]*tar -C \/project\/public -cf - \. \| tar -C \/output -xf -/, 'static builds must export through bind-mounted docker-wip staging without preserving container ownership');
assert.doesNotMatch(staticBuilderSource, /--output/, 'static builds must not use the slow BuildKit local exporter');
assert.match(shellBuilderSource, /development\|beta-test\|release[\s\S]*if \[ "\$build_profile" = release \]/, 'local Hugo builds must assemble archives only for release');
assert.match(headSource, /docs\.css[^"\n]+\?v=/, 'shared stylesheet must be cache-busted');
assert.match(contactEmailShortcodeSource, /contactUsEmail[\s\S]*info@riak\.info/, 'legacy contact-email links must have a supported default');
assert.match(currentVersionShortcodeSource, /partial "current-version\.html" \.Page \| strings\.TrimSpace/, 'the current-version shortcode must use the canonical rendered-page version');
assert.match(currentVersionShortcodeSource, /\.Get "format" \| default "full"[\s\S]*eq \$format "major-minor"[\s\S]*printf "%s\.%s"/, 'the current-version shortcode must support full and major-minor plain-text formats');
assert.match(currentVersionShortcodeSource, /format must be full or major-minor/, 'the current-version shortcode must reject unknown formats');
assert.match(previousVersionShortcodeSource, /partial "previous-version\.html" \.Page \| strings\.TrimSpace/, 'the previous-version shortcode must use the canonical previous-release resolver');
assert.match(previousVersionPartialSource, /index hugo\.Data\.versions \$productID[\s\S]*\$isEarlier[\s\S]*\$isLaterThanPrevious/, 'previous-version must select the greatest semantic version below the current release');
assert.match(previousVersionPartialSource, /previous-version has no previous release: product=%s version=%s page=%s/, 'previous-version must stop the build when no earlier release exists');
assert.match(baseSource, /js\/theme\.js[^"\n]+\?v=/, 'theme picker script must be cache-busted');
assert.match(baseSource, /js\/docs-runtime\.js[^"\n]+\?v=20260901-selected-download-table/, 'the download checksum runtime must use its current cache key');
assert.match(headSource, /css\/docs\.css[^"\n]+\?v=20260902-otp-column/, 'download table styling must use its current cache key');
assert.match(headSource, /images\/ui\/favicon\.png[^"\n]+\?v=/, 'documentation pages must use the shared OpenRiak favicon');
assert.match(homepageSource, /images\/ui\/favicon\.png[^"\n]+\?v=/, 'the homepage must use the shared OpenRiak favicon');
assert.ok(fs.existsSync(faviconPath), 'the shared OpenRiak favicon must exist');
assert.ok(fs.existsSync(projectLogoPath), 'the shared OpenRiak project mark must exist');
assert.match(sharedHeaderSource, /class="brand-home" href="\{\{ \$page\.Site\.Home\.RelPermalink \}\}"[\s\S]*openriak-mark\.png/, 'the OpenRiak project mark must always link to the site homepage');
assert.match(sharedHeaderSource, /class="brand-section" href="\{\{ partial "site-section-url\.html" \$section\.url \}\}"[\s\S]*\{\{ \$section\.name \}\}/, 'the Site section name must resolve its configured landing path against baseURL');
assert.match(sharedHeaderSource, /data-site-section-picker[\s\S]*>Site sections<\/h2>/, 'the cross-site picker must be named Site sections');
assert.match(sharedHeaderSource, /eq \.id "openriak-kv"[\s\S]*eq \.id "community"[\s\S]*role="separator"/, 'the Site section picker must separate Homepage, products, and community/archive groups');
assert.match(headerSource, /partial "site-header\.html"/, 'product pages must use the shared header');
assert.match(headerSource, /where hugo\.Data\.site_sections "id" \$context\.product\.id/, 'product pages must pass canonical Site section landing URLs into the shared header');
assert.match(blogBaseSource, /partial "site-header\.html"/, 'archived blog pages must use the shared header');
assert.match(blogBaseSource, /js\/theme\.js[\s\S]*js\/docs-shell\.js/, 'archived blog pages must load the shared header controls');
assert.match(blogBaseSource, /css\/site-header\.css/, 'archived blog pages must load shared header styling');
assert.doesNotMatch(blogBaseSource, /archive-subnav|All posts|Read-only archive/, 'the technical blog must use only the shared site header');
assert.match(blogIndexSource, /categories\/[\s\S]*>By Category<\/h2>[\s\S]*by-year\/[\s\S]*>By Year<\/h2>/, 'the archive landing page must link to category and year browsing');
assert.doesNotMatch(blogIndexSource, /Paginate|posts-grid/, 'the archive landing page must not default to an article listing');
assert.match(blogByYearSource, /GroupByDate "2006" "desc"[\s\S]*len \.Pages/, 'the year index must list years in reverse order with article counts');
assert.match(blogSingleSource, /\.Params\.categories[\s\S]*aria-label="Article categories"/, 'archived articles must link all assigned categories');
assert.match(blogCategoriesSource, /Params\.categories" "intersect"/, 'category counts must include multi-category articles');
assert.match(blogCategorySource, /Params\.categories" "intersect"/, 'category pages must include multi-category articles');
assert.match(blogMenuSource, /GroupByDate "2006" "desc"/, 'archive menu years must use reverse date order');
assert.match(blogMenuSource, /GroupByDate "January" "desc"/, 'archive menu months must use reverse date order');
assert.match(blogMenuSource, /href="\{\{ \$yearHomeURL \}\}">By Year<\/a>[\s\S]*href="\{\{ \$categoryHomeURL \}\}">By Category<\/a>/, 'archive menu group headings must link to the year and category indexes');
assert.match(blogMenuSource, /\.Pages\.ByTitle/, 'archive menu categories must use alphabetical order');
assert.match(blogMenuSource, /Params\.categories" "intersect"[\s\S]*len \$categoryPosts/, 'archive menu category counts must include multi-category articles');
assert.match(blogDateSource, /Date\.Year[\s\S]*Date\.Month[\s\S]*Paginate/, 'year and month pages must filter and paginate archived posts');
assert.match(blogCategorySource, /Params\.sort[\s\S]*ByDate\.Reverse[\s\S]*ByTitle[\s\S]*Paginate/, 'category archives must support globally paginated date and name sorting');
assert.match(blogDateSource, /Params\.sort[\s\S]*ByDate\.Reverse[\s\S]*ByTitle[\s\S]*Paginate/, 'date archives must support globally paginated date and name sorting');
assert.match(blogSortSource, />Date<\/a>[\s\S]*>Title<\/a>/, 'archive sort controls must offer Date and Title options');
assert.match(blogSingleSource, /authors\/%s\/[\s\S]*by-year\/%s\/%s\/[\s\S]*class="byline-link"/, 'article bylines must link authors and publication months to their archives');
assert.match(blogSingleSource, /replaceRE `\[\^a-z0-9\]\+` `-` \(\$author \| lower\)/, 'author links must use the same punctuation-normalizing slug rule as authored author pages');
assert.match(blogAuthorSource, /Params\.author[\s\S]*Params\.author[\s\S]*Paginate/, 'author archives must filter and paginate all articles by the selected author');
assert.match(sharedHeaderCss, /:root\[data-theme="dark"\] \.global-header/, 'the shared header must support dark theme styling');
assert.match(homepageSource, /aria-label="Site sections"/, 'the homepage list must be named Site sections');
assert.match(homepageSource, /range (?:where )?hugo\.Data\.site_sections/, 'the homepage and header must share the same Site sections data');
assert.match(homepageSource, /partial "site-header\.html"[\s\S]*js\/theme\.js[\s\S]*js\/docs-shell\.js/, 'the homepage must use the shared header and theme controls');
assert.match(homepageSource, /css\/site-header\.css[^"\n]+\?v=/, 'the homepage must load the cache-busted shared header stylesheet');
assert.match(homepageSource, /where hugo\.Data\.site_sections "showOnHomepage" "ne" false/, 'the Homepage section must not link to itself in the homepage card grid');
assert.ok(siteSections.some((section) => section.id === 'homepage' && section.name === 'Homepage' && section.url === ''), 'Homepage must use the configured base URL');
assert.ok(siteSections.some((section) => section.id === 'archived-technical-blog' && section.url === 'archived-technical-blog/'), 'Archived Technical Blog must default to its base-independent browse path');
assert.ok(siteSections.some((section) => section.id === 'community' && section.url === 'community/'), 'Community must use a base-independent path');
assert.deepEqual(siteSections.map((section) => section.id), ['homepage', 'openriak-kv', 'openriak-cs', 'openriak-ts', 'community', 'archived-technical-blog', 'archived-mailing-list'], 'Site sections must be ordered Homepage, products, Community, then archives');
assert.ok(siteSections.every((section) => section.name && section.logo && section.description && section.action && Object.hasOwn(section, 'url')), 'every Site section must provide complete shared navigation data');
assert.ok(siteSections.every((section) => !section.url.startsWith('/')), 'Site section paths must not bypass the configured base URL');
assert.match(siteSectionUrlSource, /\. \| relURL/, 'Site section paths must resolve against Hugo baseURL');
assert.match(homepageSource, /partial "site-section-url\.html" \.url/, 'Homepage cards must resolve Site section paths against baseURL');
assert.match(sharedHeaderSource, /partial "site-section-url\.html"[^\n]+\.url/g, 'Shared header links must resolve Site section paths against baseURL');
assert.match(contextDataSource, /merge \. \(dict "url" \(partial "site-section-url\.html" \.url\)\)/, 'Runtime Site section URLs must resolve against baseURL');
assert.ok(docsCssSource.includes(':root[data-theme="dark"] .version-warning { border-bottom-color: #6f5d28; background: #322d1b; color: #d8c88a; }'), 'dark theme must use a subdued old-version warning');
assert.match(docsCssSource, /\.doc-article pre \{[^}]*border: 1px solid var\(--line\)[^}]*background: var\(--panel-cool\)[^}]*color: var\(--ink\)/, 'light theme code blocks must use the light panel palette');
assert.match(docsCssSource, /\.doc-article pre code \{[^}]*padding: 0[^}]*background: transparent[^}]*color: inherit/, 'code inside preformatted blocks must not retain inline-code styling');
assert.match(docsCssSource, /:root\[data-theme="dark"\] \.doc-article pre \{[^}]*background: #202a33[^}]*color: #f6f8fa/, 'dark theme code blocks must retain their high-contrast dark palette');
assert.ok(!sharedHeaderSource.includes('⌄') && !sidebarSource.includes('⌄'), 'pickers must not use the old down marker');
assert.match(sharedHeaderSource, /data-theme-picker[\s\S]*class="theme-trigger"[\s\S]*class="picker-chevron"/, 'Theme must use the shared custom picker and chevron');
assert.ok(!sharedHeaderSource.includes('data-theme-select') && !sharedHeaderSource.includes('<select'), 'Theme picker must not use a native select');
assert.match(sharedHeaderSource, /theme-system\.svg[\s\S]*theme-dark\.svg[\s\S]*theme-light\.svg/, 'Theme picker must provide icons for default, dark, and light');
assert.match(sharedHeaderCss, /picker-chevron::before \{[^}]*content: '›'/, 'pickers must use the page-tree chevron');
assert.ok(docsCssSource.includes('.docs-sidebar:has(.picker-panel:not([hidden]))') && docsCssSource.includes('overflow: visible;'), 'open sidebar flyouts must escape the sidebar scroller');
assert.ok(docsCssSource.includes('.picker-panel {') && docsCssSource.includes('width: max-content;'), 'desktop picker panels must use intrinsic width');
assert.match(docsCssSource, /\.version-panel \{[^}]*width: max-content[^}]*max-width: calc\(100vw - 2rem\)/, 'desktop version picker must size to its content before reaching the viewport limit');
assert.match(docsCssSource, /\.version-row \{[^}]*grid-template-columns: 3\.2rem minmax\(0,1fr\)[^}]*width: 100%/, 'version rows must fit the picker width');
assert.match(docsCssSource, /\.version-releases \{[^}]*flex-wrap: wrap/, 'version releases must wrap at every viewport width');
assert.match(runtimeSource, /section\.dataset\.brand = brand\.name/, 'version brands must expose a stable styling hook');
assert.match(docsCssSource, /\.version-brand\[data-brand="Riak KV"\] \{ --version-brand-logo-height: 24\.7px; \}/, 'the Riak KV picker logo must be 65 percent of the OpenRiak logo height');
assert.match(docsCssSource, /\.version-option:first-child \{ border-top-left-radius: \.875rem; \}/, 'the first release in each version family must curve at the top left');
assert.match(docsCssSource, /\.version-option:not\(\[hidden\]\):not\(:has\(~ \.version-option:not\(\[hidden\]\)\)\) \{ border-bottom-right-radius: \.875rem; \}/, 'the last visible release in each version family must curve at the bottom right');
assert.match(docsCssSource, /\.download-os-index button \{[^}]*border-radius: 0/, 'download operating-system buttons must use square intermediate corners');
assert.match(docsCssSource, /\.download-os-index li:first-child button \{ border-top-left-radius: \.875rem; \}/, 'the first download operating system must curve at the top left');
assert.match(docsCssSource, /\.download-os-index li:last-child button \{ border-bottom-right-radius: \.875rem; \}/, 'the last download operating system must curve at the bottom right');
assert.match(docsCssSource, /@media \(max-width: 760px\)[\s\S]*\.picker-panel \{[^}]*top: calc\(64px \+ 1rem\)[^}]*bottom: 1rem[^}]*overflow-y: auto/, 'mobile picker panels must remain below the header and scroll within the viewport');
assert.match(docsCssSource, /@media \(max-width: 760px\)[\s\S]*\.docs-sidebar \{[^}]*align-self: stretch[^}]*height: auto/, 'mobile sidebar must stretch between its fixed insets so overflowing navigation can scroll');
assert.match(runtimeSource, /className = 'os-option-logo'/, 'OS picker options must render their logos');
assert.match(runtimeSource, /option\.append\(optionLogo, copy\)/, 'OS picker options must include their logos');
assert.match(runtimeSource, /data-download-os-select[\s\S]*setOs\(os\)/, 'the operating-system list must update the selected download state');
assert.match(runtimeSource, /data-all-downloads-link[\s\S]*allDownloads\.open = true/, 'the selected download box must expand All downloads before following its anchor');
assert.match(runtimeSource, /data-selected-download-os[\s\S]*data-selected-download-logo[\s\S]*data-doc-downloads[\s\S]*sourceGroups[\s\S]*downloads-table/, 'changing OS must update the selected download subtitle, logo, and package table');
assert.match(downloadsTemplateSource, /data-download-os-select[\s\S]*<h2>Download<\/h2>[\s\S]*modern-downloads-selected-os[\s\S]*data-doc-downloads[\s\S]*partial "download-table\.html"[\s\S]*data-all-downloads-link[\s\S]*<summary>Source Code<\/summary>[\s\S]*<summary>All downloads<\/summary>/, 'OpenRiak downloads must use an OS selector, title/subtitle selected table, collapsed disclosures, and an All downloads expansion link');
assert.match(downloadsTemplateSource, /data-legacy-downloads[\s\S]*Alpine Linux Riak Repository/, 'Riak KV downloads must retain the legacy grouped layout and Alpine repository link');
assert.equal((downloadsTemplateSource.match(/partial "download-table\.html"/g) || []).length, 3, 'selected, modern All downloads, and legacy downloads must share the grouped download table');
assert.match(downloadsTemplateSource, /OpenRiak KV for[\s\S]*Riak KV for/, 'modern and legacy download groups must identify their product and operating-system family');
assert.match(downloadTableSource, /<th>OTP<\/th><th>Architecture<\/th><th>Package<\/th><th class="download-table-actions">Actions<\/th>[\s\S]*data-download-os-id="\{\{ \$os\.id \}\}"[\s\S]*data-download-checksum-toggle[\s\S]*data-copy-label="Copy URL"[\s\S]*data-download-checksum-row hidden[\s\S]*<td aria-hidden="true"><\/td>[\s\S]*colspan="3"/, 'shared download tables must identify their OS and use four columns, right-aligned actions, and a checksum row spanning architecture through actions');
assert.match(downloadChecksumSource, /<div class="download-actions">[\s\S]*data-download-checksum-toggle[\s\S]*data-copy-label="Copy URL"[\s\S]*data-download-checksum-panel hidden[\s\S]*data-copy-label="Copy checksum"/, 'copy URL must sit beside the checksum toggle while copy checksum remains inside its hidden panel');
assert.match(downloadCopyIconSource, /download-copy-glyph[\s\S]*download-copy-tick/, 'copy actions must share the standard copy icon with an overlaid success tick');
assert.match(downloadHashIconSource, /download-hash-icon[\s\S]*M10 3 8 21/, 'checksum toggles must use the standard hash icon');
assert.match(runtimeSource, /sourceGroups[\s\S]*cloneNode\(true\)[\s\S]*is-checksum-expanded[\s\S]*aria-expanded[\s\S]*table\.append\(group\)/, 'changing OS must clone the shared table rows and reset their checksum controls');
assert.match(runtimeSource, /downloadChecksumToggle[\s\S]*download-package-row[\s\S]*data-download-checksum-row[\s\S]*panel\.hidden = !panel\.hidden[\s\S]*aria-expanded[\s\S]*is-checksum-expanded/, 'the checksum toggle must expand compact panels and visually merge table checksum rows with their packages');
assert.match(runtimeSource, /navigator\.clipboard\?\.writeText[\s\S]*data-copy-value[\s\S]*copyValue\(button\)/, 'checksum actions must use delegated clipboard handling for static and dynamic lists');
assert.match(docsCssSource, /\.download-copy-tick[\s\S]*#2f9e44[\s\S]*\.download-copy\.is-copied \.download-copy-tick[^{]*\{[^}]*opacity: 1/, 'successful copies must overlay the copy icon with a green tick');
assert.match(docsCssSource, /\.download-checksum-panel \{[^}]*align-items: start[^}]*\}[\s\S]*\.download-checksum-actions \{[^}]*align-self: end/, 'checksum copy actions must align with the digest rather than the full label-and-digest block');
assert.match(docsCssSource, /\.downloads-table[\s\S]*\.download-table-actions \{[^}]*text-align: right[\s\S]*is-checksum-expanded \.download-package-row > td \{[^}]*border-bottom-color: transparent[\s\S]*\.download-table-checksum-cell \.download-checksum-panel/, 'expanded table checksums must visually join their package row without an intervening divider');
assert.match(runtimeSource, /event\.key === 'Escape' && !panel\.hidden/, 'closed version picker must not claim focus on Escape');
assert.match(runtimeSource, /event\.stopPropagation\(\);[\s\S]*input\.value = '';[\s\S]*cachedQuery = '';[\s\S]*hideResults\(\);/, 'Escape in Search must clear and close results');
assert.match(runtimeSource, /query === cachedQuery[\s\S]*input\.addEventListener\('click', showCachedResults\);/, 'clicking an unchanged Search must reopen cached results');
assert.match(runtimeSource, /if \(!root\.contains\(event\.target\)\) hideResults\(\);/, 'clicking outside Search must hide results without clearing the input');
assert.match(searchIndexSource, /"content" \(\.Content \| plainify\)[\s\S]*"content" \(\$page\.Content \| plainify\)/, 'section search indexes must contain the full rendered text of the section and every page');
assert.match(sharedSearchSource, /page\.title[\s\S]*page\.description[\s\S]*page\.content/, 'shared sidebar search must match titles, descriptions, and full page text');
assert.match(runtimeSource, /page\.title[\s\S]*page\.description[\s\S]*page\.content/, 'the documentation fallback search must match titles, descriptions, and full page text');
assert.match(sharedSearchSource, /title\.includes\(query\) \? 1000[\s\S]*description\.includes\(query\) \? 100[\s\S]*content\.split\(query\)/, 'full-text search must rank title, description, and repeated content matches');
assert.match(runtimeSource, /title\.includes\(query\) \? 1000[\s\S]*description\.includes\(query\) \? 100[\s\S]*content\.split\(query\)/, 'the fallback search must use the same relevance ranking');
assert.match(sharedSearchSource, /searchParams\.set\('highlight', query\)/, 'shared search results must carry their query to the destination page');
assert.match(mailingListSearchSource, /searchParams\.append\('highlight', term\)/, 'mailing-list results must carry every search term to the destination thread');
assert.match(highlightSource, /data-search-highlight-root[\s\S]*createTreeWalker[\s\S]*mark\.search-highlight[\s\S]*scrollIntoView/, 'destination pages must highlight content matches and jump to the first one');
assert.match(highlightSource, /details:not\(\[open\]\)[\s\S]*disclosure\.open = true/, 'highlighting must reveal matches inside collapsed mailing-list replies');
assert.match(highlightSource, /search-highlight-clear[\s\S]*searchParams\.delete\('highlight'\)/, 'highlighting must provide a clear control that cleans the URL');
assert.match(baseSource, /data-search-highlight-root[\s\S]*search-highlight\.js/, 'product pages must load highlighting for their content root');
assert.match(blogBaseSource, /data-search-highlight-root[\s\S]*search-highlight\.js/, 'technical-blog pages must load highlighting for their content root');
assert.match(mailingListBaseSource, /data-search-highlight-root[\s\S]*search-highlight\.js/, 'mailing-list pages must load highlighting for their content root');
assert.match(shellSource, /data-nav-tree-toggle/, 'hierarchical navigation toggles must be initialized');
assert.match(shellSource, /children\.hidden = !expanded/, 'tree toggles must directly control their child node regardless of the current page');
assert.match(sharedSidebarSource, /data-sidebar-collapse[\s\S]*data-sidebar-expand[\s\S]*data-sidebar-version[\s\S]*data-sidebar-os[\s\S]*data-sidebar-search-button[\s\S]*data-sidebar-tree/, 'the shared sidebar shell must provide collapse, expand, version, OS, search, and page-tree controls');
assert.match(docsCssSource, /:root\.sidebar-collapsed \.docs-shell \{ grid-template-columns: 4\.25rem/, 'collapsed documentation sidebar must become a narrow icon rail');
assert.match(shellSource, /openriak-docs-sidebar-collapsed[\s\S]*setSidebarCollapsed[\s\S]*expandFor/, 'documentation sidebar state must persist and rail controls must restore their full tools');
assert.match(headSource, /openriak-docs-sidebar-collapsed/, 'persisted sidebar state must be applied before page paint');
assert.match(hugo018ImporterSource, /sibling_directory[\s\S]*_index\.md/, 'the Hugo 0.18 importer must convert page-plus-directory sections to branch bundles');
assert.match(hugo018ImporterSource, /linkTitle:[\s\S]*weight:/, 'the Hugo 0.18 importer must promote legacy menu presentation into page front matter');
const productIds = ['openriak-kv', 'openriak-cs', 'openriak-ts'];

assert.ok(compareSemVer('3.10.0', '3.9.9') > 0);
assert.ok(compareSemVer('1.10.0', '1.9.99') > 0);
assert.ok(compareSemVer('3.4.10', '3.4.9') > 0);
assert.ok(compareSemVer('3.4.1', '3.4.1-rc.1') > 0);
assert.throws(() => parseSemVer('3.4'));

const kvProduct = JSON.parse(fs.readFileSync(path.join(repositoryRoot, 'content', 'openriak-kv', 'data', 'product.json')));
assert.equal(resolveBrand('3.4.0', kvProduct.brands).name, 'OpenRiak KV');
assert.equal(resolveBrand('2.0.0', kvProduct.brands).name, 'Riak KV');

const v341 = JSON.parse(fs.readFileSync(path.join(generatedProductsRoot, 'openriak-kv', 'data', 'versions', '3.4.1.json')));
const v340 = JSON.parse(fs.readFileSync(path.join(generatedProductsRoot, 'openriak-kv', 'data', 'versions', '3.4.0.json')));
const v200 = JSON.parse(fs.readFileSync(path.join(generatedProductsRoot, 'openriak-kv', 'data', 'versions', '2.0.0.json')));
const importedKvVersions = [
  '2.0.0', '2.0.1', '2.0.2', '2.0.4', '2.0.5', '2.0.6', '2.0.7', '2.0.8', '2.0.9',
  '2.1.1', '2.1.3', '2.1.4', '2.2.0', '2.2.1', '2.2.2', '2.2.3', '2.2.6',
  '2.9.0', '2.9.1', '2.9.2', '2.9.4', '2.9.7', '2.9.8', '2.9.9', '2.9.10',
  '3.0.1', '3.0.2', '3.0.3', '3.0.4', '3.0.6', '3.0.7', '3.0.8', '3.0.9',
  '3.0.10', '3.0.11', '3.0.12', '3.0.13', '3.0.14', '3.0.15', '3.0.16',
  '3.2.0', '3.2.3', '3.2.4', '3.2.5'
];
for (const version of importedKvVersions) {
  const sourceDirectory = path.join(repositoryRoot, 'content', 'riak-kv', `${version}-new-release`);
  const adapterPath = path.join(generatedProductsRoot, 'openriak-kv', 'data', 'versions', `${version}.json`);
  assert.ok(fs.existsSync(sourceDirectory), `missing imported Riak KV ${version} baseline`);
  assert.ok(fs.existsSync(adapterPath), `missing generated Riak KV ${version} metadata`);
  const metadataRoot = path.join(repositoryRoot, 'content', 'openriak-kv', 'metadata', version);
  assert.ok(fs.existsSync(path.join(metadataRoot, 'supported-os.json')), `missing ${version} supported OS metadata`);
  assert.ok(fs.existsSync(path.join(metadataRoot, 'downloads.json')), `missing ${version} download metadata`);
  assert.ok(!fs.existsSync(path.join(metadataRoot, 'defaults.json')), `${version} must not generate unused defaults metadata`);
  const adapter = JSON.parse(fs.readFileSync(adapterPath));
  assert.equal(adapter.generatedFrom, `content/openriak-kv/metadata/${version}`);
  assert.equal(adapter.metadataStatus.defaults, 'not_generated');
  assert.deepEqual(adapter.operatingSystems, [], `${version} must not expose the OpenRiak OS picker`);
  assert.equal(adapter.defaultOs, null);
  assert.ok(adapter.downloadOperatingSystems.length > 0, `${version} downloads page must retain OS metadata`);
  assert.ok(Object.values(adapter.downloads).flat().length > 0, `${version} downloads page must retain package metadata`);
}
assert.ok(!fs.existsSync(path.join(repositoryRoot, 'content', 'riak-kv', '2.9.0p5-new-release')), '2.9.0p5 must publish as 2.9.0');
const ubuntu2404 = v341.operatingSystems.find((os) => os.id === 'ubuntu-noble-amd64');
const ubuntuArm64 = v341.operatingSystems.find((os) => os.id === 'ubuntu-noble-arm64');
assert.equal(v341.generatedFrom, 'content/openriak-kv/metadata/3.4.1');
assert.equal(v340.generatedFrom, 'content/openriak-kv/metadata/3.4.0');
assert.equal(v340.metadataStatus.defaults, 'partial');
assert.equal(v340.metadataWarnings.length, 2);
assert.equal(resolveOs('ubuntu-noble-amd64', ubuntu2404, v341).id, 'ubuntu-noble-amd64', 'exact OS and architecture are retained');
assert.equal(resolveOs('ubuntu-noble-arm64', ubuntuArm64, v340).id, 'ubuntu-noble-arm64', 'exact metadata OS and architecture are retained across versions');
assert.equal(resolveOs('ubuntu-noble-amd64', ubuntu2404, v200), null, 'legacy Riak KV versions must not expose the OS picker');
assert.equal(v200.generatedFrom, 'content/openriak-kv/metadata/2.0.0');
assert.deepEqual(v200.operatingSystems, []);
assert.ok(v200.downloadOperatingSystems.length > 0);
assert.deepEqual(v200.values, {});
assert.equal(resolveValue(v341, 'ubuntu-noble-amd64', 'ring_size'), 64);
assert.equal(resolveValue(v341, 'ubuntu-noble-amd64', 'nodename'), 'riak@127.0.0.1');
assert.equal(resolveValue(v340, 'ubuntu-noble-amd64', 'ring_size'), 64);
assert.equal(resolveValue(v340, 'ubuntu-noble-amd64', 'nodename'), 'riak@127.0.0.1');
assert.match(v341.downloads['ubuntu-noble-amd64'][0].url, /^https:\/\/files\.tiot\.jp\//);
assert.match(v340.downloads['ubuntu-noble-amd64'][0].url, /^https:\/\/files\.tiot\.jp\//);
assert.throws(() => resolveValue(v341, 'ubuntu-noble-amd64', 'missing-key'));
assert.equal(
  resolveAssetUrl('images/os/ubuntu.svg', '/docs/', 'https://docs.example'),
  'https://docs.example/docs/images/os/ubuntu.svg',
  'shared assets must resolve from the site base rather than a product route'
);
for (const [version, adapter] of [['3.4.0', v340], ['3.4.1', v341]]) {
  const metadataRoot = path.join(repositoryRoot, 'content', 'openriak-kv', 'metadata', version);
  const supportedMetadata = JSON.parse(fs.readFileSync(path.join(metadataRoot, 'supported-os.json')));
  const downloadMetadata = JSON.parse(fs.readFileSync(path.join(metadataRoot, 'downloads.json')));
  assert.equal(adapter.operatingSystems.length, supportedMetadata.operating_systems.length, 'all ' + version + ' metadata OS targets must be exposed');
  assert.equal(Object.values(adapter.downloads).flat().length, Object.values(downloadMetadata.downloads).flatMap(Object.values).length, 'all ' + version + ' metadata downloads must be exposed');
}

assert.deepEqual(
  buildVersionCandidates({
    currentUrl: 'https://docs.example/docs/openriak-kv/3.4.1/configuration/networking/advanced/?os=ubuntu-24.04',
    productBase: '/docs/openriak-kv/',
    currentVersion: '3.4.1',
    targetVersion: '3.4.0'
  }),
  [
    'https://docs.example/docs/openriak-kv/3.4.0/configuration/networking/advanced/',
    'https://docs.example/docs/openriak-kv/3.4.0/configuration/networking/',
    'https://docs.example/docs/openriak-kv/3.4.0/configuration/',
    'https://docs.example/docs/openriak-kv/3.4.0/'
  ]
);

const generatedHugoConfigPath = path.join(repositoryRoot, 'tools', 'generated', 'hugo.yaml');
const coreHugoConfigPath = path.join(repositoryRoot, 'content', 'hugo.yaml');
const archiveHugoConfigPath = path.join(repositoryRoot, 'content', 'hugo-archives.yaml');
assert.ok(fs.existsSync(generatedHugoConfigPath), 'version mounts must be generated before architecture validation');
const hugoConfig = fs.readFileSync(generatedHugoConfigPath, 'utf8');
const coreHugoConfig = fs.readFileSync(coreHugoConfigPath, 'utf8');
const kv34Mounts = hugoConfig.split(/\r?\n/).filter((line) => line.includes("target: 'content/openriak-kv/3.4."));
assert.deepEqual(
  kv34Mounts.filter((line) => line.includes("target: 'content/openriak-kv/3.4.1'")).map((line) => line.match(/source: '([^']+)'/)[1]),
  ['openriak-kv/3.4.1', 'openriak-kv/3.4.0-new-release'],
  '3.4.1 must layer over the self-contained 3.4.0 baseline'
);
assert.ok(kv34Mounts.every((line) => /source: 'openriak-kv\//.test(line)), 'OpenRiak KV 3.4.x must never inherit Riak KV sources');
const legacyKvMounts = hugoConfig.split(/\r?\n/).filter((line) => /target: 'content\/openriak-kv\/2\./.test(line));
assert.ok(legacyKvMounts.length > 0 && legacyKvMounts.every((line) => /source: 'riak-kv\//.test(line)), 'Riak KV versions must inherit only Riak KV sources while retaining OpenRiak KV URLs');
assert.match(fs.readFileSync(path.join(repositoryRoot, 'content', 'openriak-kv', '3.4.0-new-release', '_index.md'), 'utf8'), /^release_baseline: true$/m, '3.4.0 must remain explicitly marked as a release baseline');
assert.doesNotMatch(hugoConfig, /\/(?:releases|layers)\//, 'generated version mounts must use flat product/version sources');
assert.match(hugoConfig, /source: 'homepage\/pages'/, 'the homepage must be mounted into the core project');
assert.match(hugoConfig, /source: 'community\/pages', target: 'content\/community'/, 'Community must be mounted as a normal Pages collection');
assert.doesNotMatch(hugoConfig, /target: 'content\/archived-(technical-blog|mailing-list)'/, 'archive content must not be mounted into the core project');
const archiveHugoConfig = fs.readFileSync(archiveHugoConfigPath, 'utf8');
assert.match(archiveHugoConfig, /target: 'content\/archived-technical-blog'/, 'the blog must be mounted into the archive project');
assert.match(archiveHugoConfig, /target: 'content\/archived-mailing-list'/, 'the mailing list must be mounted into the archive project');
assert.match(archiveHugoConfig, /archive-technical-blog\/by-year\.html', target: 'layouts\/blog\/by-year\.html'/, 'the blog year index template must be mounted into the archive project');
assert.doesNotMatch(archiveHugoConfig, /source: '(homepage|community|openriak-kv|riak-kv)\//, 'active content must not be mounted into the archive project');
for (const [name, config] of [['core', coreHugoConfig], ['archive', archiveHugoConfig]]) {
  assert.match(config, /hugo-admonitions\/layouts\/_default\/_markup\/render-blockquote-alert\.html', target: 'layouts\/_markup\/render-blockquote-alert\.html'/, `${name} Hugo project must mount the admonition render hook`);
  assert.match(config, /hugo-admonitions\/layouts\/partials\/admonitions', target: 'layouts\/partials\/admonitions'/, `${name} Hugo project must mount the admonition icons where the module's templates.Exists check can find them`);
  assert.match(config, /hugo-admonitions\/assets\/css\/vendors', target: 'assets\/css\/vendors'/, `${name} Hugo project must mount the admonition styles`);
  assert.match(config, /hugo-admonitions\/i18n', target: 'i18n'/, `${name} Hugo project must mount the admonition translations`);
}
assert.equal((dockerfileSource.match(/COPY layouts\/_vendor\/github\.com\/KKKZOZ\/hugo-admonitions \.\/layouts\/_vendor\/github\.com\/KKKZOZ\/hugo-admonitions/g) || []).length, 2, 'both Docker Hugo stages must include the vendored admonition module');
assert.ok(fs.existsSync(path.join(repositoryRoot, 'content', 'community', 'pages', '_index.md')), 'Community must have an authored landing page');
assert.ok(fs.existsSync(path.join(commonAssets, 'images', 'sites', 'community.svg')), 'Community must have a shared Site section logo');
assert.ok(fs.existsSync(path.join(commonAssets, 'images', 'sites', 'homepage.svg')), 'Homepage must have a shared Site section logo');

const blogPostsRoot = path.join(repositoryRoot, 'content', 'archive-technical-blog', 'posts');
const blogCategoriesRoot = path.join(repositoryRoot, 'content', 'archive-technical-blog', 'pages', 'categories');
const blogDatesRoot = path.join(repositoryRoot, 'content', 'archive-technical-blog', 'pages', 'by-year');
const blogAuthorsRoot = path.join(repositoryRoot, 'content', 'archive-technical-blog', 'pages', 'authors');
const approvedBlogCategories = [
  'Architecture & Distributed Systems',
  'Case Studies',
  'Cloud & Deployment',
  'Community & Events',
  'Data Modeling',
  'Developer Tools',
  'Erlang & BEAM',
  'Integrations & Plugins',
  'Operations',
  'Performance',
  'Releases',
  'Replication',
  'Search & Analytics',
  'Security',
  'Use Cases'
];
const categoryCounts = new Map(approvedBlogCategories.map((category) => [category, 0]));
const expectedDatePages = new Set();
const expectedAuthors = new Set();
const blogPostFiles = fs.readdirSync(blogPostsRoot).filter((file) => file.endsWith('.md'));
assert.equal(blogPostFiles.length, 233, 'the complete archived blog corpus must remain present');
for (const file of blogPostFiles) {
  const source = fs.readFileSync(path.join(blogPostsRoot, file), 'utf8');
  const title = source.match(/^title:\s*["']?(.*?)["']?\s*$/m);
  assert.ok(title, `${file} must have a title`);
  assert.doesNotMatch(title[1], /\s{2,}/, `${file} title must not contain repeated whitespace that breaks alphabetical sorting`);
  const date = source.match(/^date:\s*["']?(\d{4})-(\d{2})/m);
  assert.ok(date, `${file} must have a publication date`);
  const monthName = new Intl.DateTimeFormat('en', { month: 'long', timeZone: 'UTC' }).format(new Date(Date.UTC(2000, Number(date[2]) - 1, 1))).toLowerCase();
  expectedDatePages.add(`${date[1]}/${monthName}`);
  const author = source.match(/^author:\s*["']?(.*?)["']?\s*$/m);
  assert.ok(author, `${file} must have an author`);
  expectedAuthors.add(author[1]);
  assert.doesNotMatch(source, /^category:\s*Technical\s*$/m, `${file} must not retain the placeholder Technical category`);
  const block = source.match(/^categories:\s*\r?\n((?:\s+-\s+.*\r?\n?)+)/m);
  assert.ok(block, `${file} must have category metadata`);
  const categories = [...block[1].matchAll(/^\s+-\s+["']?(.*?)["']?\s*$/gm)].map((match) => match[1]);
  assert.ok(categories.length >= 1 && categories.length <= 3, `${file} must have one to three categories`);
  assert.equal(new Set(categories).size, categories.length, `${file} must not repeat a category`);
  for (const category of categories) {
    assert.ok(categoryCounts.has(category), `${file} uses unknown category ${category}`);
    categoryCounts.set(category, categoryCounts.get(category) + 1);
  }
}
const categoryPageDirectories = fs.readdirSync(blogCategoriesRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory());
assert.equal(categoryPageDirectories.length, approvedBlogCategories.length, 'every approved blog category must have one authored page');
for (const entry of categoryPageDirectories) {
  const nameSortPage = path.join(blogCategoriesRoot, entry.name, 'name', '_index.md');
  assert.ok(fs.existsSync(nameSortPage), `missing category name-sort page ${entry.name}`);
  assert.match(fs.readFileSync(nameSortPage, 'utf8'), /^sort:\s*name\s*$/m, `${entry.name} category name-sort page must select name order`);
}
for (const [category, count] of categoryCounts) assert.ok(count > 0, `${category} must contain at least one article`);
assert.equal(expectedDatePages.size, 77, 'the archive must retain all 77 populated year-month combinations');
assert.equal(new Set([...expectedDatePages].map((entry) => entry.slice(0, 4))).size, 9, 'the archive must retain all nine publication years');
for (const relative of expectedDatePages) {
  const [year] = relative.split('/');
  assert.ok(fs.existsSync(path.join(blogDatesRoot, year, '_index.md')), `missing archive year page ${year}`);
  assert.ok(fs.existsSync(path.join(blogDatesRoot, relative, '_index.md')), `missing archive month page ${relative}`);
  assert.ok(fs.existsSync(path.join(blogDatesRoot, year, 'name', '_index.md')), `missing archive year name-sort page ${year}`);
  assert.ok(fs.existsSync(path.join(blogDatesRoot, relative, 'name', '_index.md')), `missing archive month name-sort page ${relative}`);
}
const authorSlug = (author) => author.normalize('NFD').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
assert.equal(expectedAuthors.size, 50, 'the archive must retain all 50 credited authors');
assert.equal(fs.readdirSync(blogAuthorsRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory()).length, expectedAuthors.size, 'every credited author must have one authored archive page');
for (const author of expectedAuthors) {
  const authorPage = path.join(blogAuthorsRoot, authorSlug(author), '_index.md');
  assert.ok(fs.existsSync(authorPage), `missing author archive page for ${author}`);
  assert.match(fs.readFileSync(authorPage, 'utf8'), new RegExp(`^author: ${JSON.stringify(author).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}$`, 'm'), `author archive metadata must match ${author}`);
}

for (const productId of productIds) {
  const productRoot = path.join(repositoryRoot, 'content', productId);
  assert.match(hugoConfig, new RegExp(`source: '${productId}/\\d+\\.\\d+\\.\\d+`), `${productId} versions must be mounted into the unified project`);
  assert.match(hugoConfig, new RegExp(`target: 'content/${productId}/`), `${productId} must publish below its product path`);
  const product = JSON.parse(fs.readFileSync(path.join(productRoot, 'data', 'product.json')));
  const versionDir = path.join(generatedProductsRoot, productId, 'data', 'versions');
  const versionFiles = fs.readdirSync(versionDir).filter((file) => file.endsWith('.json'));
  const seen = new Set();

  for (const file of versionFiles) {
    const version = JSON.parse(fs.readFileSync(path.join(versionDir, file)));
    parseSemVer(version.version);
    assert.equal(file, `${version.version}.json`);
    assert.equal(version.product, product.id);
    assert.ok(!seen.has(version.version), `duplicate ${product.id} ${version.version}`);
    seen.add(version.version);
    assert.equal(resolveBrand(version.version, product.brands).name.length > 0, true);

    const ids = new Set();
    for (const os of version.operatingSystems) {
      assert.ok(os.id && os.family && os.name && os.version && os.codename && os.logo);
      assert.ok(!ids.has(os.id), `duplicate OS ${os.id} in ${product.id} ${version.version}`);
      ids.add(os.id);
      assert.ok(['.svg', '.png'].includes(path.extname(os.logo)), `unsupported OS logo format ${os.logo}`);
      assert.ok(fs.existsSync(path.join(commonAssets, os.logo)), `missing ${os.logo}`);
    }
    if (version.operatingSystems.length === 0) {
      assert.equal(version.defaultOs, null, `legacy metadata without operating systems must not invent a default in ${product.id} ${version.version}`);
    } else {
      assert.ok(ids.has(version.defaultOs), `invalid default OS in ${product.id} ${version.version}`);
    }
    const families = new Set(version.operatingSystems.map((os) => os.family));
    for (const family of families) {
      const members = version.operatingSystems.filter((os) => os.family === family);
      if (members.length > 1) assert.equal(members.filter((os) => os.defaultForFamily).length, 1, `family default for ${family}`);
    }
    for (const brand of product.brands) {
      assert.ok(['.svg', '.png'].includes(path.extname(brand.logo)), `unsupported brand logo format ${brand.logo}`);
      assert.ok(fs.existsSync(path.join(commonAssets, brand.logo)), `missing ${brand.logo}`);
    }
  }
  assert.ok(seen.has(product.currentVersion), `${product.id} current version must exist`);
}

const buildRoot = path.join(repositoryRoot, 'public', '.architecture-validation', 'openriak-kv');
if (fs.existsSync(buildRoot)) {
  const exists = (relative) => fs.existsSync(path.join(buildRoot, relative));

  for (const version of ['3.2.4', '3.2.3', '3.2.1', '3.2.0']) {
    assert.ok(exists(`${version}/page-a/index.html`), `temporary picker fixture must remain available in ${version}`);
  }
  assert.ok(!exists('3.4.1/page-a/index.html'), 'proof pages must not leak into production releases');
  assert.ok(exists('3.4.1/reference/faq/index.html'), '3.4.1 must inherit unchanged production pages from 3.4.0');
  assert.ok(exists('3.4.0/reference/faq/index.html'));
  assert.ok(exists('3.4.1/reference/query-api/queued-results/index.html'), '3.4.1 additions must be published');
  assert.ok(!exists('3.4.0/reference/query-api/queued-results/index.html'), '3.4.1 additions must not leak backwards');
  assert.ok(exists('3.2.5/setup/installing/debian-ubuntu/index.html'), 'the full historical 3.2.5 corpus must be published');

  const legacyDownloadsHtml = fs.readFileSync(path.join(buildRoot, '3.2.5', 'downloads', 'index.html'), 'utf8');
  assert.doesNotMatch(legacyDownloadsHtml, /data-os-trigger/, 'legacy Riak KV must not render the OS picker');
  assert.match(legacyDownloadsHtml, /data-legacy-downloads/, 'legacy Riak KV must render its structured downloads page');
  assert.match(legacyDownloadsHtml, /Alpine Linux Riak Repository for x86_64 and aarch64 architectures/, 'legacy Alpine downloads must link to repository installation instructions');
  assert.match(legacyDownloadsHtml, /files\.tiot\.jp\/riak\/kv\/3\.2\/3\.2\.5/, 'legacy package links must come from generated download metadata');

  assert.ok(exists('3.4.0/downloads/index.html'), '3.4.0 Downloads must be top-level');
  assert.ok(exists('3.4.0/release-notes/index.html'), '3.4.0 Release Notes must be top-level');
  assert.ok(exists('3.4.1/downloads/index.html'), '3.4.1 Downloads must be top-level');
  assert.ok(exists('3.4.1/release-notes/index.html'), '3.4.1 Release Notes must be top-level');
  const html = fs.readFileSync(path.join(buildRoot, '3.4.1', 'downloads', 'index.html'), 'utf8');
  const contextMatch = html.match(/<script id=docs-context type=application\/json>([\s\S]*?)<\/script>/);
  assert.ok(contextMatch, 'runtime context must be embedded');
  const context = JSON.parse(contextMatch[1]);
  assert.equal(context.currentVersion, '3.4.1');
  assert.equal(context.productBase, '/docs/openriak-kv/');
  assert.equal(context.assetBase, '/docs/');
  assert.match(html, /data-os-trigger/, 'OS picker trigger must be rendered');
  assert.match(html, /data-os-picker/, 'OS picker listbox must be rendered');
  assert.match(html, /data-nav-tree-toggle/, 'hierarchical navigation toggles must be rendered');
  assert.match(html, /data-nav-tree-children hidden/, 'non-current sections must remain rendered and collapsible');
  assert.match(html, /class=breadcrumbs[^>]*><a href=\/docs\/openriak-kv\/3\.4\.1\/>OpenRiak KV<\/a>/, 'breadcrumb root must target the active version landing page');
  assert.match(html, /data-modern-downloads/, 'the production downloads page must use the OpenRiak layout');
  const releaseNotesMenuIndex = html.indexOf('>Release Notes</a>');
  const downloadsMenuIndex = html.indexOf('>Downloads</a>');
  const foundationsMenuIndex = html.indexOf('>Foundations</a>');
  assert.ok(releaseNotesMenuIndex >= 0 && releaseNotesMenuIndex < downloadsMenuIndex && downloadsMenuIndex < foundationsMenuIndex, 'Release Notes and Downloads must be the first two labelled top-level menu items');
  assert.match(html, /aria-label="Download operating systems"[\s\S]*data-download-os-select=ubuntu-noble-amd64/, 'the modern downloads page must render every OS as an in-page selector');
  assert.match(html, /data-selected-downloads[\s\S]*<summary>Source Code<\/summary>[\s\S]*<summary>All downloads<\/summary>/, 'the selected OS downloads must render before the collapsed Source Code and All downloads disclosures');
  assert.doesNotMatch(html, /<details[^>]+(?:data-downloads-source|data-all-downloads)[^>]+open/, 'Source Code and All downloads must be collapsed by default');
  assert.match(html, />All downloads<[\s\S]*data-download-os=alpine-3\.21-x86_64/, 'All downloads must include the initially selected OS');
  assert.match(html, /files\.tiot\.jp\/riak\/kv\/3\.4\/3\.4\.1/);

  const inheritedHtml = fs.readFileSync(path.join(buildRoot, '3.4.1', 'reference', 'faq', 'index.html'), 'utf8');
  assert.match(inheritedHtml, /href=\/docs\/openriak-kv\/3\.4\.1\/how-to\/tune\/benchmark-cluster\//, 'inherited internal links must resolve within the rendered version');

  const oldVersionHtml = fs.readFileSync(path.join(buildRoot, '3.2.5', 'setup', 'installing', 'debian-ubuntu', 'index.html'), 'utf8');
  assert.match(oldVersionHtml, /data-version-warning-target=3\.4\.1/, 'old-version warning must use the shared version switcher');

  const search = JSON.parse(fs.readFileSync(path.join(buildRoot, '3.4.1', 'index.json'), 'utf8'));
  assert.ok(search.length > 300, 'the production search index must include the full 3.4.1 corpus');
  assert.ok(search.every((item) => item.url.includes('/docs/openriak-kv/3.4.1/')), 'search must not leak other versions');
}
console.log('Architecture, SemVer, OS fallback, data binding, and layered-output tests passed.');
