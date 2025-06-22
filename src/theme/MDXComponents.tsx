import React from "react";
import OriginalMDXComponents from '@theme-original/MDXComponents';
import InlineCodeWithCopy from "@site/src/components/InlineCodeWithCopy/InlineCodeWithCopy";

export default {
  ...OriginalMDXComponents,

  inlineCode: (props) => {
    const { className, children } = props;
    /*
    if (className) {
      return <code {...props} />;
    }
    if (typeof children === 'string' && children.length <= 2) {
      return <code>{children}</code>;
    } 
    */   
    return <InlineCodeWithCopy>{children}</InlineCodeWithCopy>;
  },
};
