export function normalisePermissions(input: string[] | null | undefined): string[] {
  return Array.from(new Set((input ?? []).map((p) => p.trim()).filter(Boolean)));
}

function matchesGrantedPermission(granted: string, requested: string): boolean {
  if (granted === "*" || granted === requested) return true;
  if (!granted.endsWith(":*")) return false;
  const prefix = granted.slice(0, -2);
  return requested === prefix || requested.startsWith(`${prefix}:`);
}

export function hasPermission(permissions: string[] | null | undefined, requested: string): boolean {
  return normalisePermissions(permissions).some((granted) => matchesGrantedPermission(granted, requested));
}

export function hasAnyPermission(permissions: string[] | null | undefined, requested: string[]): boolean {
  return requested.some((permission) => hasPermission(permissions, permission));
}

export function hasAllPermissions(permissions: string[] | null | undefined, requested: string[]): boolean {
  return requested.every((permission) => hasPermission(permissions, permission));
}
