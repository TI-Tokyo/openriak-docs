import React, { useState, useEffect } from 'react';

export default function DebouncedInput({
  value,
  onChange,
  delay = 300,
  placeholder,
  style
}: {
  value: string;
  onChange: (value: string) => void;
  delay?: number;
  placeholder?: string;
  style?: any;
}) {
  const [inputValue, setInputValue] = useState(value);

  // 🔁 Sync local input value when parent value changes
  useEffect(() => {
    setInputValue(value);
  }, [value]);

  useEffect(() => {
    const handler = setTimeout(() => {
      onChange(inputValue);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [inputValue, delay, onChange]);

  return (
    <input
      value={inputValue}
      onChange={(e) => setInputValue(e.target.value)}
      placeholder={placeholder}
      style={style}
    />
  );
}
