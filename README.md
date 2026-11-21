# HEXA PLUS

A Next.js App Router application for HEXA PLUS, with a public company website and a private Supabase-backed business workspace.

## Stack

Next.js 16, React, TypeScript, Tailwind CSS 4, shadcn-style accessible components built on Radix, Lucide, Framer Motion, Supabase Auth/Postgres/Storage/Realtime, React Hook Form, Zod, Recharts, Three.js and PDF-lib. The original supplied JPEG logo is preserved byte-for-byte at `public/hexa-plus-original.jpg`.

## Run locally

1. Use Node.js 22 or newer and run `npm ci`.
2. Copy `.env.example` to `.env.local` and fill the project URL and **publishable** key. The historical `NEXT_PUBLIC_SUPABASE_ANON_KEY` variable name holds the new publishable key, not a legacy JWT.
3. Set `SUPABASE_SERVER_KEY` to the new secret key only on the server. It is required for invitations and the seed script. Never prefix it `NEXT_PUBLIC_`, commit it, or put it in website settings.
4. Set `NEXT_PUBLIC_SITE_URL` to your actual origin.
5. Apply the SQL migrations in filename order with a trusted database administrator connection. Do not run the foundation twice.
6. Run `npm run seed` to insert only the 20 services requested in the company brief and initial public identity copy. It uses conflict-ignore and does not overwrite existing content. No clients, revenue, testimonials or case studies are seeded.
7. Run `npm run dev`. For production: `npm run build`, then `npm start`.

## Deployment

The current deployment uses a separate Render Free Node web service. Build: `npm ci && npm run build`. Start: `npm start`. Render supplies `PORT`. Keep all environment variables on Render, not in the repository. Set `NODE_VERSION=22` or use a supported 22.x runtime. A free web service sleeps while idle and can take over 50 seconds to wake; it is not an always-on SLA. Database/storage/auth use the separate Supabase Free project. Monitor each provider's current usage limits before storing real business records at scale.

Vercel-specific code is not required, so the app remains technically deployable there with a plan that permits the company's commercial use. The live deployment intentionally does not use Vercel Hobby or Netlify under the owner's constraints.

## Database and security

- Migrations create the 30 requested relational tables, explicit grants, foreign keys, indexes, RLS, audit triggers, six roles, departments, transactional invoice routines and notification functions.
- Public content is served only through `published_*` projection views. Private base tables are not anonymously selectable. Hidden service pricing and staff/client identifiers do not cross that boundary.
- Both Storage buckets are private. Business file access is permission-based. The portfolio publication predicate uses exact canonical object URL equality, not wildcard/suffix matching.
- `src/lib/media.ts` translates canonical portfolio references into `/api/media`. That route uses the logged-out publishable-key client so unpublished media cannot be served merely because the server is privileged. Do not replace it with unconditional service-key downloads.
- The canonical media prefix in migration 002 is pinned to the current Supabase project. For a different project, replace the project URL in that migration before the initial deployment, or ship a reviewed incremental migration. Uploads use simple UUID keys, avoiding URL-encoding ambiguity.
- Team members see assigned projects and their children, plus assigned tasks. Ordinary staff cannot assign themselves roles. Only the super admin manages account roles and permission grants.
- Invoices use integer minor units (EGP piastres). The save RPC validates and replaces lines in one transaction and computes totals server-side. Direct invoice/item edits are revoked. Paid invoices are immutable. Payment validation locks the invoice and prevents concurrent overpayment.
- Inquiry submission validates on both server and database, rejects honeypot input, and has email/global database throttles. The global ceiling can still be exhausted by an attacker; deploy a verified CAPTCHA or edge abuse control if the company attracts sustained spam.
- Private business files currently follow module-wide Files permission, not per-client/project membership. Linking a file to a task does not automatically grant file access. Grant Files access only where appropriate.

## First administrator

Create the owner's Auth user using Supabase's trusted admin interface or server-side administrative SDK, with a secure owner-chosen/generated password. Then insert a matching `profiles` row whose `id` is the Auth user's UUID, `status='active'`, and `role_id` is the `super_admin` role ID. This is deliberately not a public signup route.

The existing deployment has its owner provisioned already. Subsequent members can be invited from Team by a super admin. Invitations send to the exact email entered in the confirmation form. Ensure Supabase Auth's Site URL and redirect allowlist contain the production origin and `/auth/confirm`. Use a production SMTP provider within an approved budget before relying on bulk team invitations; Supabase's built-in mail has provider limits. Invitation delivery has not been tested by sending to a real employee.

## Website content

Services, portfolio, gallery media and approved testimonials are managed in their modules. Draft media stays private until linked to published content. Empty portfolio and testimonial sections are honest empty states, not fabricated work or quotes. The separate owner-approved portfolio import adds only supplied projects, with actual screenshots and observed descriptions; it does not invent metrics or private client data.

