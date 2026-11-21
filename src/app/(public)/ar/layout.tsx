import type { Metadata } from "next";
export const metadata: Metadata = {
  title: {
    default: "هيكسا بلس | الحلول الرقمية والتسويق",
    template: "%s | هيكسا بلس",
  },
  description:
    "هيكسا بلس للحلول الرقمية والتسويق. تطوير المواقع والتطبيقات وأنظمة الأعمال والهوية البصرية من المنيا، مصر.",
  openGraph: { locale: "ar_EG" },
};
export default function ArabicLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
