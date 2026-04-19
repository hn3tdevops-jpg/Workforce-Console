#!/usr/bin/env node
// Enhanced smoke test: GET /api/v1/bootstrap and validate frontend hydration mapping

const API_BASE = process.env.API_BASE || 'http://127.0.0.1:8011/api/v1';
const DEFAULT_ENABLED_MODULES = [
  'dashboard','rooms','property-map','tasks','assignments','shifts','timeline','users','employees','studio','promotions','inspections','session','inventory','maintenance','communications'
];
const fetchFn = typeof globalThis.fetch === 'function' ? globalThis.fetch.bind(globalThis) : null;

(async function(){
  console.log('Using API_BASE:', API_BASE);
  try{
    if (!fetchFn) {
      console.error('This script requires Node.js 18+ with built-in fetch support.');
      process.exit(5);
    }
    const res = await fetchFn(API_BASE + '/bootstrap', { method: 'GET' });
    console.log('Status:', res.status);
    if (!res.ok) process.exit(2);
    const data = await res.json();
    console.log('Received keys:', Object.keys(data));

    const required = ['user','businesses','locations','roles','features'];
    const missing = required.filter(k => !(k in data));
    if (missing.length) {
      console.error('Missing keys in bootstrap payload:', missing);
      process.exit(3);
    }

    const mapped = {
      id: data.user?.id ?? '',
      email: data.user?.email ?? data.user?.name ?? '',
      first_name: data.user?.name ?? undefined,
      active_business_id: (data.businesses && data.businesses[0] && data.businesses[0].id) || undefined,
      memberships: (data.businesses || []).map(b => ({ business_id: b.id, business_name: b.name, role: b.default_role || 'member', enabled_modules: (data.features && data.features.enabled_modules) ? data.features.enabled_modules : undefined })),
      roles: (data.roles || []).map(r => typeof r === 'string' ? r : r.name),
      permissions: [].concat(...( (data.roles || []).map(r => r.permissions || []) )),
    };

    console.log('Mapped session membership count:', (mapped.memberships || []).length);

    const membership = mapped.memberships[0] || null;
    const enabledModules = membership?.enabled_modules ?? (data.features && data.features.enabled_modules) ?? DEFAULT_ENABLED_MODULES;
    console.log('Derived enabled modules length:', (enabledModules || []).length);

    if ((mapped.memberships || []).length === 0) {
      console.error('No memberships derived from bootstrap payload');
      process.exit(4);
    }

    console.log('Smoke bootstrap + shell-hydration checks passed');
    process.exit(0);
  }catch(e){
    console.error('Smoke test failed:', e.message || e);
    process.exit(5);
  }
})();
