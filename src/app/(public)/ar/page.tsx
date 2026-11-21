import { AgencyHome } from "@/components/agency-home";
import { publicData } from "@/lib/public-data-ar";
export default async function Home() {
  const { portfolio, services } = await publicData();
  return <AgencyHome ar portfolio={portfolio} services={services} />;
}