Website Settings supports public `hero_title`, `hero_description`, `address`, `contact_email`, `contact_phone`, approved `social_*` links and `page_about`, `page_process`, `page_industries`, `page_careers`, `page_faq`, `page_privacy`, `page_terms` body overrides. Arabic overrides use the same keys with `_ar` appended, including `hero_title_ar`, `hero_description_ar`, `address_ar` and `page_about_ar`. Services, portfolio narratives and approved testimonials have explicit Arabic fields in migration 004. The `/ar` public route tree includes all public pages and service details; language links preserve the current path and reload the document to keep HTML language/direction correct. No translation service or paid API is required. The default legacy seed headline/description fall back to the approved redesign copy; changing either CMS value applies an owner override. The shared bilingual homepage is maintained in `src/components/agency-home.tsx`; the route generator deliberately preserves it. The public design uses a dark editorial hero, local display fonts, real published project compositions and a lit beveled WebGL hex with an SVG fallback. Motion has explicit pause controls, respects reduced-motion preferences, caps rendering at about 30 FPS and pauses offscreen. The shared brand theme samples blue `#134FE9`, violet `#7852EA`, purple `#5D41D7` and navy `#020F3A` from the supplied JPEG, applying the blue-violet gradient to public CTAs, the hero illustration, capability panel and dashboard accents. The hex illustration is separate from the original unchanged logo. Arabic templates are generated from reviewed copy in `src/lib/ar-copy.tsv`; after template changes, run `node scripts/generate-ar.cjs` and inspect the generated routes. Dynamic company content must be entered in both languages. Locally hosted Space Grotesk, Manrope and Noto Sans Arabic fonts include their OFL licenses. The supplied logo is deliberately not redrawn. Privacy/terms are an operational starting draft, not legal advice; the company should review them before collecting real client data.

## Workspace

Database-backed CRM, leads and lead activity; project/task/milestone/member records; services/portfolio CMS; content calendar, campaigns and social-account records; invoice/payment/expense records; private files; roles/permission grants; notifications, audit history and website settings. Tables support server-side search, sorting and pagination. Lead/project/task boards support drag-and-drop for authorized writers. Calendar and timeline views explicitly show the current paginated result set, not an unbounded all-record plan.

Reports use actual accessible records for revenue, lead/client acquisition, project status/category distribution and manually recorded campaign performance. They do not claim automatic ad-platform ingestion or social publishing. Revenue means recorded payments, not invoice face value. Currency is EGP.

Deadline notices are checked on workspace visits and de-duplicated per Cairo calendar day. They are not scheduled email/push reminders. Realtime notification delivery depends on the project's Realtime publication and the recipient's RLS policy.

## Verification

- `npm test`: financial arithmetic and input-boundary unit tests.
- `npm run typecheck` and `npm run build`.
- `scripts/integration-test.ts`: creates clearly labeled temporary QA users/records, tests real role JWTs and negative RLS/finance/media boundaries, then retains them only for the following browser checks.
- `scripts/browser-test.mjs`: tests real database-backed create/search/detail/board/PDF flows and desktop/mobile/RTL rendering with system Chrome.
- `scripts/cleanup-test.ts`: removes the temporary QA data/users/media. Run it even after a browser-test failure.
- `scripts/realtime-test.ts`: creates two temporary authenticated sessions, waits for Postgres system readiness, confirms recipient-only WebSocket INSERT delivery and removes its fixtures.
- `scripts/public-flow-test.mjs`: real Arabic inquiry-to-lead/consent/notification flow, direct-RPC negatives, public project screenshots and draft exclusion; removes its inquiry fixture in finally.
- `scripts/arabic-test.mjs`: public Arabic routes, 20 service details, RTL, responsive overflow, validation and language switching.
- `scripts/agency-test.mjs`: actual 3D canvas pixel changes, pause/resume, reduced-motion and mobile navigation, with screenshots and a browser recording.
- `scripts/release-check.mjs`: public route and responsive checks against a built local site or `BASE_URL`, both languages, form validation, motion, reduced-motion and WebGL fallback.
- `scripts/visual-check.mjs`: captures public desktop/mobile screenshots. Inspect actual screenshots, not only console assertions.

The integration scripts target the configured database. Use a separate staging project once real company records exist. Never run destructive QA scripts blindly against a populated production database.

## Remaining release checks

This repository is a phased working build, not a claim that every long-spec acceptance criterion has received final sign-off. Complete live-site verification after each deploy, real invitation delivery with an approved recipient and company approval of the bilingual content. The two-recipient Realtime isolation test passes after explicitly waiting for the replication listener system-ready event. Review module-level file scope, legal text and abuse protection before real client onboarding. The public visitor site has a complete Arabic route tree and translated seed service content. Future company-written content needs its Arabic CMS fields filled. The private workspace is bilingual for navigation, common controls and field/status labels; some secondary explanatory/report strings still need a final Arabic pass.
