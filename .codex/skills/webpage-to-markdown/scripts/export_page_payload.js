(() => {
  const q = (selector) => document.querySelector(selector);
  const text = (selector) => q(selector)?.innerText?.trim() || '';
  const attr = (selector, name) => q(selector)?.getAttribute(name) || '';

  const title =
    text('#activity-name .js_title_inner') ||
    text('#activity-name') ||
    text('h1') ||
    document.title ||
    'untitled';

  const payload = {
    title,
    url: location.href,
    author:
      text('#js_author_name_text') ||
      text('#js_author_name') ||
      attr('meta[name="author"]', 'content'),
    account: text('#js_name'),
    publish_time: text('#publish_time'),
    description:
      attr('meta[name="description"]', 'content') ||
      attr('meta[property="og:description"]', 'content'),
    cover:
      attr('#js_row_immersive_cover_img img', 'src') ||
      attr('meta[property="og:image"]', 'content'),
    htmlContent: document.documentElement.outerHTML,
  };

  const safeBase = (payload.title || 'page')
    .replace(/[^\w\u4e00-\u9fff-]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 60) || 'page';
  const filename = `${safeBase}_payload.json`;

  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: 'application/json',
  });
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = objectUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);

  return {
    success: true,
    title: payload.title,
    filename,
    hasAuthor: Boolean(payload.author),
    hasPublishTime: Boolean(payload.publish_time),
    htmlLength: payload.htmlContent.length,
  };
})();
