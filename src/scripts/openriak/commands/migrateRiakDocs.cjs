const fileHelpers = require('../lib/fileHelpers.cjs');
const {
  getDestinationPath,
  getMarkdown
} = require('../lib/migrateHelpers.cjs');
const { format } = require('date-fns');

function flushConsole(callback) {
  const stdoutDrained = process.stdout.write('');
  const stderrDrained = process.stderr.write('');
  if (!stdoutDrained || !stderrDrained) {
    // wait for 'drain' events
    process.stdout.once('drain', () => {
      process.stderr.once('drain', callback);
    });
  } else {
    callback();
  }
}

function migrateRiakDocs(sourcePath, project, version) {
  const fullPath = fileHelpers.resolve(sourcePath);
  if (!fileHelpers.doesFileExist(fullPath)) {
    console.log(`Source path ${fullPath} could not be found.`);
    process.exit(1);
  }

  const destinationPath = getDestinationPath(project, version);

  const ids = getHugoFiles(fullPath);
  console.log(`--- Total Hugo IDs loaded: ${Object.values(ids).length} ---`);

  makeNewIdentifiers(ids);
  for (const [id, md] of Object.entries(ids)) {
    //console.log(`${md.parent} -> ${md.identifier}`);
  }
  console.log(`--- New Identifiers made: ${Object.values(ids).length} ---`);

  for (const [id, md] of Object.entries(ids)) {
    if (md.parent) {
      const parentId = ids[md.parent];
      if (!parentId) {
        console.error(`[ERROR]: ID ${id} has parent ${md.parent} but that does not exist!`);
        process.exit(1);
      }
      const shouldBePath = fileHelpers.join(parentId.identifier, md.file.name);
      if (shouldBePath !== fileHelpers.relative(fullPath, md.filePath)) {
        //console.log(`Note: ${md.identifier} -> ${shouldBePath}`);
        //console.log(`${shouldBePath} !== ${fileHelpers.relative(fullPath, md.filePath)}`);
        md.targetPath = shouldBePath;
      } else {
        // it's where it should be - yay!
        if (md.hasChildren) {
          const realPath = fileHelpers.join(parentId.identifier, md.file.baseName) + '/index.md';
          //console.log(`Note: has children, so: ${md.identifier} -> ${realPath}`);
          md.targetPath = realPath;
        } else {
          //console.log(`Note: no children, so: ${md.identifier} -> ${shouldBePath}`);
          md.targetPath = shouldBePath;
        }
      }
    } else {
      // root item?
      mdRelPath = fileHelpers.relative(fullPath, md.filePath);
      mdParentRelPath = fileHelpers.relative(fullPath, md.parentPath);
      if (!mdParentRelPath) {
        if (md.hasChildren) {
          const realPath = fileHelpers.join(md.file.baseName) + '/index.md';
          //console.log(`Note: has children, so: ${md.identifier} -> ${realPath}`);
          md.targetPath = realPath;
        } else {
          //console.log(`Note: no children, so: ${md.identifier} -> ${mdRelPath}`);
          md.targetPath = fileHelpers.join('index', mdRelPath);
        }
      } else {
        //console.log(`ID ${id} has no parent and should do: ${mdRelPath} (parent: ${mdParentRelPath})`);
        md.targetPath = md.slug?md.slug:(fileHelpers.join(mdParentRelPath, md.identifier));
      }
    }
  }

  console.log(`--- Setting target paths: ${Object.values(ids).length} ---`);

  ids["index"].slug = "/";
  ids["index"].hide_title = true;
  ids["index\/release-notes"].slug = "/release-notes"
  ids["downloads"].slug = "/downloads"

  Object.entries(ids).map(([id, md]) => {
    if (!md.targetPath) {
      console.log(`[ERROR] Missing targetPath: ${id}`)
      console.log(md);
      process.exit(1);
    }
  });

  for (const [id, md] of Object.entries(ids).sort(
    ([keyA, valueA], [keyB, valueB]) => valueA.targetPath.localeCompare(valueB.targetPath)
  )) {
    //console.log(`${md.identifier} -> ${ids[md.identifier].targetPath}`);

    if (id !== md.identifier) {
      console.error(`${id} !== ${md.identifier}`);
      process.exit(1);
    }

    /*
        if (id === "index") {
          console.log(`Found index!`);
          console.log(md);
          process.exit(1);      
        }
    */

    const newMarkdownFrontMatter = {
      title: md.title,
      sidebar_position: md.sidebar_position,
      sidebar_label: md.sidebar_label,
      sidebar_custom_props: md.sidebar_custom_props,
      pagination_label: md.pagination_label,
      hide_table_of_contents: !md.toc,
      slug: md.slug,
      hide_title: md.hide_title,
      last_update: { author: "RiakDocs", date: format(md.rawData.lastmod ? md.rawData.lastmod : new Date(), 'yyyy-MM-dd') }
    };

    const newMarkdownContents = [];
    newMarkdownContents.push('---');
    for (const [key, value] of Object.entries(newMarkdownFrontMatter)) {
      if (value) {
        if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') {
          newMarkdownContents.push(`${key}: ${value}`);
        } else if (typeof value === 'object') {
          //console.log(`Key has object as (${typeof value}) value: ${JSON.stringify(value)}`);
          var hasValue = false;
          Object.values(value).map(subvalue => hasValue = hasValue || subvalue);
          if (hasValue) {
            newMarkdownContents.push(`${key}:`);
            for (const [subkey, subvalue] of Object.entries(value)) {
              if (subvalue) {
                newMarkdownContents.push(`  ${subkey}: ${subvalue}`);
              }
            }
          }
        } else {
          console.log(`Key has object as (${typeof value}) value: ${JSON.stringify(value)}`);
          console.log(value);
          process.exit(1);
        }
      }
    }
    newMarkdownContents.push('---');

    // fix weirdly formed baseurls
    //md.rawContent = md.rawContent.replaceAll(`{{< baseurl >}}`, `{{<baseurl>}}`);
    
    /*
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}community/`, `/community/`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}community`, `/community`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/${project}/latest/`, `/${project}/`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/cs/latest/`, `/cs/`);

    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/cs/2.1.1/`, `/cs/2.1.1/`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/cs/2.1.1`, `/cs/2.1.1`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/${project}/${version}/`, `/${project}/${version}/`);
    md.rawContent = md.rawContent.replaceAll(`{{<baseurl>}}riak/${project}/3.2.0/`, `/${project}/${version}/`);
    */

    const pathSubstitutions = [
      { from: `{{<baseurl>}}data`, to: `/riakdocs-resources/data` },
      { from: `{{<baseurl>}}images`, to: `/riakdocs-resources/images` },
      { from: `{{<baseurl>}}community`, to: `/community` },
      { from: `{{<baseurl>}}riak/kv/latest`, to: `/kv` },
      { from: `{{<baseurl>}}riak/cs/latest`, to: `/cs` },
      { from: `{{<baseurl>}}riak/ts/latest`, to: `/ts` },
      { from: `{{<baseurl>}}riak/`, to: `/` },
      { from: `{{<baseurl>}}`, to: `/` },
      { from: `/kv/2.9.0p5`, to: `/kv/2.9.0` },
    ];
    for (const {from, to} of pathSubstitutions) {
      md.rawContent = md.rawContent.replaceAll(from, to);
    }
    // handle exampledomain and security email
    md.rawContent = md.rawContent.replaceAll(`{{% exampledomain %}}`, `a-riak-user.com`);
    md.rawContent = md.rawContent.replace(`{{<securitycontactusemail>}}`, `security@openriak.org`);

    // handle notes
    md.rawContent = md.rawContent.replaceAll(/{{% note title="([^"]+)" %}}((?:(?!\{\{%).)*){{% \/note %}}/gs, `<RiakDocsNote title="$1">$2</RiakDocsNote>`);
    md.rawContent = md.rawContent.replaceAll(/{{% note %}}((?:(?!\{\{%).)*){{% \/note %}}/gs, `<RiakDocsNote>$1</RiakDocsNote>`);
    md.rawContent = md.rawContent.replaceAll(/(<RiakDocsNote[^>]*>)(((?!\n).)*)\n(<\/RiakDocsNote>)/gs, `$1\n$2\n$4`);

/*
    // should now be handled by global replace above
    const releaseNotesRegExp = new RegExp(`{{<baseurl>}}riak\/(${project})\/([0-9\.]+(p[0-9])?)\/release-notes`, 'gs');
    md.rawContent = md.rawContent.replace(releaseNotesRegExp, `/$1/$2/release-notes`);
    const otherVersionsRegExp = new RegExp(`{{<baseurl>}}riak\/(${project})\/([0-9\.]+(p[0-9])?)s?\/`, 'gs');
    md.rawContent = md.rawContent.replace(otherVersionsRegExp, `/$1/${version}/`);
    md.rawContent = md.rawContent.replace(/: {{<baseurl>}}$/gm, `: `);
*/

    // fix rows
    //md.rawContent = md.rawContent.replaceAll(/<td>(((?!\<\/td\>).)+)<td>/gs, `<td>\n$1\n</td>\n<td>`);
    //md.rawContent = md.rawContent.replaceAll(/<td>(((?!\<\/td\>).)+)<\/tr>/gs, `<td>\n$1\n</td>\n</tr>`);
    //md.rawContent = md.rawContent.replaceAll(/<td>(((?!\<\/td\>).)+)<\/td>/gs, `<td>\n$1\n</td>`);
    //md.rawContent = md.rawContent.replaceAll(/<td>(((?!\<\/td\>).)+)<td>\n<\/tr/gs, `<td>$1\n</td>\n</tr`);
    //md.rawContent = md.rawContent.replaceAll(/<try>/gs, `<tr>`);
    //md.rawContent = md.rawContent.replaceAll(/<\/try>/gs, `</tr>`);
    //md.rawContent = md.rawContent.replaceAll('</td>\n</tr>\n</thead>', `</tr>\n</thead>`);
    //md.rawContent = md.rawContent.replaceAll('<tr>\n\n</td>', `<tr>`);

    // fix tbody and table
    //md.rawContent = md.rawContent.replaceAll(/<table>(((?!\<\/table\>).)+)##/gs, `<table>\n$1\n</table>\n\n##`);
    //md.rawContent = md.rawContent.replaceAll(/<tbody>(((?!\<\/tbody\>).)+)<\/table>/gs, `<tbody>\n$1\n</tbody>\n</table>`);

    // fix bad <li>
    //md.rawContent = md.rawContent.replaceAll(/<\/li$/gm, `</li>`);

    // fix bad <a>
    //md.rawContent = md.rawContent.replaceAll(/(<a [^>]+>)\n([^\n]*)(<\/a>)/gs, `$1$2$3`);

    // fix bad strong consistency links
//    md.rawContent = md.rawContent.replaceAll(`<code><a href="/${project}/${version}/configuring/reference/#strong-consistency)`, `<code><a href="/${project}/${version}/configuring/reference/#strong-consistency">strong consistency</a></code>`);

    // fix specific weird table inner list things
/*
    md.rawContent = md.rawContent.replaceAll(
      `<ul><li><code>Ensemble</code>\n---\nThe ID of the ensemble</li><li><code>Quorum</code>\n---\nThe number of ensemble peers that are either leading or following</li><li><code>Nodes</code>\n---\nThe number of nodes currently online</li><li><code>Leader</code>\n---\nThe current leader node for the ensemble</li></ul>`,
      `<ul><li><code>Ensemble</code> --- The ID of the ensemble</li><li><code>Quorum</code> --- The number of ensemble peers that are either leading or following</li><li><code>Nodes</code> --- The number of nodes currently online</li><li><code>Leader</code> --- The current leader node for the ensemble</li></ul>`
    );
    md.rawContent = md.rawContent.replaceAll(
      `<ul><li><code>Ensemble</code>\n\nThe ID of the ensemble</li><li><code>Quorum</code>\n\nThe number of ensemble peers that are either leading or following</li><li><code>Nodes</code>\n\nThe number of nodes currently online</li><li><code>Leader</code>\n\nThe current leader node for the ensemble</li></ul>    `,
      `<ul><li><code>Ensemble</code> --- The ID of the ensemble</li><li><code>Quorum</code> --- The number of ensemble peers that are either leading or following</li><li><code>Nodes</code> --- The number of nodes currently online</li><li><code>Leader</code> --- The current leader node for the ensemble</li></ul>`
    );
    md.rawContent = md.rawContent.replaceAll(
      `<ul><li><code>Ensemble</code>\n\nThe ID of the ensemble</li><li><code>Quorum</code>\n\nThe number of ensemble peers that are either leading or following</li><li><code>Nodes</code>\n\nThe number of nodes currently online</li><li><code>Leader</code>\n\nThe current leader node for the ensemble</li></ul>`,
      `<ul><li><code>Ensemble</code> --- The ID of the ensemble</li><li><code>Quorum</code> --- The number of ensemble peers that are either leading or following</li><li><code>Nodes</code> --- The number of nodes currently online</li><li><code>Leader</code> --- The current leader node for the ensemble</li></ul>`
    );

    md.rawContent = md.rawContent.replaceAll(
      `<ul><li><code>Peer</code>\n---\nThe ID of the peer</li><li><code>Status</code>\n---\nWhether the peer is a leader or a follower</li><li><code>Trusted</code>\n---\nWhether the peer's Merkle tree is currently considered trusted or not</li><li><code>Epoch</code>\n---\nThe current consensus epoch for the peer. The epoch is incremented each time the leader changes.</li><li><code>Node</code>\n---\nThe node on which the peer resides.</li></ul>`,
      `<ul><li><code>Peer</code> --- The ID of the peer</li><li><code>Status</code> --- Whether the peer is a leader or a follower</li><li><code>Trusted</code> --- Whether the peer's Merkle tree is currently considered trusted or not</li><li><code>Epoch</code> --- The current consensus epoch for the peer. The epoch is incremented each time the leader changes.</li><li><code>Node</code> --- The node on which the peer resides.</li></ul>`
    );
    md.rawContent = md.rawContent.replaceAll(
      `<ul><li><code>Peer</code>\n\nThe ID of the peer</li><li><code>Status</code>\n\nWhether the peer is a leader or a follower</li><li><code>Trusted</code>\n\nWhether the peer's Merkle tree is currently considered trusted or not</li><li><code>Epoch</code>\n\nThe current consensus epoch for the peer. The epoch is incremented each time the leader changes.</li><li><code>Node</code>\n\nThe node on which the peer resides.</li></ul>`,
      `<ul><li><code>Peer</code> --- The ID of the peer</li><li><code>Status</code> --- Whether the peer is a leader or a follower</li><li><code>Trusted</code> --- Whether the peer's Merkle tree is currently considered trusted or not</li><li><code>Epoch</code> --- The current consensus epoch for the peer. The epoch is incremented each time the leader changes.</li><li><code>Node</code> --- The node on which the peer resides.</li></ul>`
    );

    md.rawContent = md.rawContent.replaceAll(
      `<ul><li>\`connected\`\n---\nThe IP address and port of a connected client (site)</li><li>\`cluster_name\`\n---\nThe name of the connected client (site)</li><li>\`connecting\`\n---\nThe PID, IP address, and port of a client currently establishing a connection</li></ul>`,
      `<ul><li>\`connected\` --- The IP address and port of a connected client (site)</li><li>\`cluster_name\` --- The name of the connected client (site)</li><li>\`connecting\` --- The PID, IP address, and port of a client currently establishing a connection</li></ul>`
    );

    // fix non-self-closing <br>
    md.rawContent = md.rawContent.replaceAll(
      `<br>`,
      `<br />`
    );
*/
/*
    // fix non-self-closing <img>
    md.rawContent = md.rawContent.replaceAll(
      /<img ([^>]*)>/gs,
      `<img $1 />`
    );
    md.rawContent = md.rawContent.replaceAll(
      /<img ([^>]*)\/ \/>/gs,
      `<img $1 />`
    );
    // fix non-self-closing <input>
    md.rawContent = md.rawContent.replaceAll(
      /<input ([^>]*)>/gs,
      `<input $1 />`
    );

    if (md.rawContent.includes(`[client libraries]: /kv/3.0.15/developing/client-libraries/`)) {
      md.rawContent = md.rawContent.replaceAll(
        `\n\n[client libraries]: /kv/3.0.15/developing/client-libraries/`,
        ``
      );
      md.rawContent = `[client libraries]: /kv/3.0.15/developing/client-libraries/\n\n` + md.rawContent
    }
*/
/*
    md.rawContent = md.rawContent.replaceAll(
      `>     client = Riak::Client.new(nodes: [
>       {host: '10.0.0.1'},
>       {host: '10.0.0.2'},
>       {host: '10.0.0.3'}
>     ])`,
      `> \`\`\`
> client = Riak::Client.new(nodes: [
>   {host: '10.0.0.1'},
>   {host: '10.0.0.2'},
>   {host: '10.0.0.3'}
> ])
> \`\`\``
    );
*/
    /*
    md.rawContent = md.rawContent.replaceAll(`**<figure`, `<figure`);
    md.rawContent = md.rawContent.replaceAll(`<figcaption>`, `<figcaption><i>`);
    md.rawContent = md.rawContent.replaceAll(`</figcaption>`, `</i></figcaption>`);
    md.rawContent = md.rawContent.replaceAll(`</figure>**`, `</figure>`);
    */

    var useRiakDocsFigure = false;
    const figureRegExp = /\*\*<figure\s+id="([^"]+)"[^>]+>\s+<img\s+src="([^"]+)"[^>]*\/?>\s+<figcaption>\s*([^<]+)\s*<\/figcaption>\s*<\/figure>\*\*/gsm;
    //const figureRegExp = /figure/gm;
    for (const match of md.rawContent.matchAll(figureRegExp)) {
      const text = match[0];
      const id = match[1];
      const url = match[2];
      const caption = match[3].trim();
      md.rawContent = md.rawContent.replaceAll(
        text,
        `<RiakDocsFigure id="${id}" url="${url}">${caption}</RiakDocsFigure>`
      )
      useRiakDocsFigure = true;
    }
    if (useRiakDocsFigure) {
      md.rawContent = `import RiakDocsFigure from '@site/src/components/RiakDocs/RiakDocsFigure';\n\n` + md.rawContent;
    }

    md.rawContent = md.rawContent.replaceAll(`<http://127.0.0.1:8098/admin></a>`, `[http://127.0.0.1:8098/admin](http://127.0.0.1:8098/admin)`);
    md.rawContent = md.rawContent.replaceAll(`<https://localhost:8069/admin>`, `[https://localhost:8069/admin](https://localhost:8069/admin)`);
/*
    md.rawContent = md.rawContent.replaceAll(
      `    <div class=info>
    <div class=title>`,
      `    <div class="info">
    <div class="title">`
    )
*/
    md.rawContent = md.rawContent.replaceAll(`<\`PID\`>`, `&lt;\`PID\`&gt;`);
    md.rawContent = md.rawContent.replaceAll(`[...{almost_current_function,...]`, `[...&#123;almost_current_function,...]`);

/*
    md.rawContent = md.rawContent.replaceAll(
      `\`Could not parse field
<Field>, value <Value>.\``,
      `\`Could not parse field <Field>, value <Value>.\``
    );
*/
    const wrapWithBackticks = [
      `{total_count,100}`,
      `{total_size,500000}`,
      `{sizes,[{1,90},{2,5},{3,4}]}`,
      `{siblings,[{1,90},{2,6},{3,4}]}`,
      `[{"ID",KBytes_Used,Percent_Util}]`,
      `{riak_kv_multi_backend, undefined_backend, BackendName}`,
      `{suppressed,port_events,1}`,
      `{suppressed,port_events,1}`,
      `{error,eaddrinuse}`,
      `{Bucket, Key, Clock, {tombstone, Object}};`,
      `{Bucket, Key, Clock, {object, Object}};`,
      `{Bucket, Key, Clock, to_fetch}.`,
      `riak admin transfer-limit <limit>`,
      `{'EXIT', {badarg, [{ets,lookup, [schema_table,<<"search-example">>], []} {riak_search_config,get_schema,1, [{file,"src/riak_search_config.erl"}, {line,69}]} ...`,
    ]
    for (block of wrapWithBackticks) {
      //console.log(`Fixing: ${block}`);
      md.rawContent = md.rawContent.replaceAll(block, `\`` + block.trim() + `\``);
    }

    const wrapWithSpacesAndBackticks = [
      `{object, Object}`,
    ]
    for (block of wrapWithSpacesAndBackticks) {
      //console.log(`Fixing: ${block}`);
      md.rawContent = md.rawContent.replaceAll(` ` + block + ` `, ` \`` + block.trim() + `\` `);
    }


    md.rawContent = md.rawContent.replaceAll(
      `style="width: 100%; border-spacing: 0px;"`,
      `style={{width: '100%', borderSpacing: '0px'}}`
    );
    md.rawContent = md.rawContent.replaceAll(
      `style="padding: 15px; margin: 15px; border-width: 1px 0 1px 0; border-style: solid;"`,
      `style={{padding: '15px', margin: '15px', borderWidth: '1px 0 1px 0', borderStyle: 'solid'}}`
    );
    md.rawContent = md.rawContent.replaceAll(
      `style="display:none"`,
      `style={{display: 'none'}}`
    );
    md.rawContent = md.rawContent.replaceAll(
      `style="text-align:center;font-style:italic"`,
      `style={{textAlign: 'center', fontStyle: 'italic'}}`
    );
    md.rawContent = md.rawContent.replaceAll(
      `style="text-align:center;"`,
      `style={{textAlign: 'center'}}`
    );

    md.rawContent = md.rawContent.replaceAll(
      `<cod>`,
      `<code>`
    );

    // add RiakDocsNote import to all
    md.rawContent = `import RiakDocsNote from '@site/src/components/RiakDocs/RiakDocsNote';\n\n` + md.rawContent;

    // 2 - project, 4 - version, 5 - path
    const linksRegExps = [
      { pattern: /\[([^\]]+)\]\(\/(kv|cs|ts|blog|community)\/(([0-9\.]+)\/)?([^)]+)\)/gm,  replacement: "[text](url)", debug: false },
      { pattern: /^\[([^\]]+)\]:\s*\/(kv|cs|ts|blog|community)\/(([0-9\.]+)\/)?(.+)$/gm, replacement: "[text]: url", debug: false }
    ]

    for (const {pattern, replacement, debug} of linksRegExps) {
      for (const match of md.rawContent.matchAll(pattern)) {
        const text = match[0];
        const linkText = match[1];
        const linkProject = match[2];
        const linkVersion = match[4];
        const linkPath = match[5];
        const linkSuffix = linkPath.endsWith('/')?'':'/';

        if (debug) console.log("[Links] Found: " + text);

        if (linkProject === project) {// && linkVersion == version) {
          // if no link version, then it was meant to go to latest - which is now nonsensical. So go to THIS version.
          const linkFullPath = (linkVersion ? fileHelpers.join(linkProject, linkVersion, linkPath) : fileHelpers.join(linkProject, version, linkPath)) + linkSuffix;
          const mdFullPath = fileHelpers.join(project, version, (md.slug ? md.slug : md.identifier)) + '/';
          const relativePathToHere = fileHelpers.relative(mdFullPath, linkFullPath);

          /*
          console.log("Link Project:            " + linkProject);
          console.log("Link Version:            " + linkVersion);
          console.log("Link Path:               " + linkPath);
          console.log("LinkFullPath:            " + linkFullPath);
          console.log("This Project:            " + project);
          console.log("This Version:            " + version);
          console.log("This Page MD Identifier: " + md.identifier);
          console.log("This Page ID FullPath:   " + fileTargetFullPath);
          console.log("Relative URL:            " + relativePathToHere);
          */
          const replaceText = replacement.replace("text", linkText).replace("url", `./${relativePathToHere}`)
          
          if (debug) console.log("[Links]   ->: " + replaceText);

          md.rawContent = md.rawContent.replaceAll(
            text,
            replaceText,
          )
        } else {
          // link to another project (i.e. kv linking to cs)
          // so for now remove /docs/ from the root to ensure compatibility with moving
          /*
          console.log("Link Project:            " + linkProject);
          console.log("Link Version:            " + linkVersion);
          console.log("Link Path:               " + linkPath);
          console.log("This Project:            " + project);
          console.log("This Version:            " + version);
          console.log(`Link Project is ${linkProject}/${linkVersion} but this project is ${project}/${version}.`)
          */

          const replaceText = replacement.replace("text", linkText).replace("url", `/${linkProject}/${linkVersion ? (linkVersion + '/') : ''}${linkPath}`)
          md.rawContent = md.rawContent.replaceAll(
            text,
            replaceText,
          )
          //process.exit(1);
        }
      }
    }
    /*
        const definedLinks = /^\[([^\]]+)\]:\s*\/docs\/(kv|cs|ts|blog|community)\/(([0-9\.]+)\/)?(.+)$/gm;
        for (const match of md.rawContent.matchAll(definedLinks)) {
          const linkProject = match[2];
          const linkVersion = match[4];
          const linkPath = match[5];
    
          if (linkProject === project) { // && linkVersion == version) {
            const linkFullPath = linkVersion?fileHelpers.join(linkProject, linkVersion, linkPath):fileHelpers.join(linkProject, version, linkPath);
            const mdFullPath = fileHelpers.join(project, version, (md.slug?md.slug:md.identifier));
            const relativePathToHere = fileHelpers.relative(mdFullPath, linkFullPath);
    */
    /*
            console.log("Link Project:            " + linkProject);
            console.log("Link Version:            " + linkVersion);
            console.log("Link Path:               " + linkPath);
            console.log("LinkFullPath:            " + linkFullPath);
            console.log("This Project:            " + project);
            console.log("This Version:            " + version);
            console.log("This Page MD Identifier: " + md.identifier);
            console.log("This Page ID FullPath:   " + fileTargetFullPath);
            console.log("Relative URL:            " + relativePathToHere);
    */
    /*
            //process.exit(1);
            const from = `/docs/${linkProject}/${linkVersion}/${linkPath}`;
            const to = `./${relativePathToHere}`;
            console.log(`${from} --> ${to}`);
            md.rawContent = md.rawContent.replaceAll(
              from,
              to
            )
          } else {
    +/
            /*
            console.log("Link Project:            " + linkProject);
            console.log("Link Version:            " + linkVersion);
            console.log("Link Path:               " + linkPath);
            console.log("This Project:            " + project);
            console.log("This Version:            " + version);
            console.log(`Link Project is ${linkProject}/${linkVersion} but this project is ${project}/${version}.`)
            */
    /*
            md.rawContent = md.rawContent.replaceAll(
              `/docs/${linkProject}/${linkVersion?(linkVersion+'/'):''}${linkPath}`,
              `/${linkProject}/${linkVersion?(linkVersion+'/'):''}${linkPath}`,
            )
            //process.exit(1);
          }
        }
    */
    newMarkdownContents.push(md.rawContent);

    const newMarkdownFileContent = newMarkdownContents.join('\n');
    const destinationFilePath = fileHelpers.join(destinationPath, md.targetPath);

    //console.log(destinationFilePath);
    fileHelpers.setFileContent(destinationFilePath, newMarkdownFileContent);
    if (md.identifier === 'index') {
      //process.exit(1);
    }

    const noCodeBlocks = md.rawContent.replace(/```[\s\S]*?```/g, '');
    const noInlineCode = noCodeBlocks.replace(/`[^`]*`/g, '');

    if (noInlineCode.match(/(?<![`=]){{/gs)) {
      console.log(`{{ found in content. Check ${md.filePath}`);
      process.exit(1);
    }
  }
}

