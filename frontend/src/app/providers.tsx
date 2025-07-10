"use withGlobalStyles";

import { MantineProvider } from "@mantine/core";
import { ReactNode } from "react";

export function Providers({ children }: { children: ReactNode }) {
  return <MantineProvider>{children}</MantineProvider>;
}
