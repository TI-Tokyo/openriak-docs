function mergeCloneTest() {
  const sources = [];
//  sources.push(JSON.parse('{"mappings": {"alpha":   {"value": "alpha-value"},   "beta":  {"value": "beta-value"}  } }'));
//  sources.push(JSON.parse('{"mappings": {"charlie": {"value": "charlie-value"}, "delta": {"value": "delta-value"} } }'));
//  sources.push(JSON.parse('{"mappings": {"alpha":   {"merge": true, "value": "alpha-2-value"}, "delta": {"value": "delta-2-value"} } }'));
//  sources.push(JSON.parse('{"mappings": {"echo": [{"echo-1": "echo-1-value"}] }}'));
//  sources.push(JSON.parse('{"mappings": {"merge": true, "echo": [{"echo-1": "echo-1-new-value"}] }}'));
  
  sources.push({"mappings" : {
    "mdc.cluster_manager": {
      "properties": {
        "default": [
          {
            "type": "text",
            "value": "{{cluster_manager_ip}}"
          },
          {
            "type": "template",
            "value": "cluster_manager_port"
          }
        ],
        "datatype": "ip"
      },
      "comment": [
        "@doc The cluster manager will listen for connections from remote",
        "clusters on this ip and port. Every node runs one cluster manager,",
        "but only the cluster manager running on the cluster_leader will",
        "service requests. This can change as nodes enter and leave the",
        "cluster. The value is a combination of an IP address (**not",
        "hostname**) followed by a port number"
      ],
      "configName": "mdc.cluster_manager",
      "settingName": "riak_core.cluster_mgr"
    },
  }});

  sources.push({"mappings": {
    "mdc.cluster_manager": {
      "properties": {
        //"merge": true,
        "datatype": "susan"
      },
    },
  }});


  var toObject = {};
  for (const fromObject of sources) {
    console.log('ℹ️  New top level object');
    toObject = mergeClone(2, fromObject, toObject, false);
  }

  console.log(JSON.stringify(toObject, null, 2));
}

function mergeClone(level, fromObject, toObject, allowMerge) {
  //console.log(" ".repeat(level) + 'ℹ️  mergeClone');
  if (Array.isArray(fromObject)) {
    //console.log(" ".repeat(level) + `ℹ️  -> Found array in fromObject`);

    // array, so do merge on each item instead
    return mergeCloneArray(level, fromObject, toObject, allowMerge);
  } else {
    //console.log(" ".repeat(level) + `ℹ️  -> Found object in fromObject`);
    switch (typeof fromObject) {
      // value types, so return actual value
      case 'boolean':
      case 'string':
      case 'integer':
        //console.log(" ".repeat(level) + `ℹ️  -> Found value object in fromObject`);
        if (allowMerge && toObject) {
          // if merging, then use updated value in fromObject
          return fromObject;
        } else if (toObject) {
          // if not merging, then return current value in toObject
          return toObject;
        } else {
          // if no value in toObject, then use new value in  fromObject
          return fromObject;
        }
      case 'object':
        // merge froObject into toObject
        return mergeCloneObject(level, fromObject, toObject, allowMerge);
      default:
        console.error(`❌ Unknown typeof fromObject: ${typeof fromObject}`);
        process.exit(1);
    }
  }
}

function mergeCloneArray(level, fromObject, toObject, allowMerge) {
  //console.log(" ".repeat(level) + 'ℹ️  mergeCloneArray');
  if (toObject === null ) {
    return fromObject;
    const results = [];
    for (item in fromObject) {
      results.push(item);
    }
    return results;
  } else {
    // array's don't merge - they override
    if (allowMerge) {
      return fromObject;
    } else {
      return toObject;
    }
  }
}

function mergeCloneObject(level, fromObject, toObject = null, allowMerge = false) {
  //console.log(" ".repeat(level) + 'ℹ️  mergeCloneObject');
  if (!toObject) {
    return fromObject;
  }
  for (const [fromName, fromValue] of Object.entries(fromObject)) {
    // don't process merge - it's a flag as to whether to merge THIS item, not all subsequent items
    if (fromName === 'merge') { continue; }
    if (toObject[fromName]) {
      // handle potential merge 
      switch (fromName) {
        case 'merge': 
          // don't merge in the merge value - it's a flag as to whether to merge THIS item, not all subsequent items
          //console.log(" ".repeat(level) + `ℹ️  -> Found "${fromName}" so skipping this entry.`);
          break;
        case 'mappings':
        case 'translations':
        case 'validators':
          //console.log(" ".repeat(level) + `ℹ️  -> Found "${fromName}" so merging regardless`);
          toObject[fromName] = mergeClone(level+2, fromValue, toObject[fromName], (allowMerge || fromValue.merge || false));
          break;
        default:
          //console.log(" ".repeat(level) + `ℹ️  -> Found "${fromName}" so checking on merge. Alreadying merging: "${allowMerge}". Start merging: "${fromValue.merge || false}"`);
          toObject[fromName] = mergeClone(level+2, fromValue, toObject[fromName], (allowMerge || fromValue.merge || false));
          if (allowMerge || fromValue.merge || Array.isArray(fromValue)) {
            // merge objects
//            toObject[fromName] = mergeClone(level+2, fromValue, toObject[fromName], (allowMerge || fromValue.merge || false));
          } else {
            // do not merge, so do nothing as toObject already has the right value
            //toObject[fromName] = fromValue;
          }
      }
    } else {
      toObject[fromName] = fromValue;
    }
  }
  return toObject;
}

module.exports = { mergeCloneTest, mergeClone }