function makeNewIdentifiers(sourceIds) {
  // place them into filename order
  const sortedById = Object.values(sourceIds).sort(
    (valueA, valueB) => valueA.filePath.localeCompare(valueB.filePath)
  );

  //console.log(`--- Sorted: ${sortedById.length} ---`);

  const reorganisedIds = {};
  sortedById.map((md) => {
    md.newIdentifier = getNewId(sourceIds, md);
    //console.log(`[DEBUG] New identifier ${md.newIdentifier}`);
  });

  sortedById.map((md) => {
    if (md.parent) {
      const parentMd = sourceIds[md.parent];
      if (!parentMd) {
        console.error(`[ERROR] Has parent but not found!}`);
        console.error(item);
        process.exit(1);
      }
      md.parent = parentMd.newIdentifier;
      parentMd.hasChildren = true;
    }
  });

  sortedById.map((md) => {
    delete sourceIds[md.identifier];
    md.oldIdentifier = md.identifier;
    md.identifier = md.newIdentifier;
    sourceIds[md.identifier] = md;
  });
}

function getNewId(sourceIds, item) {
  //console.log(item.identifier);
  if (item.parent) {
    //console.log(`[DEBUG] Item Parent ${item.parent}`);
    if (sourceIds[item.parent]) {
      return getNewId(sourceIds, sourceIds[item.parent]) + '/' + item.file.baseName;
    } else {
      console.error(`[ERROR] Has parent but not found!}`);
      console.error(item);
      process.exit(1);
    }
  } else {
    return item.file.baseName;
  }
}

