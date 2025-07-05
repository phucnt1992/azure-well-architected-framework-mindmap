"use client";


import { createContext, useContext, useState, useMemo } from "react";

export const THEME = {
  LIGHT: "light",
  DARK: "dark",
}

const Context = createContext<[string, (theme: string) => void]>([THEME.LIGHT, () => {
  console.warn("No theme provider found");
}]);

export function ThemeProvider({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [theme, setTheme] = useState(THEME.LIGHT);
  const value = useMemo(() => [theme, setTheme] as [string, (theme: string) => void], [theme, setTheme]);
  return (
    <Context.Provider value={value}>{children}</Context.Provider>
  );
}

export const useThemeContext = () => {
  return useContext(Context);
}
