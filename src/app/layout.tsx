import { headers } from "next/headers";
import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: {
    default: "HEXA PLUS | Digital solutions & marketing",
    template: "%s | HEXA PLUS",
  },
  description:
    "Technology, creativity and strategy. Digital solutions and marketing services from Minya, Egypt.",
  robots: { index: true, follow: true },
  icons: { icon: "/hexa-plus-original.jpg" },
};
export default async function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const ar = (await headers()).get("x-site-locale") === "ar";
  return (
    <html
      lang={ar ? "ar" : "en"}
      dir={ar ? "rtl" : "ltr"}
      suppressHydrationWarning
    >
      <body>{children}</body>
    </html>
  );
}