function getHugoFiles(folderPath, knownIds = {}) {
  var resultIds = {};
  //if (folderPath.endsWith("deprecated")) { return;}
  fileHelpers.forFiles(folderPath, (file) => {
    if (file.name.startsWith('_')) return;
    if (file.isFile) {
      const potentialChildDir = fileHelpers.join(file.parentPath, file.baseName);
      if (fileHelpers.doesFileExist(potentialChildDir)) {
        //console.log(`${file.name} is really an index file for ${potentialChildDir}`);
      } else {
        //console.log(`${file.name} is a normal content file ${file.parentPath}`);
      }
      const markdown = getMarkdown(file.fullPath);
      // return first item
      //console.log(markdown);
      var markdownMenu = null;
      var id = file.name;
      var parent = '';
      if (markdown.data.menu) {
        markdownMenu = Object.values(markdown.data.menu).find((item) => true) ?? null;
        if (!markdownMenu.identifier) {
          console.error(`No ID:   ${file.fullPath}`);
          process.exit(1);
        } else {
          //console.log(`ID:      ${file.fullPath}`);
          id = markdownMenu.identifier;
        }
        if (!markdownMenu.parent) {
          //console.log(`No parent: ${file.fullPath}`);
        } else {
          parent = markdownMenu.parent;
        }
      } else {
        //console.log(`No menu:   ${file.fullPath}`);
      }
      if (knownIds[id] || resultIds[id]) {
        console.log(`ID clash:  ${file.fullPath}`);
      } else {
        if (markdown.data.draft) {
          //console.log(`File ${file.fullPath} is a draft, so skipping.`);
        } else if (markdown.data.layout && markdown.data.layout === 'redirect') {
          //console.log(`File ${file.fullPath} is a redirect, so skipping.`);
        } else {
          resultIds[id] = {
            rawData: markdown.data,
            file: file,
            filePath: file.fullPath,
            identifier: id,
            parentPath: fileHelpers.getParentFolder(file.fullPath),
            title: `"` + markdown.data.title + `"`,
            sidebar_position: markdownMenu?.weight ?? '',
            sidebar_label: markdownMenu?.name ?? `"` + markdown.data.title + `"`,
            sidebar_icon: markdownMenu?.pre ?? '',
            pagination_label: `"` + markdown.data.title + `"`,
            toc: markdown.toc ? true : false,
            parent: markdownMenu?.parent ?? '',
            rawContent: markdown.content,
          };
        }

      }
    } else if (file.isDirectory) {
      childIds = getHugoFiles(file.fullPath, knownIds);
      const duplicateKeys = Object.keys(childIds).filter(key => key in resultIds);
      if (duplicateKeys.length > 0) {
        throw new Error(`Duplicate keys found: ${duplicateKeys.join(', ')}`);
      }
      resultIds = { ...resultIds, ...childIds };
      //results.push(...childResults);
    } else {
      console.error(`Unknown file type:`);
      console.error(file);
      process.exit(1);
    }
  });

  const duplicateKeys = Object.keys(knownIds).filter(key => key in resultIds);
  if (duplicateKeys.length > 0) {
    throw new Error(`Duplicate keys found: ${duplicateKeys.join(', ')}`);
  }
  const result = { ...knownIds, ...resultIds };

  return result;
}

module.exports = {
  migrateRiakDocs
};
