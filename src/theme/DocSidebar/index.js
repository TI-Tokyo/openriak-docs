import React from 'react';
import DocSidebar from '@theme-original/DocSidebar';
import SidebarOSDropdown from '@site/src/components/OSSelection/SidebarOSDropdown';
import SidebarOSSelect from '@site/src/components/OSSelection/SidebarOSSelect';

export default function DocSidebarWrapper(props) {

  return (
    <>
      <SidebarOSSelect />
      <DocSidebar {...props} />
    </>
  );
}
