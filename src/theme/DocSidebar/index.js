import React from 'react';
import OriginalDocSidebar from '@theme-original/DocSidebar';
import SidebarOSSelect from '@site/src/components/OSSelection/SidebarOSSelect';
import VersionPicker from '@site/src/components/VersionPicker/VersionPicker';

export default function DocSidebarWrapper(props) {
  return (
    <>
      <SidebarOSSelect />
      <VersionPicker />
      <OriginalDocSidebar {...props} />
    </>
  );
}
