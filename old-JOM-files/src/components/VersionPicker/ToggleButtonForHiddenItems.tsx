import { useState } from "react";
import { ChevronRightIcon } from "@radix-ui/react-icons";

export default function ToggleButtonForHiddenItems({selectorClass, hiddenClassName, unhiddenClassname }) {
  const [hideItems, setHideItems] = useState(true);

  function toggleHidden() {
    const newHideItems = !hideItems;
    if (newHideItems) {
      // hide items with unhiddenClassname and show button
      if (unhiddenClassname) {
        document.querySelectorAll(`.${selectorClass}.${unhiddenClassname}`)
          .forEach((el) => {
            el.classList.remove(unhiddenClassname);
            if (hiddenClassName) el.classList.add(hiddenClassName);
          });
      }
    } else {
      // show items with hiddenClassname and hide button
      if (hiddenClassName) {
        document.querySelectorAll(`.${selectorClass}.${hiddenClassName}`)
          .forEach((el) => {
            el.classList.remove(hiddenClassName);
            if (unhiddenClassname) el.classList.add(unhiddenClassname);
          });
      }
    }
    setHideItems(newHideItems);
  }

  if (!hideItems) return null;

  return (
    <button className="toggleButtonForHiddenItems" onClick={() => toggleHidden()}><ChevronRightIcon /></button>
  );
}


