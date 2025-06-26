import * as React from "react";
import * as Popover from '@radix-ui/react-popover';
import { CheckIcon, CaretDownIcon, CaretUpIcon, Cross2Icon } from '@radix-ui/react-icons';
import { useLocation } from '@docusaurus/router';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import VersionLink from './VersionLink';
import useBaseUrl from '@docusaurus/useBaseUrl';
import semver from 'semver';
import { useColorMode } from '@docusaurus/theme-common';

export default function VersionPicker() {
  const { siteConfig } = useDocusaurusContext();
  const location = useLocation();
  const locationMatch = location.pathname?.match(/^\/docs\/([^\/]+)(\/(([0-9]+\.[0-9]+\.[0-9]+)\/?)?.*)?$/s);
  const project = locationMatch?.[1] ?? '';
  var activeVersion = locationMatch?.[4] ?? '';
  const { colorMode } = useColorMode(); // returns 'light' or 'dark'
  const isDarkTheme = colorMode === 'dark';

  if (!project) {
    throw new Error("No project could be found from the current location.");
  }
  //console.log(siteConfig.customFields);

  if (!siteConfig.customFields?.versionPicker) {
    throw new Error("'customFields.versionPicker' is missing.");
  }

  if (!activeVersion) {
    console.log(`Using fallback version for project "${project}".`)
    activeVersion = siteConfig.customFields.versionPicker?.["fallbackVersion"] ?? '';
  }

  if (!activeVersion) {
    throw new Error("No version could be found from the current location or from 'customFields.versionPicker.fallbackVersion'.");
  }

  const projectVersions = siteConfig.customFields.versionPicker.versions?.[project] ?? [];
  if (projectVersions.length === 0) {
    throw new Error(`No versions could be found for project ${project} under 'customFields.versionPicker.versions'.`);
  }
  console.log(`Rendering versions for project "${project}" with active version of "${activeVersion}".`)

  const activeSubProject = projectVersions.find(value => value.versions.includes(activeVersion));
  
  const activeSubProjectLogoUrl = activeSubProject?useBaseUrl(isDarkTheme?activeSubProject.logoDark:activeSubProject.logoLight):null;
  const activeSubProjectName = activeSubProject?.name ?? '';

  const subProjects = [];

  projectVersions.map((subProject, subProjectIndex) => {
    const name = subProject.name ?? '';
    const logo = subProject.logoLight || subProject.logoDark || null;
    const logoUrl = logo ? useBaseUrl(isDarkTheme?subProject.logoDark:subProject.logoLight) : null;
    const currentVersion = subProject.current ?? '';
    const ltsVersions = subProject.ltsVersions ?? [];
    // sort descending, so rcompare instead of compare
    const displayVersions = subProject.versions.sort(semver.rcompare);

    const groupedDisplayVersions = {};

    for (const displayVersion of displayVersions) {
      const parsed = semver.parse(displayVersion);
      if (!parsed) continue;

      const key = `${parsed.major}.${parsed.minor}`;
      if (!groupedDisplayVersions[key]) {
        groupedDisplayVersions[key] = [];
      }
      groupedDisplayVersions[key].push(displayVersion);
    }

    const versionGroupOutput = [];
    for (const key of Object.keys(groupedDisplayVersions).sort((a, b) => semver.rcompare(`${a}.0`, `${b}.0`))) {
      const versionsOutput = [];
      const isLTS = ltsVersions.includes(key);
      if (isLTS) {
        versionsOutput.push(
          <div className='versionPicker versionPicker-version versionPicker-lts' style={{ display: 'inline-block' }}>LTS</div>
        );
      }
      //console.log(groupedDisplayVersions[key]);

      groupedDisplayVersions[key].map((toVersion, versionIndex) => {
        const isActive = activeVersion === toVersion.toString();
        const classNames = `versionPicker versionPicker-version ${isActive?' versionPicker-activeVersion':''}`;
        const versionLink = <VersionLink className={classNames} key={'toVersion-' + versionIndex} pluginId={project} toVersion={toVersion.toString()} isCurrent={toVersion.toString()===currentVersion} />;
        if (versionLink) {
          versionsOutput.push(versionLink);
        }
      });
      //console.log("versionsOutput");
      //console.log(versionsOutput);

      if ((isLTS && versionsOutput.length > 1) || (!isLTS && versionsOutput.length > 0)) {
        versionGroupOutput.push(
          <div key={'versionFamily-' + key} className="versionPicker versionPicker-versionFamily">
            {versionsOutput}
          </div>
        )
      }
    }
    if (versionGroupOutput.length > 0) {
      const subProjectOutput = (
        <div key={'subProject-' + subProjectIndex} className="versionPicker versionPicker-subProject">
          <div key={'title-' + subProjectIndex} className="versionPicker versionPicker-subProject-Title" style={{ display: 'flex', alignItems: 'center' }}>
            {logoUrl && <img key={'logo-' + subProjectIndex} className="versionPicker versionPicker-subProject-Logo" src={logoUrl} alt={name} style={{ height: '2.5em' }} />}
            {name && <span key={'name-' + subProjectIndex} className="versionPicker versionPicker-subProject-Name" style={{ fontSize: '2em' }}>{name}</span>}
          </div>
          {versionGroupOutput}
        </div>
      );

      subProjects.push(subProjectOutput);
    }
  });
  //return <>{subProjects}</>

  return (
    <Popover.Root>
      <Popover.Trigger asChild className="versionPicker versionPicker-trigger">
        <div className="versionPicker versionPicker-triggerContent">
          <img src={useBaseUrl(activeSubProjectLogoUrl)} style={{height: "1.5em"}} alt={activeSubProjectName} />
          <span style={{paddingLeft:'0.3em'}}>{activeSubProjectName}</span>
          <span className="push-right">
            <span style={{paddingRight:'0.3em'}}>{activeVersion}</span>
            <CaretDownIcon className="push-right" />
          </span>
        </div>
      </Popover.Trigger>
      <Popover.Portal className="versionPicker versionPicker-optionsPortal">
        <Popover.Content className="versionPicker versionPicker-optionsContent w-[var(--radix-popover-trigger-width)]" sideOffset={0}>
          {subProjects}
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
