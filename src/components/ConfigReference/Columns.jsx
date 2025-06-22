import React from "react";
import Link from "@docusaurus/Link";
import MarkdownRenderer from './MarkdownRenderer';
import InlineCodeWithCopy from "@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy";
import ChosenOS from "@site/src/components/OSSelection/ChosenOS";
import { useLocation } from '@docusaurus/router';
import ScrollToClosestLink from './ScrollToClosestLink';

export function getAnchorFromName(name) {
    return name.replace(/[^a-zA-Z0-9-_]/g, '_');
}

export function getComments(info) {
    const item = info.getValue();
    return getCommentsFromItem(item);
}

export function getCommentsFromItem(item) {
    const textProperty = item?.docText ?? '';

    if (textProperty) {
        return <MarkdownRenderer markdown={textProperty.join('\n')} />;
    }
}

export function getSees(info, extras) {
    const item = info.getValue();
    return getSeesFromItem(item, extras);
}

export function getSeesFromItem(item, extras) {
    const seesProperty = item?.docSees ?? '';
    var location = useLocation();
    //console.log(location);

    const segments = location.pathname.split("/").filter(Boolean); // removes empty segments
    const index = segments.indexOf("configure");
    if (index !== -1) {
        location = "/" + segments.slice(0, index + 1).join("/");
        //console.log("Base path:", location);
    }

    const outputItems = [];

    if (seesProperty) {
        seesProperty.map((text, index) => {
            const anchor = getAnchorFromName(text);
            outputItems.push(<ScrollToClosestLink className="relatedPage seeAlso" key={'alsoSeeLink-'+index} linkText={text} targetId={anchor} closestSelector="tr" />);
        })
    }

    if (extras && extras.configs && extras.links) {
        Object.entries(extras.configs).filter(([key,value]) => {
            try {
                const regExp = new RegExp(key);
                return (item.configName.match(regExp));
            } catch (err) {
                console.log(err);
                throw err;
            }
        }).map(([key, value], entryIndex) => {
            const relatedPages = value.relatedPages || [];
            relatedPages.map((relatedPage, index) => {
                // PJAC
                const relatedPageLink = extras.links[relatedPage];
                if (relatedPageLink) {
                    const url = relatedPageLink.url;
                    outputItems.push(<Link className="relatedPage extra" key={'relatedPage-'+entryIndex+'-'+index} to={location + relatedPageLink.url}>{relatedPageLink.text}</Link>);
                }
            });
        });
    }
    return outputItems;
}

export function getDefaultValue(info) {
    const item = info.getValue();
    return getDefaultValueFromItem(item, false);
}

export function getDefaultValueFromItem(item, hidePlatform) {
    const properties = item?.properties ?? '';
    var defaultProperty = properties?.default ?? '';

    var defaultPropertyOutput = <></>;

    if (defaultProperty) {
        switch (typeof defaultProperty) {
        case 'string':
            defaultPropertyOutput = <InlineCodeWithCopy>{String(defaultProperty || '')}</InlineCodeWithCopy>
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
            defaultPropertyOutput = <InlineCodeWithCopy>{defaultValues.join(":")}</InlineCodeWithCopy>;
            break;
        default:
            throw new Error(`Unknown typeof default ${typeof defaultProperty} with value ${JSON.stringify(defaultProperty, null, 0)}`);
        }
    } else {
        defaultPropertyOutput = <i>no default value</i>;
    } 

    if (properties.defaultHasPlaceholder === true && !hidePlatform) {
        return <>{defaultPropertyOutput} on <ChosenOS /></>
    } else {
        return defaultPropertyOutput;
    }

}

export function getDataTypeList(info) {
    const item = info.getValue();
    return getDataTypeListFromItem(item);
}

