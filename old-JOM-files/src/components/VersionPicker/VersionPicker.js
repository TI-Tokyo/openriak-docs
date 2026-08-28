import * as React from "react";
import * as Popover from '@radix-ui/react-popover';
import { CheckIcon, CaretDownIcon, CaretUpIcon, Cross2Icon, ButtonIcon } from '@radix-ui/react-icons';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import VersionLink from './VersionLink';
import useBaseUrl from '@docusaurus/useBaseUrl';
import semver from 'semver';
import { useColorMode } from '@docusaurus/theme-common';
import ToggleButtonForHiddenItems from './ToggleButtonForHiddenItems';

export default function VersionPicker() {
  const { siteConfig } = useDocusaurusContext();
  const location = useLocation();
  const locationMatch = location.pathname?.match(/^\/docs\/([^\/]+)(\/(([0-9]+\.[0-9]+\.[0-9]+)\/?)?.*)?$/s);
  const pageProject = locationMatch?.[1] ?? '';
  var pageVersion = locationMatch?.[4] ?? '';
  const { colorMode } = useColorMode(); // returns 'light' or 'dark'
  const isDarkTheme = colorMode === 'dark';

  if (!pageProject) {
    throw new Error("No project could be found from the current location.");
  }
  //console.log(siteConfig.customFields);

  if (!siteConfig.customFields) throw new Error("'customFields' is missing.");
  if (!siteConfig.customFields.versionPicker) throw new Error("'customFields.versionPicker' is missing.");
  if (!siteConfig.customFields.versionPicker[pageProject]) throw new Error(`'customFields.versionPicker.${pageProject}' is missing.`);

  const pageProjectConfig = siteConfig.customFields.versionPicker[pageProject];

  const projectCurrentVersion = pageProjectConfig["current"];
  if (!pageVersion) pageVersion = projectCurrentVersion ?? '';
  if (!pageVersion) throw new Error("No version could be found from the current location or from 'customFields.versionPicker.current'.");

  const projectBrands = pageProjectConfig.brands ?? [];
  if (projectBrands.length === 0) {
    console.log(`No brands could be found for project ${pageProject} under 'customFields.versionPicker.${pageProject}.brands'.`);
  }

  const pageBrand = projectBrands.find(brand => {
    return brand.groups.find(group => group.versions.includes(pageVersion));
  });
  //console.log("Active Brand:");
  //console.log(pageBrand);
  
  const pageBrandLogoUrl = pageBrand?useBaseUrl(isDarkTheme?pageBrand.logoDark:pageBrand.logoLight):null;
  const pageBrandName = pageBrand?.name ?? '';

  const brandsOutput = [];
  // loop over brands, e.g. OpenRiak and RiakKV
  projectBrands.map((brand, brandIndex) => {
    const brandName = brand.name ?? '';
    const brandLogo = (isDarkTheme?brand.logoDark:brand.logoLight) || null;
    const brandLogoUrl = brandLogo ? useBaseUrl(brandLogo) : null;

    const brandGroupOutput = [];
    
    //console.log(brand.groups);
    
    // loop over the brand's groups e.g. 3.0 and 3.2
    brand.groups.map((brandGroup, brandGroupIndex) => {
      // get the brand metadata ready for later
      const displayName = brandGroup.displayName || '';
      const isLTS = brandGroup.lts || false;
      const groupVersions = brandGroup.versions.sort(semver.rcompare);
      if (groupVersions.length === 0) throw new Error(`Brand has no group!`)
      const collapseBelow = brandGroup.collapseBelow || groupVersions[groupVersions.length-1];

      // split the versions into shown and collaspsed
      const groupVersionsOutput = [];
      // we need to show the collapsed versions when the current page is one
      var useCollapsedSection = true;
      var hasCollapsedItems = false;
      //console.log(groupVersions);
      if (groupVersions.includes(pageVersion)) {
        // pageVersion is in this group
        if (semver.lt(pageVersion, collapseBelow)) {
          // pageVersion is in this group and should be hidden as in the collapsed versions
          // therefore - don't collapse them!
          useCollapsedSection = false;
        }
      }

      const selectorClass = `versionPicker-brand-${brandIndex}-group-${brandGroupIndex}`;
      const hiddenClass = "versionPicker-version-hidden";
      // loop over the group's versions e.g. 3.0.1 and 3.0.2
      groupVersions.map((groupVersion, groupVersionIndex) => {
        const isPageVersion = (pageVersion === groupVersion.toString());
        var classNames = 'versionPicker versionPicker-version';
        classNames += ' ' + selectorClass;
        // tag is the active version
        if (isPageVersion) classNames += ' versionPicker-activeVersion';
        // tag if we are NOT showing collased versions AND this version is below the collapse point
        const isCollapsed = useCollapsedSection && semver.lt(groupVersion, collapseBelow);
        if (isCollapsed) {
          classNames += ' ' + hiddenClass;
          hasCollapsedItems = true;
        }
        
        const versionLink = <VersionLink 
          className={classNames} 
          key={`brand-${brandIndex}-group-${brandGroupIndex}-version-${groupVersionIndex}`} 
          pluginId={pageProject} 
          toVersion={groupVersion.toString()} 
          isCurrent={projectCurrentVersion === groupVersion.toString()} 
        />;
        groupVersionsOutput.push(versionLink);
      });
      //console.log(groupVersionsOutput);

      // is there a collapsed section?
      if (hasCollapsedItems) {
        // we need a button to make other visisble
        groupVersionsOutput.push(<ToggleButtonForHiddenItems selectorClass={selectorClass} hiddenClassName={hiddenClass} />);
        //shownVersionsOutput.push([...collapsedVersionsOutput]);
      }
      //console.log(groupVersionsOutput);

      // do we have a header?
      const label = <>
        {displayName && <span key={'brandGroup-name-' + brandGroupIndex}className="versionPicker versionPicker-brandGroup-displayName">{displayName}</span>}
        {isLTS && <span key={'brandGroup-lts-' + brandGroupIndex} title="Long Term Support" className="versionPicker versionPicker-brandGroup-lts">LTS</span>}
        </>;
      const versionClassNames = "versionPicker versionPicker-versions" + ((!displayName && !isLTS)?" versionPicker-versions-nolabel":"");
      brandGroupOutput.push(
        <div key={'brandGroup-' + brandGroupIndex} className="versionPicker versionPicker-brandGroup">
          {(displayName || isLTS) && <div key={'brandGroupLabel-' + brandGroupIndex} className='versionPicker versionPicker-label'>{label}</div>}
          <div key={'brandGroupVersions-' + brandGroupIndex} className={versionClassNames}>
            {groupVersionsOutput}
          </div>
        </div>
      );
    });

    if (brandGroupOutput.length > 0) {
      const brandOutput = (
        <div key={'brand-' + brandIndex} className="versionPicker versionPicker-brand">
          <div key={'title-' + brandIndex} className="versionPicker versionPicker-brand-Title">
            {brandLogoUrl && <img key={'logo-' + brandIndex} className="versionPicker versionPicker-brand-Logo" src={brandLogoUrl} alt={brandName} />}
            {brandName && <span key={'name-' + brandIndex} className="versionPicker versionPicker-brand-Name">{brandName}</span>}
          </div>
          {brandGroupOutput}
        </div>
      );

      brandsOutput.push(brandOutput);
    }
  });

  return (
    <Popover.Root>
      <Popover.Trigger asChild className="versionPicker versionPicker-trigger">
        <div className="versionPicker versionPicker-triggerContent">
          <img src={useBaseUrl(pageBrandLogoUrl)} style={{height: "1.5em"}} alt={pageBrandName} />
          <span style={{paddingLeft:'0.3em'}}>{pageBrandName}</span>
          <span className="push-right">
            <span style={{paddingRight:'0.3em', fontWeight: 'bold'}}>{pageVersion}</span>
            <CaretDownIcon className="push-right" />
          </span>
        </div>
      </Popover.Trigger>
      <Popover.Portal className="versionPicker versionPicker-optionsPortal">
        <Popover.Content className="versionPicker versionPicker-optionsContent" sideOffset={0}>
          {brandsOutput}
          <Popover.Arrow className="versionPicker versionPicker-arrow" width={'1rem'} height={'0.5rem'}/>
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  );

  /*
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
          style={{margin:'1em', fontSize:'1.2em', width:'calc(100% - 2em)', 
            backgroundColor:'var(--ifm-color-primary-lightest)', 
            borderColor:'var(--ifm-color-primary-darkest)', 
            borderWidth:'0', borderRadius:'0.125em'}}
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
            style={{background:'var(--ifm-color-primary-lightest)'}}
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
*/
}
