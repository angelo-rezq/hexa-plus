import Link from "next/link";
import {
  ArrowUpRight,
  ArrowDown,
  Code2,
  Component,
  ChartNoAxesCombined,
  Check,
  MoveUpRight,
} from "lucide-react";
import { publicData } from "@/lib/public-data-ar";
import { Reveal } from "@/components/reveal";
import { ProjectGallery } from "@/components/project-gallery-ar";
export default async function Home() {
  const { services, portfolio, testimonials, settings } = await publicData();
  return (
    <main id="main">
      <section className="hero section-wrap">
        <div className="hero-copy">
          <Reveal>
            <div className="location-label">
              <span /> المنيا، مصر · أفكار تتجاوز الحدود{" "}
            </div>
            <h1>
              {settings.hero_title ? (
                <>
                  {settings.hero_title.split("\n").map((line, i, lines) => (
                    <span
                      key={i}
                      style={{
                        display: "block",
                        color: i === lines.length - 1 ? "#8ca3ff" : "inherit",
                      }}
                    >
                      {line}
                    </span>
                  ))}
                </>
              ) : (
                <>
                  {" "}
                  رؤيتك. <br /> خبرتنا الرقمية. <br />
                  <span> نتيجة تصنع الفارق. </span>
                </>
              )}
            </h1>
            <p>
              {settings.hero_description ||
                "نجمع بين التقنية والإبداع والاستراتيجية لبناء تجارب رقمية تدفع أعمالك إلى الأمام."}
            </p>
            <div className="hero-actions">
              <Link href="/ar/contact" className="primary-link">
                {" "}
                ابدأ مشروعك <ArrowUpRight size={19} />
              </Link>
              <Link href="/ar/portfolio" className="secondary-link">
                {" "}
                استكشف أعمالنا <ArrowUpRight size={18} />
              </Link>
            </div>
            <div className="hero-footnote">
              <span> ٠١ / نربط الفكرة بالتنفيذ </span>
              <ArrowDown size={16} />
            </div>
          </Reveal>
        </div>
        <Reveal className="hero-art" delay={0.12}>
          <div className="art-topline">
            <span> منهج هيكسا بلس </span>
            <span>+</span>
          </div>
          <div className="logo-stage">
            <div className="logo-orbit orbit-one" />
            <div className="logo-orbit orbit-two" />
            <img
              src="/hexa-plus-original.jpg"
              width="380"
              height="380"
              alt="الشعار الأصلي لهيكسا بلس للحلول الرقمية"
              fetchPriority="high"
            />
          </div>
          <div className="art-bottom">
            <span>
              {" "}
              تقنية. <br /> إبداع. <br />
              <strong> تكامل. </strong>
            </span>
            <MoveUpRight size={48} strokeWidth={1} />
          </div>
          <div className="art-caption"> شريك واحد. صورة متكاملة. </div>
        </Reveal>
      </section>
      <div className="capability-strip">
        <div>
          {" "}
          الحلول الرقمية <span>+</span> الإنتاج الإبداعي <span>+</span>{" "}
          استراتيجية التسويق <span>+</span> نمو الأعمال{" "}
        </div>
      </div>
      <section className="section-wrap section-space">
        <Reveal className="section-heading">
          <div>
            <span className="eyebrow"> ٠١ / خدماتنا </span>
            <h2>
              {" "}
              حلول لها هدف. <br />
              <span> تعمل معًا من أجلك. </span>
            </h2>
          </div>
          <p>
            {" "}
            التقنية والتسويق في فريق واحد. نربط أنظمة عملك وهوية علامتك التجارية
            بأهداف واضحة.{" "}
          </p>
        </Reveal>
        <div className="division-grid">
          <Reveal className="division-card">
            <div className="division-number">
              01 <Code2 size={25} />
            </div>
            <h3> الحلول الرقمية </h3>
            <p>
              {" "}
              تقنية مدروسة تحول تحديات الأعمال المعقدة إلى منتجات رقمية
              مفيدة.{" "}
            </p>
            <div className="division-tags">
              <span> مواقع وتطبيقات </span>
              <span> أنظمة الأعمال </span>
              <span> الأتمتة </span>
            </div>
            <Link href="/ar/services#digital" className="text-link">
              {" "}
              استكشف الحلول الرقمية <ArrowUpRight size={18} />
            </Link>
          </Reveal>
          <Reveal className="division-card creative" delay={0.08}>
            <div className="division-number">
              02 <Component size={25} />
            </div>
            <h3> التسويق والإبداع </h3>
            <p>
              {" "}
              هوية مميزة ورسالة واضحة واستراتيجية مناسبة للوصول إلى جمهورك.{" "}
            </p>
            <div className="division-tags">
              <span> الهوية والمحتوى </span>
              <span> وسائل التواصل </span>
              <span> الأداء </span>
            </div>
            <Link href="/ar/services#marketing" className="text-link">
              {" "}
              استكشف التسويق والإبداع <ArrowUpRight size={18} />
            </Link>
          </Reveal>
        </div>
        <div className="service-mini-grid">
          {services
            .filter((s) => s.featured)
            .slice(0, 6)
            .map((s, i) => (
              <Link href={"/ar/services/" + s.slug} key={s.slug}>
                <span>0{i + 1}</span>
                {s.name}
                <ArrowUpRight size={17} />
              </Link>
            ))}
        </div>
      </section>
      <section className="work-section">
        <div className="section-wrap section-space">
          <Reveal className="section-heading">
            <div>
              <span className="eyebrow"> ٠٢ / أعمال مختارة </span>
              <h2>
                {" "}
                أفكار تتحول <br />
                <span> إلى واقع. </span>
              </h2>
            </div>
            <Link href="/ar/portfolio" className="secondary-link">
              {" "}
              شاهد جميع الأعمال <ArrowUpRight size={18} />
            </Link>
          </Reveal>
          <ProjectGallery projects={portfolio} />
        </div>
      </section>
      <section className="section-wrap section-space">
        <div className="why-layout">
          <Reveal>
            <span className="eyebrow"> ٠٣ / لماذا هيكسا بلس </span>
            <h2>
              {" "}
              رؤية تربط <br /> بين أعمالك <br />
              <span> وفرصها القادمة. </span>
            </h2>
            <Link href="/ar/about" className="text-link">
              {" "}
              تعرّف علينا <ArrowUpRight size={18} />
            </Link>
          </Reveal>
          <div className="principle-list">
            {[
              [
                "رؤية متكاملة",
                "نفكر في التقنية والتصميم والتسويق معًا منذ البداية.",
              ],
              ["أعمالك أولًا", "الحل المناسب يبدأ بفهم ما تريد تحقيقه."],
              [
                "وضوح في كل خطوة",
                "نطاق عمل متفق عليه، ومراحل واضحة، وتواصل مباشر.",
              ],
            ].map(([a, b], i) => (
              <Reveal key={a} className="principle">
                <span>0{i + 1}</span>
                <div>
                  <h3>{a}</h3>
                  <p>{b}</p>
                </div>
                <Check size={19} />
              </Reveal>
            ))}
          </div>
        </div>
      </section>
      <section className="process-section section-wrap section-space">
        <span className="eyebrow"> ٠٤ / كيف نعمل </span>
        <div className="section-heading">
          <h2>
            {" "}
            من أول سؤال <br />
            <span> إلى خطوتك القادمة. </span>
          </h2>
          <Link href="/ar/process" className="secondary-link">
            {" "}
            طريقة عملنا <ArrowUpRight size={18} />
          </Link>
        </div>
        <div className="process-grid">
          {[
            ["نفهم", "نستمع ونطرح الأسئلة ونفهم أهدافك."],
            ["نخطط", "نحول الاتجاه المناسب إلى خطة واضحة."],
            ["ننَفّذ", "نصمم ونبني ونختبر ونطور معًا."],
            ["ننمو", "نطلق المشروع بعناية ونخطط لما بعده."],
          ].map(([a, b], i) => (
            <Reveal key={a} delay={i * 0.06}>
              <span className="step-index">
                0{i + 1}
                <span>+</span>
              </span>
              <h3>{a}</h3>
              <p>{b}</p>
            </Reveal>
          ))}
        </div>
      </section>
      {testimonials.length > 0 && (
        <section className="section-wrap section-space">
          <span className="eyebrow"> بكلمات عملائنا </span>
          <div className="testimonial-grid">
            {testimonials.map((t) => (
              <blockquote key={t.id}>
                <p>“{t.quote}”</p>
                <cite>
                  {t.name} · {t.company}
                </cite>
              </blockquote>
            ))}
          </div>
        </section>
      )}
      <section className="section-wrap cta-section">
        <Reveal>
          <span className="eyebrow"> خطوتك القادمة تبدأ هنا </span>
          <h2>
            {" "}
            لديك رؤية؟ <br />
            <span> لنحولها إلى واقع. </span>
          </h2>
          <Link href="/ar/contact" className="primary-link">
            {" "}
            لنتحدث عن مشروعك <ArrowUpRight size={20} />
          </Link>
        </Reveal>
        <ChartNoAxesCombined className="cta-symbol" strokeWidth={0.6} />
      </section>
    </main>
  );
}