export function getDataTypeListFromItem(item) {
    const properties = item?.properties ?? '';
    const datatypeProperty = properties?.datatype ?? '';

    const returnedElements = [];

    var datatypeValue = datatypeProperty;
    // set default type to string
    if (!datatypeValue) { datatypeValue = { "type": "atom", "value": "string" } }
    
    if (!Array.isArray(datatypeValue)) {
        datatypeValue = [datatypeValue];
    }
    const listElements = [];
    datatypeValue.map((item, index) => {
        switch (typeof item) {
            case 'string': 
                listElements.push(<React.Fragment key="string">{item}</React.Fragment>);
                break;
            case 'object': 
                switch (item.type) {
                    case 'atom':
                        if (typeof item.value === 'object') {
                            switch (item.value.type) {
                                case 'atom':
                                    listElements.push(<InlineCodeWithCopy key="atomAtomValue">{item.value.value}</InlineCodeWithCopy>);
                                    break;
                                default:
                                    throw new Error(`Unknown atom value type ${item.value.type} with value ${JSON.stringify(item.value, null, 0)}`);  
                            }
                        } else {
                            switch (item.value) {
                                case 'flag':
                                    listElements.push(<InlineCodeWithCopy key="flagOn">on</InlineCodeWithCopy>);
                                    listElements.push(<InlineCodeWithCopy key="flagOff">off</InlineCodeWithCopy>);
                                    break;
                                case 'integer':
                                case 'atom':
                                    listElements.push(<React.Fragment key="genericAn">an <InlineCodeWithCopy>{item.value}</InlineCodeWithCopy></React.Fragment>);
                                    break;
                                case 'bytesize':
                                    listElements.push(<React.Fragment key="bytesize">a <InlineCodeWithCopy>{item.value}</InlineCodeWithCopy> in bytes</React.Fragment>);
                                    break;
                                case 'ip':
                                    listElements.push(<React.Fragment key="ip">an <InlineCodeWithCopy>IP address</InlineCodeWithCopy></React.Fragment>);
                                    break;
                                case 'file':
                                case 'directory':
                                case 'string':
                                case 'float':
                                case 'boolean':
                                    listElements.push(<React.Fragment key="genericA">a <InlineCodeWithCopy>{item.value}</InlineCodeWithCopy></React.Fragment>);
                                    break;
                                default: 
                                    throw new Error(`Unknown value type ${item.type} with value ${JSON.stringify(item.value, null, 0)}`);  
                            }
                        }
                        break;
                    case 'enum':
                        item.possibleValues.map((posVal, posIdx) => {
                            switch (posVal.type) {
                                case 'atom': 
                                    listElements.push(<InlineCodeWithCopy key={'enumAtom-'+posIdx}>{posVal.value}</InlineCodeWithCopy>);
                                    break;
                                case 'text': 
                                    listElements.push(<InlineCodeWithCopy key={'enumText-'+posIdx}>{posVal.value}</InlineCodeWithCopy>);
                                    break;
                                default:
                                    throw new Error(`Unknown enum type ${posVal.type} with value ${JSON.stringify(posVal.value, null, 0)}`);
                            }
                        });
                        break;
                    case 'integer':
                        listElements.push(<InlineCodeWithCopy key="integer">{item.value}</InlineCodeWithCopy>);
                        break;
                    case 'flag':
                        listElements.push(<InlineCodeWithCopy key="flagOn">{item.trueValue || 'on'}</InlineCodeWithCopy>);
                        listElements.push(<InlineCodeWithCopy key="flagOff">{item.falseValue || 'off'}</InlineCodeWithCopy>);
                        break;
                    case 'duration':
                        var unitMessage = '';
                        switch (item.unit) {
                            case 'ms':
                                unitMessage = "measured in millseconds (1/1000 of a second)";
                                break;
                            case 's':
                                unitMessage = "measured in seconds";
                                break;
                            case 'm':
                                unitMessage = "measured in minutes (60 seconds)";
                                break;
                            default:
                                throw new Error(`Unknown unit for duration value ${JSON.stringify(item.unit, null , 0)}`);
                        }
                        listElements.push(<React.Fragment key="duration">a <InlineCodeWithCopy>duration</InlineCodeWithCopy> {unitMessage}</React.Fragment>);
                        break;
                    case 'percent':
                        var scaleMessage = '';
                        switch (item.unit.value) {
                            case 'float':
                                scaleMessage = <>as a <InlineCodeWithCopy>float</InlineCodeWithCopy> between 0 and 1.</>
                                break;
                            case 'integer':
                                scaleMessage = <>as a <InlineCodeWithCopy>integer</InlineCodeWithCopy> between 0 and 100.</>
                                break;    
                            default:
                                throw new Error(`Unknown unit for percent with value ${JSON.stringify(item.unit, null , 0)}`);
                        }
                        listElements.push(<React.Fragment key="percent">a <InlineCodeWithCopy>percentage</InlineCodeWithCopy> {scaleMessage}</React.Fragment>);
                        break;
                    default:
                        throw new Error(`Unknown datatype ${item.type} with values scale for percent with value ${JSON.stringify(item, null , 0)}`);
                }
                break;
            default:
                listElements.push(<span key="defaultString" className="cuttlefishDefault">a <InlineCodeWithCopy>string</InlineCodeWithCopy></span>);
        }
    })
    if (listElements.length > 1) {
        returnedElements.push(<i key='typesHeader'>One of:</i>);
        returnedElements.push(  
            <ul key='typesValues'>
            {listElements.map((item, index) => {
                return <li key={'typesValue-'+index}>{item}</li>
            })}
            </ul>
        );
    } else {
        returnedElements.push(<React.Fragment key="soleDataType">{listElements}</React.Fragment>);
    }
    
    return returnedElements;
}
