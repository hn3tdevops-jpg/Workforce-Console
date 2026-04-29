import React, { createContext, useContext, useEffect, useState } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { fetchApi } from "./api-client";
import { hasPermission as matchesPermission, normalisePermissions } from "./permissions";
import { SessionInfo } from "@workspace/api-client-react/src/generated/api.schemas";
import { useToast } from "@/hooks/use-toast";

const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

const DEMO_SESSION: SessionInfo = {
  id: "user-001",
  email: "manager@silversands.com",
  first_name: "Sarah",
  last_name: "Okonkwo",
  is_active: true,
  active_business_id: "biz-001",
  roles: ["owner"],
  permissions: ["owner:*"],
  memberships: [
    {
      business_id: "biz-001",
      business_name: "Silver Sands Motel",
      role: "owner",
    },
  ],
};

interface ApiUserSummary {
  id: string;
  email: string;
  is_active?: boolean;
  first_name?: string;
  last_name?: string;
  is_superadmin?: boolean;
}

interface ApiMembershipSummary {
  business_id: string;
  status?: string;
  is_owner?: boolean;
  business_name?: string;
  role?: string;
}

interface ApiMeResponse {
  user?: ApiUserSummary;
  id?: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  business_id?: string;
  active_business_id?: string;
  memberships?: ApiMembershipSummary[];
  roles?: string[];
  permissions?: string[];
}

interface ApiLoginResponse {
  access_token: string;
  token_type?: string;
  business_id?: string;
  user?: ApiUserSummary;
}

function mapToSessionInfo(data: ApiMeResponse, effectivePermissions: string[] = []): SessionInfo {
  const id = data.user?.id ?? data.id ?? "";
  const email = data.user?.email ?? data.email ?? "";
  const first_name = data.user?.first_name ?? data.first_name;
  const last_name = data.user?.last_name ?? data.last_name;
  const is_active = data.user?.is_active ?? true;
  const active_business_id = data.business_id ?? data.active_business_id;

  const memberships = (data.memberships ?? []).map((m) => ({
    business_id: m.business_id,
    business_name: m.business_name ?? "",
    role: m.is_owner ? "owner" : (m.role ?? "member"),
  }));

  return {
    id,
    email,
    first_name,
    last_name,
    is_active,
    active_business_id,
    memberships,
    roles: data.roles ?? [],
    permissions: normalisePermissions(effectivePermissions.length > 0 ? effectivePermissions : (data.permissions ?? [])),
  };
}

export interface EmploymentAssignment {
  id: string;
  role_name: string;
  scope_type: string;
  permissions: string[];
}

export interface EmploymentScope {
  employee_profile_id: string;
  employee_name: string;
  employee_code: string | null;
  job_title: string | null;
  department: string | null;
  employment_status: string;
  assignments: EmploymentAssignment[];
  effective_permissions: string[];
  is_super_admin: boolean;
}

