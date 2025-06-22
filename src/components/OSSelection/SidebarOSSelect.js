import * as Select from '@radix-ui/react-select';
import { Check, ChevronDown, ChevronUp } from 'lucide-react';
import osOptionsUnsorted from '@site/src/metadata/os/os.json';
import { useOSSelection } from '@site/src/components/OSSelection/OSSelectionContext';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function SidebarOSSelect() {
  const { selected, setSelected } = useOSSelection();
  const osOptions = osOptionsUnsorted.sort((a, b) => a.displayName.localeCompare(b.displayName));

  const handleChange = (e) => {
    const chosen = osOptions.find(opt => opt.displayName === e.target.value);
    setSelected(chosen);
  };

  return (
    <Select.Root
      value={selected.displayName}
      onValueChange={(value) => {
        const chosen = osOptions.find(opt => opt.displayName === value);
        if (chosen) setSelected(chosen);
      }}
      >
    <div className="p-3">
        <Select.Trigger
          className="flex w-full items-center justify-between rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm shadow-sm transition hover:border-gray-400 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary"
          style={{margin:'1em', width:'calc(100% - 2em)'}}
        >
          <div className="flex items-center gap-2">
            <img src={useBaseUrl(selected.smallLogo)} style={{height: "1.2em"}} alt={selected.displayName} className="w-5 h-5" />
            <span style={{paddingLeft:'0.3em'}}>{selected.displayName}</span>
          </div>
          <Select.Icon>
            <ChevronDown className="w-4 h-4 text-gray-500" />
          </Select.Icon>
        </Select.Trigger>
      
      

        <Select.Portal>
          <Select.Content
            className="z-50 w-[var(--radix-select-trigger-width)] overflow-hidden rounded-lg border border-gray-200 bg-white shadow-lg animate-in fade-in slide-in-from-top-1"
            position="popper"
            style={{background:'buttonface'}}
          >
            <Select.ScrollUpButton className="flex items-center justify-center py-1 bg-white text-gray-500">
              <ChevronUp className="w-4 h-4" />
            </Select.ScrollUpButton>


            <Select.Viewport className="p-1">
              {osOptions.map((opt) => (
                <Select.Item
                  key={opt.displayName}
                  value={opt.displayName}
                  className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-gray-800 cursor-pointer transition-colors hover:bg-gray-100 focus:bg-gray-100"
                  style={{display: 'grid', rowGap: '0.5rem', paddingLeft:'0.5em'}}
                >
                  <div style={{display: 'grid', gridTemplateColumns: '2em 1fr 2em', alignItems: 'center', }}>
                  <img src={useBaseUrl(opt.smallLogo)} style={{height:'1.2em', width:'1.2em'}} alt={opt.displayName} className="w-5 h-5" />
                  <Select.ItemText>{opt.displayName}</Select.ItemText>
                  <Select.ItemIndicator>
                    <Check className="w-4 h-4 text-primary" />
                  </Select.ItemIndicator>
                  </div>
                </Select.Item>
              ))}
            </Select.Viewport>

            <Select.ScrollDownButton className="flex items-center justify-center py-1 bg-white text-gray-500">
              <ChevronDown className="w-4 h-4" />
            </Select.ScrollDownButton>
          </Select.Content>
        </Select.Portal>
      </div>
    </Select.Root>
  );  
}
