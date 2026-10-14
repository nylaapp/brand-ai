// Run in the live blog post page (browser javascript tool). Returns a compact JSON summary.
(() => {
  const q = (s) => document.querySelector(s);
  const meta = (n) => (q(`meta[name="${n}"]`) || q(`meta[property="${n}"]`))?.content || null;
  const body = q('article') || q('main') || document.body;
  const text = (body.innerText || '').trim();
  const words = text.split(/\s+/).filter(Boolean).length;
  const ld = [...document.querySelectorAll('script[type="application/ld+json"]')].flatMap((s) => {
    try { const j = JSON.parse(s.textContent); return Array.isArray(j) ? j : (j['@graph'] || [j]); } catch (e) { return [{ '@type': 'PARSE_ERROR' }]; }
  });
  const types = ld.flatMap((o) => [].concat(o['@type'] || 'unknown'));
  const imgs = [...body.querySelectorAll('img')].map((i) => ({ src: (i.currentSrc || i.src || '').slice(0, 120), alt: i.getAttribute('alt') }));
  const host = location.hostname;
  const links = [...body.querySelectorAll('a[href]')].map((a) => a.href);
  const internal = links.filter((h) => { try { return new URL(h).hostname === host; } catch (e) { return false; } });
  const firstP = [...body.querySelectorAll('p')].map((p) => p.innerText.trim()).find((t) => t.split(/\s+/).length > 15) || '';
  const placeholders = [...new Set((text.match(/\[\[[^\]]{0,120}\]\]/g) || []))];
  const title = document.title || '';
  const desc = meta('description') || '';
  return {
    url: location.href,
    title, title_len: title.length,
    meta_description: desc, meta_len: desc.length,
    canonical: q('link[rel="canonical"]')?.href || null,
    robots: meta('robots'),
    og_image: meta('og:image'),
    h1_count: document.querySelectorAll('h1').length,
    h2: [...body.querySelectorAll('h2')].map((h) => h.innerText.trim()).slice(0, 20),
    h3_count: body.querySelectorAll('h3').length,
    jsonld_types: types,
    words,
    first_paragraph_words: firstP.split(/\s+/).filter(Boolean).length,
    images: { total: imgs.length, missing_alt: imgs.filter((i) => !i.alt).length, hotlinked: imgs.filter((i) => i.src && !i.src.includes(host) && !i.src.includes('cdn')).length, sample: imgs.slice(0, 4) },
    links: { internal: internal.length, external: links.length - internal.length, product_or_collection: internal.filter((h) => /\/(products|collections)\//.test(h)).length, blog: internal.filter((h) => /\/blogs\//.test(h)).length },
    placeholders_left: placeholders,
  };
})()