interface AccessContextResponse {
  user_id: string;
  has_access: boolean;
  active_scope_count: number;
  scopes: EmploymentScope[];
  resolved_at: string;
}

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  session: SessionInfo | null;
  employmentScope: EmploymentScope | null;
  effectivePermissions: string[];
  login: (credentials: LoginRequest) => Promise<void>;
  logout: () => void;
  switchBusiness: (businessId: string) => Promise<void>;
  hasPermission: (permission: string) => boolean;
  hasEffectivePermission: (permission: string) => boolean;
  hasRole: (role: string) => boolean;
  hasEmployeePermission: (permission: string) => boolean;
  isOwner: () => boolean;
  isSuperAdmin: () => boolean;
  canSwitchBusiness: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<SessionInfo | null>(null);
  const [employmentScope, setEmploymentScope] = useState<EmploymentScope | null>(null);
  const [effectivePermissions, setEffectivePermissions] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const loadSession = async () => {
    if (DEMO_MODE) {
      setSession(DEMO_SESSION);
      setEffectivePermissions(normalisePermissions(DEMO_SESSION.permissions));
      setIsLoading(false);
      return;
    }

    const token = localStorage.getItem("workforce_token");
    if (!token) {
      try {
        const data = await fetchApi<any>("/bootstrap");
        const mapped: any = {
          id: data.user?.id ?? "",
          email: data.user?.email ?? "",
          first_name: data.user?.name ?? undefined,
          last_name: undefined,
          is_active: true,
          active_business_id: data.businesses?.[0]?.id ?? undefined,
          memberships: (data.businesses ?? []).map((b: any) => ({ business_id: b.id, business_name: b.name, role: b.default_role ?? "member", enabled_modules: (data.features && data.features.enabled_modules) ? data.features.enabled_modules : undefined }),
          roles: (data.roles ?? []).map((r: any) => r.name ?? r),
          permissions: [].concat(...(data.roles ?? []).map((r: any) => r.permissions ?? [])),
        };
        setSession(mapped);
        setEffectivePermissions(normalisePermissions(mapped.permissions));
        setIsLoading(false);
        return;
      } catch (err) {
        setSession(null);
        setEffectivePermissions([]);
        setIsLoading(false);
        return;
      }
    }

    try {
      const data = await fetchApi<ApiMeResponse>("/auth/me");
      const activeBusinessId = data.business_id ?? data.active_business_id ?? "";
      let permissions: string[] = data.permissions ?? [];
      if (activeBusinessId) {
        try {
          permissions = await fetchApi<string[]>(`/me/effective-permissions?business_id=${encodeURIComponent(activeBusinessId)}`);
        } catch {
          permissions = data.permissions ?? [];
        }
      }
      const info = mapToSessionInfo(data, permissions);
      setSession(info);
      setEffectivePermissions(normalisePermissions(permissions));
      try {
        const userId = data.user?.id ?? data.id ?? info.id;
        if (userId) {
          const ctx = await fetchApi<AccessContextResponse>("/auth/me/access-context");
          setEmploymentScope(ctx.scopes?.[0] ?? null);
        }
      } catch {
        setEmploymentScope(null);
      }
    } catch {
      localStorage.removeItem("workforce_token");
      setSession(null);
      setEffectivePermissions([]);
      setEmploymentScope(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadSession();

    const handleUnauthorized = () => {
      localStorage.removeItem("workforce_token");
      setSession(null);
      setEffectivePermissions([]);
      queryClient.clear();
      window.location.href = "/login";
    };

    window.addEventListener("auth:unauthorized", handleUnauthorized);
    return () => window.removeEventListener("auth:unauthorized", handleUnauthorized);
  }, []);

  const login = async (credentials: LoginRequest) => {
    if (DEMO_MODE) {
      setSession(DEMO_SESSION);
      setEffectivePermissions(normalisePermissions(DEMO_SESSION.permissions));
      return;
    }

    const path = "/auth/login";

    try {
      const response = await fetchApi<ApiLoginResponse>(path, {
        method: "POST",
        body: JSON.stringify({ ...credentials, business_id: null }),
      });
      localStorage.setItem("workforce_token", response.access_token);
      await loadSession();
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : String(err);
      throw new Error(msg);
    }
  };

  const hasEmployeePermission = (permission: string) => {
    if (!employmentScope) return false;
    const perms = employmentScope.effective_permissions ?? [];
    return perms.includes("*") || perms.includes(permission);
  };

  const logout = () => {
    localStorage.removeItem("workforce_token");
    setSession(null);
    setEffectivePermissions([]);
    setEmploymentScope(null);
    queryClient.clear();
    window.location.href = "/login";
  };

  const switchBusiness = async (businessId: string) => {
    try {
      const response = await fetchApi<ApiLoginResponse>("/auth/switch-business", {
        method: "POST",
        body: JSON.stringify({ business_id: businessId }),
      });
      localStorage.setItem("workforce_token", response.access_token);
      await queryClient.invalidateQueries();
      await loadSession();
      toast({ title: "Switched business context" });
    } catch (error: unknown) {
      const msg = error instanceof Error ? error.message : "Unknown error";
      toast({
        title: "Failed to switch business",
        description: msg,
        variant: "destructive",
      });
      throw error;
    }
  };

  const hasPermission = (permission: string) =>
    session?.permissions?.some(
      (p: string) => p === permission || p === "owner:*" || p === "business:owner"
    ) ?? false;

  const hasEffectivePermission = (permission: string) =>
    matchesPermission(effectivePermissions, permission);

  const hasRole = (role: string) =>
    session?.roles?.some((r: string) => r.toLowerCase() === role.toLowerCase()) ?? false;

  const isOwner = () =>
    hasRole("owner") ||
    hasPermission("owner:*") ||
    hasPermission("business:owner") ||
    (session?.memberships?.some((m: any) => m.role?.toLowerCase() === "owner") ?? false);

  const isSuperAdmin = () =>
    hasRole("superadmin") ||
    hasPermission("superadmin:*") ||
    (session as (SessionInfo & { is_superadmin?: boolean }) | null)?.is_superadmin === true;

  const canSwitchBusiness = (session?.memberships?.length ?? 0) > 1;

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!session,
        isLoading,
        session,
        employmentScope,
        effectivePermissions,
        login,
        logout,
        switchBusiness,
        hasPermission,
        hasEffectivePermission,
        hasRole,
        hasEmployeePermission,
        isOwner,
        isSuperAdmin,
        canSwitchBusiness,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
