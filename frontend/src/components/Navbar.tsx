import { NavLink, useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { Globe, Map, BarChart3, FolderOpen, LogIn, UserPlus } from "lucide-react";
import { Button } from "@/components/ui/button";

const tabs = [
  { to: "/", label: "Languages", icon: Globe },
  { to: "/map", label: "Map", icon: Map },
  { to: "/analytics", label: "Analytics", icon: BarChart3 },
  { to: "/sets", label: "Language Sets", icon: FolderOpen },
];

export default function Navbar() {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 border-b bg-card/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <NavLink to="/" className="flex items-center gap-2">
          <Globe className="h-6 w-6 text-primary" />
          <span className="font-display text-xl font-semibold tracking-tight text-foreground">
            Linguistic Atlas API
          </span>
        </NavLink>

        <nav className="hidden items-center gap-1 md:flex">
          {tabs.map((tab) => {
            const isActive =
              tab.to === "/"
                ? location.pathname === "/"
                : location.pathname.startsWith(tab.to);
            return (
              <NavLink
                key={tab.to}
                to={tab.to}
                className="relative px-4 py-2 text-sm font-medium transition-colors"
              >
                <span
                  className={
                    isActive
                      ? "text-primary"
                      : "text-muted-foreground hover:text-foreground"
                  }
                >
                  <tab.icon className="mr-1.5 inline-block h-4 w-4" />
                  {tab.label}
                </span>
                {isActive && (
                  <motion.div
                    layoutId="navbar-indicator"
                    className="absolute inset-x-2 -bottom-[1px] h-0.5 rounded-full bg-primary"
                    transition={{ type: "spring", stiffness: 380, damping: 30 }}
                  />
                )}
              </NavLink>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm">
            <LogIn className="mr-1.5 h-4 w-4" /> Login
          </Button>
          <Button size="sm">
            <UserPlus className="mr-1.5 h-4 w-4" /> Register
          </Button>
        </div>
      </div>
    </header>
  );
}
