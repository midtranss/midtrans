const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");

function readJson(relativePath) {
  return JSON.parse(fs.readFileSync(path.join(root, relativePath), "utf8"));
}

function writeFile(relativePath, content) {
  const target = path.join(root, relativePath);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.writeFileSync(target, content, "utf8");
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function escapeAttribute(value) {
  return escapeHtml(value).replace(/'/g, "&#39;");
}

function toOutputPath(slug) {
  if (slug === "/") {
    return "index.html";
  }

  return path.join(slug.replace(/^\/|\/$/g, ""), "index.html");
}

function getString(strings, group, key, fallback = "") {
  return strings[group] && strings[group][key] ? strings[group][key] : fallback;
}

function getActionLabel(strings, key, fallback) {
  return getString(strings, "actions", key, fallback);
}

function canonicalFor(page, content) {
  return content.seo.canonical || page.canonical;
}

function buildHreflang(page, registry, languageMap) {
  const equivalents = registry.filter((candidate) => candidate.hreflangGroup === page.hreflangGroup);
  const availableCodes = new Set(languageMap.availableLanguages.map((language) => language.code));
  const links = equivalents
    .filter((candidate) => availableCodes.has(candidate.language))
    .map(
      (candidate) =>
        `    <link rel="alternate" hreflang="${escapeAttribute(candidate.language)}" href="${escapeAttribute(candidate.canonical)}">`
    );
  const defaultPage =
    equivalents.find((candidate) => candidate.language === languageMap.defaultLanguage) || equivalents[0];

  if (defaultPage) {
    links.push(`    <link rel="alternate" hreflang="x-default" href="${escapeAttribute(defaultPage.canonical)}">`);
  }

  return links.join("\n");
}

function buildHead(page, content, registry, languageMap) {
  const seo = content.seo;
  const canonical = canonicalFor(page, content);
  const og = seo.openGraph || {};
  const hreflang = buildHreflang(page, registry, languageMap);

  return `    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(seo.title)}</title>
    <meta name="description" content="${escapeAttribute(seo.description)}">
    <meta name="robots" content="${escapeAttribute(seo.robots || "index,follow")}">
    <link rel="canonical" href="${escapeAttribute(canonical)}">
${hreflang}
    <meta property="og:type" content="website">
    <meta property="og:title" content="${escapeAttribute(og.title || seo.title)}">
    <meta property="og:description" content="${escapeAttribute(og.description || seo.description)}">
    <meta property="og:url" content="${escapeAttribute(canonical)}">
    <link rel="stylesheet" href="/assets/styles.css">`;
}

function organizationSchema(company) {
  const officeTelephones = company.offices.flatMap((office) =>
    office.contacts.map((contact) => contact.schemaTelephone)
  );
  const contactPoint = company.offices.map((office) => ({
    "@type": "ContactPoint",
    telephone: office.contacts[0].schemaTelephone,
    contactType: office.label,
    areaServed: office.schemaAddress.addressCountry
  }));

  contactPoint.push({
    "@type": "ContactPoint",
    telephone: company.whatsapp.schemaTelephone,
    contactType: company.whatsapp.label,
    areaServed: "SY"
  });

  return {
    "@type": "Organization",
    "@id": `${company.primaryDomain}/#organization`,
    name: company.name,
    url: `${company.primaryDomain}/`,
    telephone: officeTelephones,
    address: company.offices.map((office) => ({
      "@type": "PostalAddress",
      ...office.schemaAddress
    })),
    contactPoint
  };
}

function breadcrumbSchema(content, strings, company) {
  if (!content.breadcrumbs || content.breadcrumbs.length === 0) {
    return null;
  }

  return {
    "@type": "BreadcrumbList",
    "@id": `${content.seo.canonical}#breadcrumb`,
    itemListElement: content.breadcrumbs.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.label || getString(strings, "breadcrumbs", item.labelKey, item.labelKey),
      item: item.url.startsWith("http") ? item.url : `${company.primaryDomain}${item.url}`
    }))
  };
}

function pageSchema(page, content, company) {
  const canonical = canonicalFor(page, content);
  return {
    "@type": page.pageType === "contact" ? "ContactPage" : "WebPage",
    "@id": `${canonical}#webpage`,
    url: canonical,
    name: content.seo.title,
    description: content.seo.description,
    inLanguage: content.language,
    isPartOf: {
      "@id": `${company.primaryDomain}/#website`
    },
    about: {
      "@id": `${company.primaryDomain}/#organization`
    }
  };
}

