// Netlify serverless function — proxies Overpass airport queries.
// Receives POST from the browser with a URL-encoded body (data=<query>),
// parses out the query, then issues a plain GET to Overpass server-side.
// Server-side GET has no CORS complications and avoids body-forwarding quirks.

exports.handler = async (event) => {
  try {
    // Decode body (Netlify may base64-encode binary payloads)
    const rawBody = event.isBase64Encoded
      ? Buffer.from(event.body || '', 'base64').toString('utf8')
      : (event.body || '');

    const query = new URLSearchParams(rawBody).get('data');
    if (!query) {
      return { statusCode: 400, headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify({ error: 'Missing data parameter' }) };
    }

    const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;
    const resp = await fetch(url, { headers: { 'User-Agent': 'FlyBy-Radar/1.5' } });
    const text = await resp.text();

    return {
      statusCode: resp.status,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: text,
    };
  } catch (e) {
    return {
      statusCode: 502,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: e.message }),
    };
  }
};
