import React from 'react';
import {
  useAllDocsData,
  useActiveVersion,
  useActiveDocContext,
} from '@docusaurus/plugin-content-docs/client';
import Link from '@docusaurus/Link';

interface VersionLinkProps {
  pluginId?: string;
  toVersion: string;
  isCurrent?: boolean;
  className?: string;
}

const VersionLink: React.FC<VersionLinkProps> = ({
  pluginId,
  toVersion,
  isCurrent = false,
  className = ''
}) => {
  const allDocsData = useAllDocsData();
  const activeVersion = useActiveVersion(pluginId);
  const activeDocContext = useActiveDocContext(pluginId);

  //console.log(isCurrent);

  if (!activeVersion || !activeDocContext) return null;

  const currentDocId = activeDocContext.activeDoc?.id;
  if (!currentDocId) return null;

  const pluginData = allDocsData[pluginId];
  if (!pluginData) return null;
  //console.log("[VersionLink] D");
  const searchVersion = isCurrent?'current':(toVersion);
  const targetVersion = pluginData.versions.find((v) => v.name === searchVersion);
  //console.log("[VersionLink] Target Version: " + targetVersion );
  //console.log(targetVersion);
  if (!targetVersion) return null;
  //console.log("[VersionLink] E");

  var targetDoc = targetVersion.docs.find((d) => d.id === currentDocId);
  if (!targetDoc) {
    // fall back to root doc
     targetDoc = targetVersion.docs.find((d) => d.id === targetVersion.mainDocId)
  }
  var targetDocLink = null;
  if (targetDoc) {
    targetDocLink = targetDoc.path;
  } else {
    targetDocLink = targetVersion.path
  }
  //console.log("[VersionLink] F");

  //console.log(targetDoc);

  return (
    <div className={className}>
      <Link to={targetDocLink}>{toVersion}</Link>
    </div>
  )
};

export default VersionLink;
