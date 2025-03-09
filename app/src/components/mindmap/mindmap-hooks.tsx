'use client';

import { Markmap } from 'markmap-view';
import { Toolbar } from 'markmap-toolbar';
import React, { useEffect, useRef, useState } from 'react';

import { transformer } from './markmap';

const initValue = `# markmap
- beautiful
- useful
- easy
- interactive
`;

const renderToolbar = (map: Markmap, wrapper: HTMLElement | null) => {
  while (wrapper?.firstChild) wrapper.firstChild.remove();

  if (!!map && !!wrapper) {
    const toolbar = new Toolbar();

    toolbar.attach(map);
    // Register custom buttons
    toolbar.register({
      id: 'alert',
      title: 'Click to show an alert',
      content: 'Alert',
      onClick: () => alert('You made it!'),
    });
    toolbar.setItems([...Toolbar.defaultItems, 'alert']);
    wrapper.append(toolbar.render());
  }
}

export const MindmapHooks = () => {
  const [value, setValue] = useState(initValue);
  // Ref for SVG element
  const refSvg = useRef<SVGSVGElement>(null);
  // Ref for markmap object
  const refMap = useRef<Markmap>(null);
  // Ref for toolbar wrapper
  const refToolbar = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // If refMap is already set, skip
    if (refMap.current) return;

    // Create markmap and save to refMm
    const map = Markmap.create(refSvg.current);

    refMap.current = map;

    renderToolbar(
      refMap.current,
      refToolbar.current
    );
  }, [refSvg.current]);

  useEffect(() => {
    // Update data for markmap once value is changed
    const map = refMap.current;
    if (!map) return;

    const { root } = transformer.transform(value);
    map.setData(root)
      .then(() => {
        map.fit();
      });

  }, [refMap.current, value]);

  const handleChange = (e: { target: { value: React.SetStateAction<string>; }; }) => {
    setValue(e.target.value);
  };

  return (
    <>
      <div data-testid="mindmap" className="flex-1">
        <textarea
          className="w-full h-full border border-gray-400"
          value={value}
          onChange={handleChange}
        />
      </div>
      <svg data-testid="mindmap-svg" className="flex-1" ref={refSvg} />
      <div data-testid="mindmap-toolbar" ref={refToolbar}></div>
    </>
  );
}