function websiteSchema(company) {
  return {
    "@type": "WebSite",
    "@id": `${company.primaryDomain}/#website`,
    name: company.name,
    url: `${company.primaryDomain}/`,
    publisher: {
      "@id": `${company.primaryDomain}/#organization`
    }
  };
}

function buildSchema(page, content, strings, company) {
  const graph = [organizationSchema(company), websiteSchema(company), pageSchema(page, content, company)];
  const breadcrumbs = breadcrumbSchema(content, strings, company);

  if (breadcrumbs) {
    graph.push(breadcrumbs);
  }

  return JSON.stringify(
    {
      "@context": "https://schema.org",
      "@graph": graph
    },
    null,
    2
  );
}

function renderHeader(strings, company, currentSlug) {
  const homeCurrent = currentSlug === "/" ? ' aria-current="page"' : "";
  const contactCurrent = currentSlug === "/contact-us/" ? ' aria-current="page"' : "";

  return `<header class="site-header">
      <nav class="nav" aria-label="Main navigation">
        <a class="brand" href="/"${homeCurrent}>${escapeHtml(company.brandName)}</a>
        <div class="nav-links">
          <a href="/contact-us/"${contactCurrent}>${escapeHtml(strings.navigation.contact)}</a>
        </div>
      </nav>
    </header>`;
}

function renderFooter(company, strings) {
  return `<footer class="site-footer">
      <p>${strings.footer.copyrightPrefix} ${escapeHtml(company.name)}</p>
    </footer>`;
}

function renderBreadcrumbs(content, strings) {
  if (!content.breadcrumbs || content.breadcrumbs.length === 0) {
    return "";
  }

  const items = content.breadcrumbs
    .map((item, index) => {
      const label = item.label || getString(strings, "breadcrumbs", item.labelKey, item.labelKey);
      const isLast = index === content.breadcrumbs.length - 1;

      if (isLast) {
        return `<li aria-current="page">${escapeHtml(label)}</li>`;
      }

      return `<li><a href="${escapeAttribute(item.url)}">${escapeHtml(label)}</a></li>`;
    })
    .join("\n          ");

  return `<nav class="breadcrumbs" aria-label="Breadcrumb">
        <ol>
          ${items}
        </ol>
      </nav>`;
}

function renderHero(content) {
  const hero = content.hero;
  const cta = hero.cta
    ? `
        <a class="button" href="${escapeAttribute(hero.cta.url)}" data-action-key="${escapeAttribute(hero.cta.labelKey)}"></a>`
    : "";

  return `<section class="${content.pageType === "home" ? "hero" : "page-heading"}">
        <p class="eyebrow">${escapeHtml(hero.eyebrow)}</p>
        <h1>${escapeHtml(hero.h1)}</h1>
        <p class="lede">${escapeHtml(hero.summary)}</p>${cta}
      </section>`;
}

function hydrateActionLabels(html, strings) {
  return html.replace(
    /<a class="button" href="([^"]+)" data-action-key="([^"]+)"><\/a>/g,
    (_, href, key) =>
      `<a class="button" href="${href}">${escapeHtml(getActionLabel(strings, key, key))}</a>`
  );
}

function renderOfficeCards(company, mode) {
  const fullClass = mode === "detail" ? " full" : "";

  return company.offices
    .map((office) => {
      const address = office.addressLines.map((line) => escapeHtml(line)).join("<br>\n            ");

      if (mode === "detail") {
        const details = office.contacts
          .map(
            (contact) => `<div>
              <dt>${escapeHtml(contact.label)}</dt>
              <dd><a href="${escapeAttribute(contact.href)}">${escapeHtml(contact.display)}</a></dd>
            </div>`
          )
          .join("\n            ");

        return `<article class="office-card${fullClass}">
          <p class="office-label">${escapeHtml(office.label)}</p>
          <h2>${escapeHtml(office.name)}</h2>
          <address>
            ${address}
          </address>
          <dl class="detail-list">
            ${details}
          </dl>
        </article>`;
      }

      const contacts = office.contacts
        .map(
          (contact) =>
            `<li>${escapeHtml(contact.label)}: <a href="${escapeAttribute(contact.href)}">${escapeHtml(contact.display)}</a></li>`
        )
        .join("\n            ");

      return `<article class="office-card${fullClass}">
          <p class="office-label">${escapeHtml(office.label)}</p>
          <h2>${escapeHtml(office.name)}</h2>
          <address>
            ${address}
          </address>
          <ul class="contact-list">
            ${contacts}
          </ul>
        </article>`;
    })
    .join("\n\n        ");
}

