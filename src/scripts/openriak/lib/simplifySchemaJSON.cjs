function simplifySchemaJSON(schemaInputObject) {
    const result = { mappings: {}, translations: {}, validators: {} }

    for (topLevelBlock of schemaInputObject) {
        switch (topLevelBlock.type) {
            case 'mapping': 
                const mappingName = topLevelBlock.configName;
                const mappingValue = simplifyMapping(topLevelBlock);
                result.mappings[mappingName] = mappingValue;
                break;
            case 'translation':
                const translationName = topLevelBlock.configName;
                const translationValue = simplifyTranslation(topLevelBlock);
                result.translations[translationName] = translationValue;
                break;
            case 'validator':
                const validatorName = topLevelBlock.configName;
                const validatorValue = simplifyValidator(topLevelBlock);
                result.validators[validatorName] = validatorValue;
                break;
            default:
                throw Error(`❌ Unknown block type "${topLevelBlock.type}" in: ${JSON.stringify(topLevelBlock, null, 0)}`);
        }
    }
    return result;
}

function simplifyValidator(validatorObject) {
    const result = {
        properties: {}
    };
    for ([fieldName, fieldValue] of Object.entries(validatorObject)) {
        switch (fieldName) {
            case 'type': break; // ignore as we already know it's validator
            case 'comment': result.comment = fieldValue; break;
            case 'rawSchema': break; //result.rawSchema = fieldValue; break;
            case 'name': result.name = fieldValue; break;
            case 'description': result.description = fieldValue; break;
            case 'func': result.settingName = fieldValue; break;
            default:
                throw Error(`❌ Unknown validator field "${fieldName}" in: ${JSON.stringify(validatorObject, null, 0)}`);
        }
    }
    return result;
}

function simplifyTranslation(translationObject) {
    const result = {
        properties: {}
    };
    for ([fieldName, fieldValue] of Object.entries(translationObject)) {
        switch (fieldName) {
            case 'type': break; // ignore as we already know it's translation
            case 'comment': result.comment = fieldValue; break;
            case 'rawSchema': break; result.rawSchema = fieldValue; break;
            case 'configName': result.configName = fieldValue; break;
            case 'func': result.settingName = fieldValue; break;
            default:
                throw Error(`❌ Unknown translation field "${fieldName}" in: ${JSON.stringify(translationObject, null, 0)}`);
        }
    }
    return result;
}

function simplifyMapping(mappingObject) {
    const result = {
        properties: {}
    };

    for ([fieldName, fieldValue] of Object.entries(mappingObject)) {
        switch (fieldName) {
            case 'type': break; // ignore as we already know it's mapping
            case 'comment': result.comment = fieldValue; break;
            case 'rawSchema': break; //result.rawSchema = fieldValue; break;
            case 'configName': result.configName = fieldValue; break;
            case 'settingName': result.settingName = fieldValue; break;
            case 'properties': 
                for (const property of fieldValue) {
                    //console.log(`ℹ️  Looking at property in: ${JSON.stringify(property, null, 0)}`);
                    const simpleProperty = simplifyProperty(property);
                    switch (simpleProperty.type) {
                        case "flag": result.properties[simpleProperty.name] = true; break;
                        case "key-value": result.properties[simpleProperty.name] = simpleProperty.value; break;
                        case "array": result.properties[simpleProperty.name] = simpleProperty.value; break;
                        default:
                            throw Error(`❌ Unknown type of property: ${JSON.stringify(simpleProperty, null, 0)}`);
                    }
                }
                break;
            default:
                throw Error(`❌ Unknown mapping field "${fieldName}" in: ${JSON.stringify(mappingObject, null, 0)}`);
        }
    }
    return result;
}

function simplifyProperty(propertyObject) {
    var outputPropertyName = null;
    var propertyValue = null;
    switch (propertyObject.type) {
        // atom means it is a flag - e.g. "hidden"
        case 'atom':
            return {
                type: "flag",
                name: propertyObject.value
            };
        case 'text':
            return {
                type: "key-value",
                name: propertyObject.value
            };
        case 'tuple':
            if (propertyObject.value && propertyObject.value.length === 2 && propertyObject.value[0].type === 'atom') {
                switch (propertyObject.value[0].value) {
                    case 'default': 
                        return {
                            type: "key-value",
                            name: propertyObject.value[0].value,
                            value: propertyObject.value[1].value
                        };
                    case 'datatype': 
                        return {
                            type: "key-value",
                            name: propertyObject.value[0].value,
                            value: simplifyPropertyDataType(propertyObject.value[1])
                        };
                    case 'new_conf_value':
                    case 'level':
                    case 'include_default':
                    case 'commented':
                        return {
                            type: "key-value",
                            name: propertyObject.value[0].value,
                            value: propertyObject.value[1].value
                        };
                    case 'validators':
                        return {
                            type: "array",
                            name: propertyObject.value[0].value,
                            value: simplifyPropertyDataType(propertyObject.value[1])
                        };
                    default:
                        throw Error(`❌ Unknown property name ${propertyObject.value[0].value} for: ${JSON.stringify(propertyObject, null, 0)}`);
                }
            }
            throw Error(`❌ Unknown property tuple format for: ${JSON.stringify(propertyObject, null, 0)}`);
            break;
        default:
            throw Error(`❌ Unknown property type "${propertyObject.type}" in: ${JSON.stringify(propertyObject, null, 0)}`);

    }
}

function simplifyPropertyDataType(propertyObject) {
    switch (propertyObject.type) {
        case 'text':
            // keep the same structure
            return propertyObject;
        case 'atom':
            return propertyObject.value;
        case 'tuple':
            if (propertyObject.value && propertyObject.value.length === 2 && propertyObject.value[0].type === 'atom') {
                switch (propertyObject.value[0].value) {
                    case 'duration':
                        return { "type": propertyObject.value[0].value, "unit": propertyObject.value[1].value }
                    case 'enum':
                        return { "type": propertyObject.value[0].value, "possibleValues": simplifyPropertyDataType(propertyObject.value[1]) }
                    case 'integer':
                    case 'atom':
                        return { "type": propertyObject.value[0].value, "value": propertyObject.value[1] };
                    case 'percent':
                        return { "type": propertyObject.value[0].value, "unit": propertyObject.value[1] };
                    default:
                        throw Error(`❌ Unknown property datatype atom tuple type in: ${JSON.stringify(propertyObject, null, 0)}`);    
                }
            } else if (propertyObject.value && propertyObject.value.length === 3 && propertyObject.value[0].value === 'flag') {
                return { 
                    "type": propertyObject.value[0].value, 
                    "falseValue": propertyObject.value[1].value,
                    "trueValue": propertyObject.value[2].value
                 };
            } else {
                throw Error(`❌ Unknown property datatype tuple in: ${JSON.stringify(propertyObject, null, 0)}`);    
            }
        case 'array':
            const arrayContents = [];
            for (arrayItem of propertyObject.value) {
                arrayContents.push(simplifyPropertyDataType(arrayItem));
            }
            return arrayContents;
        default:
            throw Error(`❌ Unknown property datatype in: ${JSON.stringify(propertyObject, null, 0)}`);    
    }
}

module.exports = {simplifySchemaJSON};