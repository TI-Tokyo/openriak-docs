import React from "react";
import Link from "@docusaurus/Link";
import MarkdownRenderer from './MarkdownRenderer';

export function getAnchorFromName(name) {
    return name.replace(/[^a-zA-Z0-9-_]/g, '_');
}

export function getComments(info) {
    const item = info.getValue();
    const textProperty = item?.docText ?? '';

    if (textProperty) {
        return <MarkdownRenderer markdown={textProperty.join('\n')} />;
    }
/*
    const outputItems = [];

    if (textProperty) {
        var textBuffer = [];
        textProperty.map((text, index) => {
            if (text) {
                textBuffer.push(text);
            } else {
                if (textBuffer.length > 0) {
                    outputItems.push(<p key={'docText-'+index}>{textBuffer.join(' ')}</p>);
                }
                textBuffer = [];
            }
        })
        if (textBuffer.length > 0) {
            outputItems.push(<p className="docText-final" key={'docText-final'}>{textBuffer.join(' ')}</p>);
        }
    }
    return outputItems;
*/
}

export function getSees(info, relatedPages) {
    const item = info.getValue();
    const seesProperty = item?.docSees ?? '';

    const outputItems = [];

    if (seesProperty) {
        seesProperty.map((text, index) => {
            const anchor = getAnchorFromName(text);
            outputItems.push(<Link key={'alsoSeeLink-'+index} to={'#'+anchor}>{text}</Link>);
        })
    }

    if (relatedPages && item.configName && relatedPages[item.configName] && relatedPages[item.configName].relatedPages) {
        relatedPages[item.configName].relatedPages.map((item, index) => {
            outputItems.push(<Link key={'relatedPages-'+index} to={item.url}>{item.text}</Link>);
        });
    }

    return outputItems;
}


export function getDefaultValue(info) {
    const item = info.getValue();
    const properties = item?.properties ?? '';
    var defaultProperty = properties?.default ?? '';

    var defaultPropertyOutput = <></>;

    if (defaultProperty) {
        switch (typeof defaultProperty) {
        case 'string':
            defaultPropertyOutput = <code>{String(defaultProperty || '')}</code>
            break;
        case 'object':
            if (!Array.isArray(defaultProperty)) {
                defaultProperty = [defaultProperty];
            }
            const defaultValues = defaultProperty.map(item => {
                switch (item.type) {
                    case 'atom':
                    case 'text': return item.value;break;
                    default:
                        throw new Error(`Unknown default value object type ${typeof item.type} with value ${JSON.stringify(item, null, 0)}`);
                }
            });
            defaultPropertyOutput = <code>{defaultValues.join(":")}</code>;
            break;
        default:
            throw new Error(`Unknown typeof default ${typeof defaultProperty} with value ${JSON.stringify(defaultProperty, null, 0)}`);
        }
    } else {
        defaultPropertyOutput = <i>no default value</i>;
    } 

    return defaultPropertyOutput;
}