function renderWhatsappPanel(company, content, strings, mode) {
  const section = content.sections.whatsapp || {};

  if (mode === "detail") {
    return `<section class="whatsapp-panel" aria-label="${escapeAttribute(strings.labels.whatsapp)} contact">
        <div>
          <p class="office-label">${escapeHtml(company.whatsapp.label)}</p>
          <h2>${escapeHtml(company.whatsapp.display)}</h2>
          <p>${escapeHtml(section.supportingText)}</p>
        </div>
        <a class="button secondary" href="${escapeAttribute(company.whatsapp.url)}">${escapeHtml(strings.actions.openWhatsapp)}</a>
      </section>`;
  }

  return `<section class="whatsapp-panel" aria-label="${escapeAttribute(strings.labels.whatsapp)} contact">
        <div>
          <p class="office-label">${escapeHtml(company.whatsapp.label)}</p>
          <h2>${escapeHtml(section.heading)}</h2>
        </div>
        <a class="button secondary" href="${escapeAttribute(company.whatsapp.url)}">${escapeHtml(company.whatsapp.display)}</a>
      </section>`;
}

function renderHome(content, company, strings) {
  const officeSection = content.sections.offices;

  return `${renderHero(content)}

      <section class="office-grid" aria-label="${escapeAttribute(officeSection.ariaLabel)}">
        ${renderOfficeCards(company, "summary")}
      </section>

      ${renderWhatsappPanel(company, content, strings, "summary")}`;
}

function renderContact(content, company, strings) {
  const officeSection = content.sections.offices;

  return `${renderBreadcrumbs(content, strings)}
      ${renderHero(content)}

      <section class="office-grid" aria-label="${escapeAttribute(officeSection.ariaLabel)}">
        ${renderOfficeCards(company, "detail")}
      </section>

      ${renderWhatsappPanel(company, content, strings, "detail")}`;
}

function renderLayout({ page, content, strings, company, registry, languageMap, body }) {
  const language = languageMap.availableLanguages.find((item) => item.code === content.language);
  const schema = buildSchema(page, content, strings, company);

  return `<!doctype html>
<html lang="${escapeAttribute(content.language)}" dir="${escapeAttribute(language ? language.dir : "ltr")}">
  <head>
${buildHead(page, content, registry, languageMap)}
    <script type="application/ld+json">
${schema
  .split("\n")
  .map((line) => `      ${line}`)
  .join("\n")}
    </script>
  </head>
  <body>
    ${renderHeader(strings, company, page.slug)}

    <main>
      ${hydrateActionLabels(body, strings)}
    </main>

    ${renderFooter(company, strings)}
  </body>
</html>
`;
}

function renderPage(page, registry, languageMap, company) {
  const content = readJson(page.contentFile);
  const strings = readJson(`strings/${page.language}.json`);
  const templateMap = {
    HomePageTemplate: renderHome,
    ContactPageTemplate: renderContact
  };
  const renderTemplate = templateMap[page.template];

  if (!renderTemplate) {
    throw new Error(`No renderer registered for ${page.template}`);
  }

  return renderLayout({
    page,
    content,
    strings,
    company,
    registry,
    languageMap,
    body: renderTemplate(content, company, strings)
  });
}

function assertProtectedPages(registry, protectedPages) {
  const protectedSet = new Set(protectedPages.pages);

  for (const page of registry) {
    if (protectedSet.has(page.slug) && !page.protected) {
      throw new Error(`${page.slug} is listed as protected but is not flagged in page-registry.json`);
    }
  }
}

function build() {
  const registry = readJson("config/page-registry.json");
  const protectedPages = readJson("config/protected-pages.json");
  const languageMap = readJson("config/language-map.json");
  const company = readJson("config/company-profile.json");

  assertProtectedPages(registry, protectedPages);

  for (const page of registry) {
    writeFile(toOutputPath(page.slug), renderPage(page, registry, languageMap, company));
  }

  console.log(`Generated ${registry.length} page(s).`);
}

build();
