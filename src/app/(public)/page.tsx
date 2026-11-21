import { AgencyHome } from "@/components/agency-home";
import { publicData } from "@/lib/public-data";
export default async function Home() {
  const { portfolio, services } = await publicData();
  return <AgencyHome portfolio={portfolio} services={services} />;
}
