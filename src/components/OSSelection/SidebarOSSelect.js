import * as Select from '@radix-ui/react-select';
import { CheckIcon, CaretDownIcon, CaretUpIcon } from '@radix-ui/react-icons';
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
    <div>
        <Select.Trigger className="osPicker osPicker-trigger">
          <div className="osPicker osPicker-triggerContent">
            <img src={useBaseUrl(selected.smallLogo)} style={{height: "1.2em"}} alt={selected.displayName} />
            <span style={{paddingLeft:'0.3em'}}>{selected.displayName}</span>
          </div>
          <Select.Icon className="push-right">
            <CaretDownIcon />
          </Select.Icon>
        </Select.Trigger>

        <Select.Portal className="osPicker osPicker-portal">
          <Select.Content
            className="osPicker osPicker-content w-[var(--radix-select-trigger-width)]"
            position="popper"
          >
            <Select.ScrollUpButton>
              <CaretUpIcon />
            </Select.ScrollUpButton>

            <Select.Viewport className="osPicker osPicker-viewport" >
              {osOptions.map((opt) => (
                <Select.Item className="osPicker osPicker-item"
                  key={opt.displayName}
                  value={opt.displayName}
                >
                  <div style={{display: 'grid', gridTemplateColumns: '2em 1fr 2em', alignItems: 'center', }}>
                  <img src={useBaseUrl(opt.smallLogo)} style={{height:'1.2em', width:'1.2em'}} alt={opt.displayName} />
                  <Select.ItemText>{opt.displayName}</Select.ItemText>
                  <Select.ItemIndicator>
                    <CheckIcon />
                  </Select.ItemIndicator>
                  </div>
                </Select.Item>
              ))}
            </Select.Viewport>

            <Select.ScrollDownButton>
              <CaretDownIcon  />
            </Select.ScrollDownButton>
            <Select.Arrow className="osPicker osPicker-arrow" width={20} height={10} />
  
          </Select.Content>
        </Select.Portal>
      </div>
    </Select.Root>
  );  
}
