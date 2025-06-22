import React, {type ReactNode} from 'react';
import Layout from '@theme-original/Layout';
import type LayoutType from '@theme/Layout';
import type {WrapperProps} from '@docusaurus/types';
import { OSSelectionProvider } from '@site/src/components/OSSelection/OSSelectionContext';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): ReactNode {
  return (
    <OSSelectionProvider>
      <Layout {...props} />
    </OSSelectionProvider>
  );
}