export function getDataTypeList(info) {
    const item = info.getValue();
    const properties = item?.properties ?? '';
    const datatypeProperty = properties?.datatype ?? '';

    const returnedElements = [];

    var datatypeValue = datatypeProperty;
    // set default type to string
    if (!datatypeValue) { datatypeValue = { "type": "atom", "value": "string" } }
    
    if (!Array.isArray(datatypeValue)) {
        datatypeValue = [datatypeValue];
    }
    if (datatypeValue.length > 1) { returnedElements.push(<i key='typesHeader'>One of:</i>); }
    returnedElements.push(  
        <ul key='typesValues'
            style={
                datatypeValue.length === 1
                ? { listStyle: 'none', padding: 0, margin: 0, display: 'inline' }
                : undefined
            }
        >
        {
            datatypeValue.map((item, index) => {
                switch (typeof item) {
                    case 'string': 
                        return <li key={index}>{item}</li>
                    case 'object': 
                        switch (item.type) {
                            case 'atom':
                                if (typeof item.value === 'object') {
                                    switch (item.value.type) {
                                    case 'atom':
                                        return <li key={index}><code>{item.value.value}</code></li>
                                    default:
                                        return <li key={index}><b>Object: {JSON.stringify(item.value,null,0)}</b></li>
                                    }
                                    return <li key={index}>Object: {JSON.stringify(item.value,null,0)}</li>
                                } else {
                                    switch (item.value) {
                                    case 'flag':
                                        return <li key={index}><i>One of:</i><ul><li key={index+'-1'}><code>on</code></li><li key={index+'-2'}><code>off</code></li></ul></li>
                                    case 'integer':
                                    case 'atom':
                                        return <li key={index}>an <code>{item.value}</code></li>
                                    case 'bytesize':
                                        return <li key={index}>a <code>{item.value}</code> in bytes</li>
                                    case 'ip':
                                        return <li key={index}>an <code>IP address</code></li>
                                    case 'file':
                                    case 'directory':
                                    case 'string':
                                    case 'float':
                                    case 'boolean':
                                        return <li key={index}>a <code>{item.value}</code></li>
                                    default: 
                                        throw new Error(`Unknown value type ${item.type} with value ${JSON.stringify(item.value, null, 0)}`);  
                                    }
                                }
                            case 'enum':
                                const enumItems = item.possibleValues.map((posVal, posIdx) => {
                                    switch (posVal.type) {
                                    case 'atom': 
                                        return <li key={index+'-b-'+posIdx}><code>{posVal.value}</code></li>
                                    case 'text': 
                                        return <li key={index+'-b-'+posIdx}><code>{posVal.value}</code></li>
                                    default:
                                        throw new Error(`Unknown enum type ${posVal.type} with value ${JSON.stringify(posVal.value, null, 0)}`);
                                    }
                                });
                                return (
                                    <React.Fragment key={index}>
                                    {datatypeValue.length === 1 ? (
                                    <li key={index+'-a'}>
                                    <i>One of:</i>
                                    <ul key={index+'-b'}>
                                    {enumItems}
                                    </ul>
                                    </li>
                                    ) : ( enumItems )}
                                    </React.Fragment>
                                );
                            case 'integer':
                                return <li key={index}><code>{item.value}</code></li>
                            case 'flag':
                                return <li key={index}><i>One of:</i><ul><li key={index+'-1'}><code>{item.falseValue || 'off'}</code></li><li key={index+'-2'}><code>{item.trueValue || 'on'}</code></li></ul></li>
                            case 'duration':
                                switch (item.unit) {
                                    case 'ms':
                                        return <li key={index}>a <code>duration</code> measured in millseconds (1/1000 of a second)</li>
                                    case 's':
                                        return <li key={index}>a <code>duration</code> measured in seconds</li>
                                    case 'm':
                                        return <li key={index}>a <code>duration</code> measured in minutes (60 seconds)</li>
                                    default:
                                        return <li key={index}><b>DEBUG: Cannot handle duration datatype type with values {JSON.stringify(item, null , 0)}</b></li>    
                                }
                            case 'percent':
                                switch (item.unit.value) {
                                    case 'float':
                                        return <li key={index}>a <code>percentage</code> as a <code>float</code> between 0 and 1.</li>
                                    case 'integer':
                                        return <li key={index}>a <code>percentage</code> as an <code>integer</code> between 0 and 100.</li>
                                    default:
                                        return <li key={index}><b>DEBUG: Cannot handle percent datatype type with values {JSON.stringify(item, null , 0)}</b></li>    
                                }
                            default:
                                return <li key={index}><b>DEBUG: Cannot handle datatype type {item.type} with values {JSON.stringify(item, null , 0)}</b></li>
                        }
                    default:
                    return <li key={index}><span className="cuttlefishDefault"><code>string</code></span></li>
                }
            })
        }
        </ul>
    );
    return returnedElements;
}
